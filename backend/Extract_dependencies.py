import os
import esprima
import json


class JSProjectAnalyzer:
    def __init__(self):
        self.file_set = set()
        self.depend_list = []

    def is_js_file(self, filename):
        return filename.endswith(".js") or filename.endswith(".jsx")

    def imported_statement_usages(self,ast_body,imports_name_list, source_code):
        
        if ast_body.type != 'ImportDeclaration':
            start_line ,end_line = ast_body.range
            code_snippet = source_code[start_line:end_line]
            for value in imports_name_list:
                if value in code_snippet:
                    return code_snippet
                return "null"

    def extract_dependencies(self, ast_body, filename, code_data):
        dependencies = []
        local_name_of_dependency = []
        function_extract = []
        if ast_body.type == 'ImportDeclaration':
            for specifier in ast_body.specifiers:
                if specifier.type == 'ImportDefaultSpecifier' or specifier.type == 'ImportSpecifier':
                    dependent_name = os.path.basename(ast_body.source.value)
                    d_value = specifier.local.name
                    for ext in ['', '.js', '.jsx']:
                        if dependent_name + ext in self.file_set:
                            dependencies.append(dependent_name + ext)
                            local_name_of_dependency.append(d_value)

        usages = self.imported_statement_usages(ast_body,local_name_of_dependency, code_data)
        function_extract.append(usages)

        return dependencies, local_name_of_dependency, function_extract

    def exception_parsing(self, filepath, keywords):
        codes = ""
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in enumerate(file):
                if any(key in line for key in keywords):
                    codes += line
        try:
            # print(codes)
            ast = esprima.parseModule(codes, {"jsx": True, "range": True})
            return ast
        except Exception as error:
            print(f"Exception failed {os.path.basename(filepath)} :", error)
            return -1

    def parse_js_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                js_code = file.read()
            ast = esprima.parseModule(js_code, {"jsx": True, "range": True})
            return ast, js_code
        except Exception as error:
            print(f"Parsing With exception file {os.path.basename(file_path)}: {error}")
            ast1 = self.exception_parsing(file_path, keywords=['import', 'require'])
            return ast1, js_code

    def analyze_dependencies(self, js_file):
        fileName_with_extension = os.path.basename(js_file)
        ast, code = self.parse_js_file(js_file)
        if ast is None:
            return

        dependencies = []
        local_names = []
        imported_usages = []
        for node in ast.body:
            external_dependency, local_name_dependent, function_data = self.extract_dependencies(node,
                                                                                                 fileName_with_extension,
                                                                                                 code)
            dependencies.extend(external_dependency)
            local_names.extend(local_name_dependent)
            imported_usages.extend(function_data)
        return {
            "filename": os.path.relpath(js_file, self.directory),
            "scriptName": fileName_with_extension,
            "dependencies": dependencies,
            "local_names": local_names,
        }

    def analyze_repo(self, directory):
        self.directory = directory
        js_files = [os.path.join(root, file)
                    for root, _, files in os.walk(directory)
                    for file in files if self.is_js_file(file)]

        for file in js_files:
            self.file_set.add(os.path.basename(file))

        for js_file in js_files:
            dependency_info = self.analyze_dependencies(js_file)
            if dependency_info:
                self.depend_list.append(dependency_info)

        return json.dumps(self.depend_list, indent=4)


# # Example usage
# analyzer = JSProjectAnalyzer()
# directory = ""
# dependencies_json = analyzer.analyze_repo(directory)
# # print(dependencies_json)
