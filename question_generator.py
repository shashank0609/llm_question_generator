import fitz  # PyMuPDF
import openai
import os
import random
import pandas as pd  # For structured output
from prompt import DOMAIN_CONTEXT, QUESTION_GENERATION_PROMPT


class PDFQuestionGenerator:
    def __init__(
        self, azure_openai_key, azure_openai_endpoint, deployment_name, api_version
    ):
        self.client = openai.AzureOpenAI(
            api_key=azure_openai_key,
            base_url=azure_openai_endpoint,
            api_version=api_version,
        )
        self.deployment_name = deployment_name

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from the entire PDF and returns a structured format with page numbers."""
        text_per_page = {}
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            text = doc[page_num].get_text("text")
            if text.strip():
                text_per_page[page_num + 1] = text.strip()  # Page numbers start from 1
        return text_per_page

    def generate_questions(self, extracted_text, num_questions=5):
        """Generates questions using Azure OpenAI GPT models based on extracted text."""
        prompt = QUESTION_GENERATION_PROMPT.format(
            domain_context=DOMAIN_CONTEXT,
            extracted_text=extracted_text,
            num_questions=num_questions,
        )

        response = self.client.completions.create(
            model=self.deployment_name, prompt=prompt, temperature=0.7, max_tokens=500
        )

        questions = response.choices[0].text.strip().split("\n")
        return [q for q in questions if q]  # Filter out empty responses

    def generate_questions_from_pdf(self, pdf_path, num_questions=5):
        """Extracts text and generates questions distributed across the document."""
        extracted_texts = self.extract_text_from_pdf(pdf_path)
        total_pages = len(extracted_texts)

        if total_pages == 0:
            print(f"⚠️ No text found in {pdf_path}. Skipping...")
            return []

        # Select pages randomly but ensure even distribution
        selected_pages = random.sample(extracted_texts.keys(), min(5, total_pages))
        combined_text = " ".join([extracted_texts[p] for p in selected_pages])
        questions = self.generate_questions(combined_text, num_questions)

        return [
            {"Question": q, "Page Reference": p}
            for q, p in zip(questions, selected_pages)
        ]

    def generate_questions_from_multiple_pdfs(self, pdf_paths, num_questions=5):
        """Processes multiple PDFs and generates questions for each."""
        results = {}
        for pdf_path in pdf_paths:
            questions = self.generate_questions_from_pdf(pdf_path, num_questions)
            results[pdf_path] = questions
        return results
