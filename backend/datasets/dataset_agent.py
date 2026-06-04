from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detect_datasets_from_chunk(chunk):

    prompt = f"""
You are reading a research paper.

Identify all datasets mentioned in the text below.

Return dataset names as a JSON list.

Example:
["ImageNet", "CIFAR-10"]

Text:
{chunk}
"""

    response = client.chat.completions.create(

        model="llama3-70b-8192",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0
    )

    return response.choices[0].message.content