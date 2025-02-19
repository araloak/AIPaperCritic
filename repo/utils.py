from volcenginesdkarkruntime import Ark
from openai import OpenAI
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption, DocumentConverter, ImageFormatOption, PowerpointFormatOption, WordFormatOption, ExcelFormatOption, HTMLFormatOption
from datetime import datetime

import os, re, argparse

# Doubao config
DOUBAO_API_KEY = "YOUR API KEY"  
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DOUBAO_MODEL_NAME = "YOUR MODEL NAME"
# OpenAI config
API_KEY = "YOUR API KEY"
BASE_URL = "YOUR BASE URL"
MODEL_NAME = "YOUR MODEL NAME"

reviewer_role = "openai"  # select from ["doubao", "openai"]
language = "cn" # select from ["en", "cn"]
docling_model_path = "../model/AI-ModelScope/docling-models"

reviewer_system_prompt_path = "../data/prompts/"+language+"/reviewer_system_prompt.txt"
reviewer_system_prompt = open(reviewer_system_prompt_path, encoding='utf8').read().strip()

get_paper_summary_prompt_path = "../data/prompts/"+language+"/get_paper_summary.txt"
get_paper_summary_prompt = open(get_paper_summary_prompt_path, encoding='utf8').read().strip()

analyze_research_motivation_prompt_path = "../data/prompts/"+language+"/analyze_research_motivation.txt"
analyze_research_motivation_prompt = open(analyze_research_motivation_prompt_path, encoding='utf8').read().strip()

analyze_method_motivation_prompt_path = "../data/prompts/"+language+"/analyze_method_motivation.txt"
analyze_method_motivation_prompt = open(analyze_method_motivation_prompt_path, encoding='utf8').read().strip()

analyze_method_correctness_prompt_path = "../data/prompts/"+language+"/analyze_method_correctness.txt"
analyze_method_correctness_prompt = open(analyze_method_correctness_prompt_path, encoding='utf8').read().strip()

analyze_method_effectiveness_prompt_path = "../data/prompts/"+language+"/analyze_method_effectiveness.txt"
analyze_method_effectiveness_prompt = open(analyze_method_effectiveness_prompt_path, encoding='utf8').read().strip()

analyze_language_prompt_path = "../data/prompts/"+language+"/analyze_language.txt"
analyze_language_prompt = open(analyze_language_prompt_path, encoding='utf8').read().strip()

generate_questions_prompt_path = "../data/prompts/"+language+"/generate_questions.txt"
generate_questions_prompt = open(generate_questions_prompt_path, encoding='utf8').read().strip()

def chat_with_doubao(prompt):
    client = Ark(
        base_url=DOUBAO_BASE_URL,
        api_key=DOUBAO_API_KEY
    )
    try:
        messages = [
            {
                "role": "system",
                "content": reviewer_system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        print("----- standard request -----")
        completion = client.chat.completions.create(
            model=DOUBAO_MODEL_NAME,
            messages=messages,
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error {str(e)}")

def chat_with_openai(prompt):
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    try:
        messages = [
            {
                "role": "system",
                "content": reviewer_system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]


        print("----- standard request -----")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.6,

        )

        # # stream mode
        # full_message = ""
        # for chunk in response:
        #     chunk_message = chunk.choices[0].delta.content
        #     full_message+=chunk_message
        #     print(chunk_message, end='', flush=True)
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error: {str(e)}")

def chat_with_reviewer(prompt):
    if reviewer_role == 'doubao':
        return chat_with_doubao(prompt)
    if reviewer_role == 'openai':
        return chat_with_openai(prompt)


def remove_line_numbers(text): #去除review版本pdf中带有的行号
    # 定义正则表达式模式，匹配行号（三位数字，后面跟零个或多个空白字符，然后是换行符）
    pattern = r'\d{3}\s*\n+'
    # 使用 re.sub 函数将匹配到的行号替换为空字符串
    result = re.sub(pattern, '', text)
    return result

def pdf2md(pdf_path):
    filename = os.path.basename(pdf_path)
    md_path = "../data/papers/" + filename.replace(".pdf", ".md")

    # 配置pdf模型，设置Docling模型的路径
    pdf_pipeline_options = PdfPipelineOptions(artifacts_path=docling_model_path)

    # 转换模型
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_pipeline_options),
            InputFormat.IMAGE: ImageFormatOption(pipeline_options=pdf_pipeline_options),
            InputFormat.PPTX: PowerpointFormatOption(pipeline_options=pdf_pipeline_options),
            InputFormat.DOCX: WordFormatOption(pipeline_options=pdf_pipeline_options),
            InputFormat.XLSX: ExcelFormatOption(pipeline_options=pdf_pipeline_options),
            InputFormat.HTML: HTMLFormatOption(pipeline_options=pdf_pipeline_options)
        }
    )
    result = converter.convert(pdf_path)
    paper_text = result.document.export_to_markdown()
    paper_text = remove_line_numbers(paper_text)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(paper_text)

    return paper_text

def pdf2md_v2(pdf_path): #docling无法使用时考虑使用markitdown
    from markitdown import MarkItDown

    md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
    result = md.convert(pdf_path)
    filename = os.path.basename(pdf_path)
    md_path = "../data/papers/" + filename.replace(".pdf", ".md")

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(result.text_content)
    paper_text = remove_line_numbers(result.text_content)

    return paper_text


def parse_paper_md(file_path): #TODO: 论文按section划分，不同问题只输入相关section
    """Parse a markdown paper file into sections based on ## headers"""
    sections = {}
    current_section = None
    current_content = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            if line.strip().startswith('## '):
                # When we find a new section, save the previous section if it exists
                if current_section:
                    sections[current_section] = ''.join(current_content).strip()
                # Start new section
                current_section = line.strip()[3:].lower()  # Remove '## ' and convert to lowercase
                current_content = []
            else:
                if current_section:
                    current_content.append(line)

        # Don't forget to save the last section
        if current_section:
            sections[current_section] = ''.join(current_content).strip()

        return sections

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error parsing markdown file: {str(e)}")
        return None