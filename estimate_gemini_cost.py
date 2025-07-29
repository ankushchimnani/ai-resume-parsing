import tiktoken
import sys

# Gemini 1.5 Flash pricing (per 1,000 tokens)
INPUT_PRICE_PER_1K = 0.075
OUTPUT_PRICE_PER_1K = 0.30

# Your prompt (edit as needed)
prompt = """
You are a highly-skilled resume parser that strictly follows output formatting rules.
Assume the current year is 2025.
Your task is to analyze the provided resume and extract its information precisely into the JSON format defined below. Do not deviate from this schema.
... (add your full prompt here) ...
"""

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    if len(sys.argv) != 3:
        print("Usage: python estimate_gemini_cost.py <resume.txt> <sample_output.json>")
        sys.exit(1)
    resume_path = sys.argv[1]
    output_path = sys.argv[2]
    resume_text = read_file(resume_path)
    output_json = read_file(output_path)

    enc = tiktoken.get_encoding("cl100k_base")
    prompt_tokens = len(enc.encode(prompt + resume_text))
    output_tokens = len(enc.encode(output_json))

    input_cost = (prompt_tokens / 1000) * INPUT_PRICE_PER_1K
    output_cost = (output_tokens / 1000) * OUTPUT_PRICE_PER_1K
    total_cost = input_cost + output_cost

    print(f"Prompt+Resume tokens: {prompt_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Input cost: ${input_cost:.4f}")
    print(f"Output cost: ${output_cost:.4f}")
    print(f"Total estimated cost for this resume: ${total_cost:.4f}")

if __name__ == "__main__":
    main() 