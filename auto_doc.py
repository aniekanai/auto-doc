import os
import ast
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load your OpenAI API key from .env
load_dotenv()
client = OpenAI()

def extract_functions_from_file(file_path):
    with open(file_path, "r") as f:
        file_content = f.read()

    tree = ast.parse(file_content)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_code = ast.get_source_segment(file_content, node)
            functions.append(func_code)
    return functions

def generate_docstring(function_code):
    prompt = f"""
You are a senior software engineer. Here is a Python function:

{function_code}

Generate a clean, Google-style docstring explaining its purpose, parameters, return type, and a short usage example.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You generate professional, clean, Google-style Python docstrings."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: python auto_doc.py <python_file_to_document>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        sys.exit(1)

    functions = extract_functions_from_file(file_path)
    if not functions:
        print("No functions found in this file.")
        sys.exit(0)

    for idx, func in enumerate(functions, 1):
        print(f"\n{'='*50}\nFunction {idx}:\n{func}\n")
        docstring = generate_docstring(func)
        print(f"Generated Docstring:\n{docstring}\n{'='*50}")

if __name__ == "__main__":
    main()
