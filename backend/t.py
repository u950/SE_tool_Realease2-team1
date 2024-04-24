import code_summary_model as csm

code = """import React from 'react'"""
summarizer = csm.CodeSummarizer()
summary = summarizer.summarize_code(code)
print(summary)