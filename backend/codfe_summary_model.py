from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjs
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from server import tokenizer, model

# # # Load tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_large_code_documentation_generation_javascript_multitask_finetune", skip_special_tokens=True)
# model = AutoModelForSeq2SeqLM.from_pretrained("SEBIS/code_trans_t5_large_code_documentation_generation_javascript_multitask_finetune").to('cuda' if torch.cuda.is_available() else 'cpu')

# Define a function for batch processing
def batch_process_code(code_list, batch_size=8):
    tokenized_inputs = tokenizer(code_list, padding=True, truncation=True, return_tensors="pt")
    outputs = []
    for i in range(0, len(code_list), batch_size):
        batch_inputs = {k: v[i:i+batch_size] for k, v in tokenized_inputs.items()}
        batch_outputs = model.generate(**batch_inputs, max_new_tokens=512)  # Adjust max_new_tokens as needed
        outputs.extend(batch_outputs)
    return outputs

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

# Example code
code = """import React from 'react';
ReactDOM.render(
  <h1>Hello, world!</h1>,
  document.getElementById('root')
);"""

# Process code and generate summary
tokenized_code = process_code(code)
summary = tokenizer.decode(batch_process_code([tokenized_code])[0], skip_special_tokens=True)
print(summary)
