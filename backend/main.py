import Tree_sitter_code_snippets as tscs
import Dependency_extract as de


class CodeSnippetExtractor:
    def __init__(self,directory):
        self.path = directory
        dependencies_extractor = de.DependencyExtractor(directory)
        dependencies_extractor.run_extraction()
        self.main_dependency_list = dependencies_extractor.return_dependencies()
        
        

    def extract_code_snippets(self, file_path):
        file = open(file_path, "r", encoding="utf-8")
        code = file.read()

        code_extractor = tscs.CodeExtractor(code)
        code_extractor.parse_code()
        code_snippets = code_extractor.get_code_snippets()

        return code_snippets

    def parse_dependency_list(self, main_list):
        main_list=self.main_dependency_list
        ls = 0
        l={}
        
        for node in main_list:
            filename = node["exactPath"]
            code_snippets = self.extract_code_snippets(filename)
            keywords = node["local_dependent"]
            if keywords:
                p = len(code_snippets)
            
                for key in keywords:
                    s = []
                    for i in range(p - 1, -1, -1):
                        k = True
                        for j in s:
                            if j in code_snippets[i]["code_snippet"]:
                                k = False
                                break
                            if code_snippets[i]["code_snippet"] in j:
                                k = False
                                break
                        if key in code_snippets[i]["code_snippet"] and k:
                            s.append(code_snippets[i]["code_snippet"])
                    l[key] = s

                if l:
                    ls += 1
            else:
                continue
        return l
    
    def get_list(self):
        return self.main_dependency_list

# if __name__ == "__main__":
#     directory = "./mern-marketplace"
#     extractor = CodeSnippetExtractor(directory)
#     results = extractor.get_list()
#     print(results)