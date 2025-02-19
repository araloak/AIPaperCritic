from utils import *


def get_paper_summary(paper_text):
    prompt = get_paper_summary_prompt + paper_text
    return chat_with_reviewer(prompt)

def analyze_research_motivation(paper_text):
    prompt = analyze_research_motivation_prompt + paper_text
    return chat_with_reviewer(prompt)

def analyze_method_motivation(paper_text):
    prompt = analyze_method_motivation_prompt + paper_text
    return chat_with_reviewer(prompt)

def analyze_method_correctness(paper_text):
    prompt = analyze_method_correctness_prompt + paper_text
    return chat_with_reviewer(prompt)

def analyze_method_effectiveness(paper_text):
    prompt = analyze_method_effectiveness_prompt + paper_text
    return chat_with_reviewer(prompt)

def generate_questions(paper_text):
    prompt = generate_questions_prompt + paper_text
    return chat_with_reviewer(prompt)

def analyze_writing(paper_text):
    prompt = analyze_language_prompt + paper_text
    return chat_with_reviewer(prompt)

def generate_review(paper_text,file_path):
    # Combine all sections into a single text while preserving section headers
    prompt_prefix = "# 论文内容\n"
    # Get individual components
    summary = get_paper_summary(prompt_prefix +paper_text)
    problem_analysis = analyze_research_motivation(prompt_prefix + paper_text)
    method_motivation_analysis = analyze_method_motivation(prompt_prefix + paper_text)
    method_correctness_analysis = analyze_method_correctness(prompt_prefix + paper_text)
    method_effectiveness_analysis = analyze_method_effectiveness(prompt_prefix + paper_text)
    questions = generate_questions(prompt_prefix +  paper_text + "\n# Method Motivation Analysis\n" + method_motivation_analysis + "\n# Method Effectiveness Analysis\n" + method_effectiveness_analysis)
    #writing_analysis = analyze_writing(prompt_prefix + paper_text)
    
    # Compile the review in markdown format
    review = f"""# Paper Review Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Summary
{summary}

---

# Research Motivation Analysis
{problem_analysis}

---

# Methodology Motivation Analysis
{method_motivation_analysis}

---

# Methodology Correctness Analysis
{method_correctness_analysis}

---

# Methodology Effectiveness Analysis
{method_effectiveness_analysis}

---

# Questions
{questions}

"""
    
    # Save the review
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'../data/papers/{os.path.basename(file_path)}_paper_review_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(review)
    
    return filename

def main():
    parser = argparse.ArgumentParser(description='file path')
    parser.add_argument('--file_path', type=str, default='../data/papers/example.pdf', help='Specify the file path')
    args = parser.parse_args()

    file_path = args.file_path

    if file_path.endswith(".pdf"):
        paper_text = pdf2md(file_path)
        file_path = file_path.replace(".pdf",".md")
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            paper_text = f.read()

    review_file = generate_review(paper_text, file_path)
    print(f"Review has been saved to: {review_file}")

if __name__ == "__main__":
    main()