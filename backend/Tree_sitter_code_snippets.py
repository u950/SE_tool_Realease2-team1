from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjs


class CodeExtractor:
    def __init__(self, code):
        # Load JavaScript language
        Js_language = Language(tsjs.language(), 'javascript')
        self.parser = Parser()
        self.parser.set_language(Js_language)
        self.code = code
        self.code_snippets = []

    def extract_code_snippet(self, node):
        if node.type == 'jsx_element' or node.type == 'function_declaration' or node.type == "arrow_function":
            code_snippet = self.code[node.start_byte:node.end_byte]
            snippet_info = {
                "code_snippet": code_snippet,
            }
            self.code_snippets.append(snippet_info)

    def traverse(self, node):
        if node.type == 'jsx_element' or node.type == 'function_declaration' or node.type == "arrow_function":
            self.extract_code_snippet(node)
        for child in node.children:
            self.traverse(child)

    def parse_code(self):
        tree = self.parser.parse(bytes(self.code, "utf8"))
        self.traverse(tree.root_node)

    def get_code_snippets(self):
        return self.code_snippets

# Example usage:
# if __name__ == "__main__":
#     file_path = "/Users/apgur/Desktop/project-tool/mern-marketplace/client/auction/Auctions.js"
#     code_extractor = CodeExtractor(file_path)
#     code_extractor.parse_code()