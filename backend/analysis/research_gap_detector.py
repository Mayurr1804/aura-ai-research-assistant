from groq import Groq
from dotenv import load_dotenv
import os

# import summary generator
from backend.analysis.summary_generator import generate_paper_summary

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def detect_research_gaps(papers):

    """
    papers = ranked papers list
    each paper contains:
    {
        "title": "...",
        "summary": "..."
    }
    """

    # use top 10 papers
    papers = papers[:10]

    paper_summaries = []

    # STEP 1: generate summaries
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

    # STEP 3: detect research gaps
    prompt = f"""
You are an expert research scientist.

Using the research paper summaries below, identify
the major research gaps in this field.

A research gap means something that current research
has not solved or areas where further research is needed.

Paper Summaries:
{summaries_text}

Return:

1. Key research gaps
2. Possible future research directions

Provide 4–6 bullet points.
"""

    response = client.chat.completions.create(

        model="llama3-70b-8192",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.3
    )

    return response.choices[0].message.content