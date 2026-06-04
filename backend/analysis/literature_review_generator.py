from groq import Groq
from dotenv import load_dotenv
import os

# import summary generator
from backend.analysis.summary_generator import generate_paper_summary

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_literature_review(papers):

    """
    papers = ranked papers list
    each paper contains:
    {
        "title": "...",
        "summary": "..."
    }
    """

    # take top 5 papers
    papers = papers[:5]

    paper_summaries = []

    # STEP 1: generate summary for each paper
    for paper in papers:

        title = paper.get("title", "")
        abstract = paper.get("summary", "")

        summary = generate_paper_summary(title, abstract)

        paper_summaries.append(summary)

    # STEP 2: combine summaries
    summaries_text = ""

    for i, summary in enumerate(paper_summaries):

        summaries_text += f"""
Paper {i+1} Summary:
{summary}

"""

    # STEP 3: generate literature review
    prompt = f"""
You are an expert research scientist.

Using the paper summaries below, write a literature review
describing the current research trends in this field.

Focus on:

• common research approaches
• main methodologies
• important findings
• limitations in existing work

Paper Summaries:
{summaries_text}

Write a structured literature review in 3–4 paragraphs.
Do NOT summarize each paper separately.
Instead synthesize the overall research trends.
"""

    response = client.chat.completions.create(

        model="llama3-70b-8192",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.3
    )

    return response.choices[0].message.content