from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_paper_summary(title: str, abstract: str):

    prompt = f"""
You are an expert research assistant.

Explain the following research paper clearly for beginners.

Paper Title:
{title}

Abstract:
{abstract}

Explain:

1. Problem
2. Background
3. Method
4. Experiments / datasets
5. Results
6. Limitations
7. Importance
"""

    response = client.chat.completions.create(

        model="llama3-70b-8192",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.3
    )

    return response.choices[0].message.content