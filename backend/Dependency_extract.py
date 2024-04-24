import os
import esprima
import json


class DependencyExtractor:
    def __init__(self, directory):
        self.directory = directory
        self.keywords = ['import', 'require']
        self.file_set = []
        self.dependent_list_main = []

    def is_js_file(self, filename):
        return filename.endswith(".js") or filename.endswith('.jsx')

    def extract_dependencies(self, node):
        dependencies = []
        local_dep = []
        if node.type == "VariableDeclaration":
            for declaration in node.declarations:
                if declaration.init.type == "CallExpression":
                    if declaration.init.callee.name == "require":
                        dependent_name = declaration.init.arguments[0].value
                        d_value = declaration.id.name
                        dependent_name_base = os.path.basename(dependent_name)
                        if dependent_name_base in self.file_set and dependent_name.startswith("."):
                            dependencies.append(dependent_name)
                            local_dep.append(d_value)
                        elif dependent_name_base + ".js" in self.file_set and dependent_name.startswith("."):
                            dependencies.append(dependent_name + ".js")
                            local_dep.append(d_value)
                        elif dependent_name_base + ".jsx" in self.file_set and dependent_name.startswith("."):
                            dependencies.append(dependent_name + ".jsx")
                            local_dep.append(d_value)

        elif node.type == "ImportDeclaration":
            for specifier in node.specifiers:
                if specifier.type == "ImportSpecifier" or specifier.type == "ImportDefaultSpecifier":
                    dependent_name = node.source.value
                    d_value = specifier.local.name
                    dependent_name_base = os.path.basename(dependent_name)
                    if dependent_name_base in self.file_set and dependent_name.startswith("."):
                        dependencies.append(dependent_name)
                        local_dep.append(d_value)
                    elif dependent_name_base + ".js" in self.file_set and dependent_name.startswith("."):
                        dependencies.append(dependent_name + ".js")
                        local_dep.append(d_value)
                    elif dependent_name_base + ".jsx" in self.file_set and dependent_name.startswith("."):
                        dependencies.append(dependent_name + ".jsx")
                        local_dep.append(d_value)
        return dependencies, local_dep

    def read_directory(self, file_path):
        source = ""
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.readlines()
            for line in code:
                if any(keyword in line for keyword in self.keywords):
                    source += line
        try:
            if source != "":
                return esprima.parseModule(source, {"jsx": True})
            else:
                return None
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    def parse_file_extract_dependencies(self, files_list):
        intermediate_dependency_list=[]
        idDict = {}
        for js_file in files_list:
            dependencies = []
            local_dep = []
            ast = self.read_directory(js_file)
            if ast:
                try:
                    for body in ast.body:
                        temp1, temp2 = self.extract_dependencies(body)
                        dependencies.extend(temp1)
                        local_dep.extend(temp2)
                except Exception as e:
                    print(f"Error in file {js_file}: {e}")
            else:
                dependencies.extend([])
                local_dep.extend([])

            file_name_with_extension = os.path.basename(js_file)
            idDict[os.path.relpath(js_file, self.directory)] = len(intermediate_dependency_list)
            intermediate_dependency_list.append({
                "id": len(intermediate_dependency_list),
                "label": file_name_with_extension,
                "scriptName": os.path.relpath(js_file, self.directory),
                "exactPath": js_file,
                "dependencies": dependencies,
                "local_dependent": local_dep
            })
        for item in intermediate_dependency_list:
            depId=[]
            addr = item["scriptName"].split("\\")
            g = ''
            for j in addr[:-1]:
                if g == '':
                    g = j
                else:
                    g = g + '\\' + j
            for j in item["dependencies"]:
                l = j.split('/')
                s = 0
                for k in range(0, len(l) - 1):
                    if l[k] == '..':
                        s = s + 1
                if l[0] == '.':
                    x = ''
                    if s > len(addr) - 1:
                        continue
                    for k in range(0, len(addr) - 1 - s):
                        if x == '':
                            x = addr[k]
                        else:
                            x = x + '\\' + addr[k]
                    for k in range(s + 1, len(l)):
                        if x == '':
                            x = l[k]
                        else:
                            x = x + '\\' + l[k]
                    depId.append((j, idDict[x]))
                else:
                    x = ''
                    if s > len(addr) - 1:
                        continue
                    for k in range(0, len(addr) - 1 - s):
                        if x == '':
                            x = addr[k]
                        else:
                            x = x + '\\' + addr[k]
                    for k in range(s, len(l)):
                        if x == '':
                            x = l[k]
                        else:
                            x = x + '\\' + l[k]
                    depId.append((j, idDict[x]))
            self.dependent_list_main.append({
                "id": item["id"],
                "exactPath": item["exactPath"],
                "label": item["label"],
                "group": g,
                "scriptName": item["scriptName"],
                "dependencies": depId,
                "local_dependent": item["local_dependent"]
            })


    def run_extraction(self):
        js_files = [os.path.join(root, file) for root, _, files in os.walk(self.directory) for file in files if
                    self.is_js_file(file)]
        for js_file in js_files:
            self.file_set.append(os.path.basename(js_file))
        self.parse_file_extract_dependencies(js_files)

    # def write_to_json(self, output_file="output.json"):
    #     json_obj = json.dumps(self.dependent_list_main, indent=4)
    #     with open(output_file, "w") as outfile:
    #         outfile.write(json_obj)

    def return_dependencies(self):
        return self.dependent_list_main


# Example usage:
if __name__ == "__main__":
    extractor = DependencyExtractor("./mern-ecommerce")
    print(extractor.run_extraction())