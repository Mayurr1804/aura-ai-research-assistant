from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_dataset_email(paper_title, author_name, user_instruction=None):

    base_prompt = f"""
You are helping a researcher write a polite email to request access to a dataset used in a research paper.

Paper title:
{paper_title}

Author:
{author_name}

Write a professional email asking for access to the dataset used in the paper.
Keep it polite and concise.
"""

    if user_instruction:
        base_prompt += f"\nAdditional user instruction: {user_instruction}"

    response = client.chat.completions.create(

        model="llama3-70b-8192",

        messages=[
            {"role": "user", "content": base_prompt}
        ],

        temperature=0.4
    )

    return response.choices[0].message.content