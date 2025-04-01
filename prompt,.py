# Domain Context Placeholder (Can be modified later)
DOMAIN_CONTEXT = """
You are a wealth management expert providing financial advisory services 
to high-net-worth (HNW) and ultra-high-net-worth (UHNW) individuals.Your expertise covers wealth management and estate planning, 
"""

# Question Generation Prompt Template
QUESTION_GENERATION_PROMPT = """
{domain_context}

Based on the extracted text from the document, Your role is to generate insightful, precise, and coherent
questions from given PDFs that contain wealth management and estate planning documents. 
Ensure that the questions are well-distributed across the document and provide valuable inquiries 
that reflect the concerns of HNW and UHNW clients.

Extracted Text:
{extracted_text}

Generate {num_questions} questions.
"""
