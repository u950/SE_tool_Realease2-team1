import subprocess
import json

def analyze_js_metrics(filename):
    # Run ESLint on the JavaScript file to generate code metrics
    eslint_output = subprocess.run(['eslint', '--format=json', filename], capture_output=True, text=True)

    # Parse ESLint output to extract code metrics
    eslint_json = json.loads(eslint_output.stdout)
    metrics = eslint_json[0]['metrics']

    print(f"Metrics for {filename}:")
    print(f"  Lines of Code (LOC): {metrics['lines']}")
    print(f"  Source Lines of Code (SLOC): {metrics['sloc']}")
    print(f"  Comments: {metrics['comments']}")
    print(f"  Single-line Comments: {metrics['singleCommentLines']}")
    print(f"  Block Comments: {metrics['blockCommentLines']}")
    print(f"  Empty Lines: {metrics['emptyLines']}")

if __name__ == "__main__":
    filename = '/backend/code_summary_model.py'
    analyze_js_metrics(filename)
