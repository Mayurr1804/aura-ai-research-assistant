from groq import Groq
from dotenv import load_dotenv
import os

from backend.analysis.literature_review_generator import generate_literature_review
from backend.analysis.research_gap_detector import detect_research_gaps
from backend.datasets.dataset_finder import find_datasets

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_research_roadmap(query, ranked_papers):

    if not ranked_papers:
        return "No research papers found for this query."

    top5 = ranked_papers[:5]
    top10 = ranked_papers[:10]

    base_paper = ranked_papers[0]

    literature_review = generate_literature_review(top5)

    research_gaps = detect_research_gaps(top10)

    datasets = find_datasets(query)

    dataset_text = ""

    for d in datasets[:3]:

        name = d.get("name", "Unknown Dataset")
        source = d.get("source", "Unknown Source")
        link = d.get("link", "No link available")

        dataset_text += f"""
Dataset: {name}
Source: {source}
Link: {link}
"""

    prompt = f"""
You are an expert research scientist.

Create a detailed research roadmap for the following problem.

Research Problem:
{query}

Current Research Overview:
{literature_review}

Identified Research Gaps:
{research_gaps}

Base Paper for Guidance:
Title: {base_paper.get("title")}
Authors: {base_paper.get("authors")}
Year: {base_paper.get("year")}

Available Datasets:
{dataset_text}

Generate a structured roadmap containing:

1. Research Problem
2. Current Research Overview
3. Identified Research Gaps
4. Base Paper for Guidance
5. Proposed Research Direction
6. Dataset Strategy
   - include dataset name
   - source
   - direct link
   - explain how it can be used
7. Methodology Plan
8. Experimental Setup
9. Evaluation Metrics
10. Expected Contributions
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content