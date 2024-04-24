from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjs
from transformers import BartTokenizer, BartForConditionalGeneration
import torch

# Load tokenizer and model
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn").to('cuda' if torch.cuda.is_available() else 'cpu')

# Parse code using tree-sitter
JAVASCRIPT_LANGUAGE = Language(tsjs.language(), 'javascript')
parser = Parser()
parser.set_language(JAVASCRIPT_LANGUAGE)

def get_string_from_code(node, lines):
    line_start = node.start_point[0]
    line_end = node.end_point[0]
    char_start = node.start_point[1]
    char_end = node.end_point[1]
    if line_start != line_end:
        return ' '.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
    else:
        return lines[line_start][char_start:char_end]

def traverse(node, lines):
    if node.child_count == 0:
        return get_string_from_code(node, lines)
    else:
        code_list = []
        for n in node.children:
            code_list.append(traverse(n, lines))
        return ' '.join(code_list)

def process_code(code):
    lines = code.split('\n')
    tree = parser.parse(bytes(code, "utf8"))
    return traverse(tree.root_node, lines)

# Define a function to generate summary
def generate_summary(code):
    # Process code and generate tokenized input
    tokenized_code = process_code(code)
    input_text = "Generate a natural language summary for the following JavaScript code:\n" + tokenized_code
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(model.device)
    
    # Generate summary
    summary_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Example code
code = """import React from 'react';
ReactDOM.render(
  <h1>Hello, world!</h1>,
  document.getElementById('root')
);"""

# Generate summary
summary = generate_summary(code)
print(summary)
