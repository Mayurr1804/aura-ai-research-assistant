from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Retrieval modules
from backend.retrieval.arxiv_search import search_arxiv
from backend.retrieval.semantic_scholar import search_semantic_scholar
from backend.retrieval.merge_sources import merge_papers

# Ranking module
from backend.ranking.paper_ranker import rank_papers

# Dataset modules
from backend.datasets.pdf_parser import extract_text_from_pdf
from backend.datasets.text_chunker import split_text_into_chunks
from backend.datasets.dataset_agent import detect_datasets_from_chunk
from backend.datasets.dataset_availability_checker import check_dataset_availability
#email genrrator
from backend.agents.email_generator import generate_dataset_email
#dataset finder
from backend.datasets.dataset_finder import find_datasets
from backend.analysis.summary_generator import generate_paper_summary
from backend.analysis.literature_review_generator import generate_literature_review
from backend.analysis.research_gap_detector import detect_research_gaps
from backend.analysis.research_roadmap_generator import generate_research_roadmap
from backend.analysis.citation_graph import build_citation_graph
from backend.agents.research_agent import run_research_agent
app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------
# Home Endpoint
# ------------------------------

@app.get("/")
def home():
    return {"message": "AURA AI Research Assistant API is running"}


# ------------------------------
# ArXiv Search
# ------------------------------

@app.get("/search")
def search_papers(query: str, limit: int = 5):

    papers = search_arxiv(query, limit)

    return {
        "query": query,
        "results": papers
    }


# ------------------------------
# Semantic Scholar Search
# ------------------------------

@app.get("/semantic-search")
def semantic_search(query: str, limit: int = 5):

    papers = search_semantic_scholar(query, limit)

    return {
        "query": query,
        "results": papers
    }


# ------------------------------
# Multi Source + Ranking
# ------------------------------

@app.get("/merged-search")
def merged_search(query: str, limit: int = 5):

    arxiv_papers = search_arxiv(query, limit)

    semantic_papers = search_semantic_scholar(query, limit)

    merged = merge_papers(arxiv_papers, semantic_papers)

    ranked = rank_papers(query, merged)

    return {
        "query": query,
        "total_results": len(ranked),
        "best_base_paper": ranked[0],
        "results": ranked
    }


# ------------------------------
# Dataset Detection from Paper
# ------------------------------

@app.post("/paper-datasets")
def paper_datasets(pdf_url: str):

    # extract full paper text
    paper_text = extract_text_from_pdf(pdf_url)

    # split paper into chunks
    chunks = split_text_into_chunks(paper_text)

    detected_datasets = set()

    for chunk in chunks:

        result = detect_datasets_from_chunk(chunk)

        if isinstance(result, list):
            for d in result:
                detected_datasets.add(d)

    availability = check_dataset_availability(paper_text)

    return {
        "datasets_detected": list(detected_datasets),
        "dataset_availability": availability
    }
@app.post("/generate-email")
def generate_email(
    paper_title: str,
    author_name: str,
    availability: str,
    user_instruction: str = None
):

    if availability not in ["request_required", "private"]:

        return {
            "message": "Dataset is public. Email not required."
        }

    email = generate_dataset_email(
        paper_title,
        author_name,
        user_instruction
    )

    return {
        "generated_email": email
    }
@app.post("/dataset-search")
def dataset_search(description: str):

    datasets = find_datasets(description)

    return {
        "query": description,
        "datasets_found": datasets
    }
@app.post("/paper-summary")
def paper_summary(title: str, abstract: str):

    summary = generate_paper_summary(title, abstract)

    return {
        "title": title,
        "summary": summary
    }
# ------------------------------
# Literature Review Generator
# ------------------------------

@app.get("/literature-review")

def literature_review(query: str):

    # Step 1: search papers
    arxiv_papers = search_arxiv(query, 10)
    semantic_papers = search_semantic_scholar(query, 10)

    # Step 2: merge papers
    merged = merge_papers(arxiv_papers, semantic_papers)

    # Step 3: rank papers
    ranked = rank_papers(query, merged)

    # Step 4: take top papers
    top_papers = ranked[:5]

    # Step 5: generate literature review
    review = generate_literature_review(top_papers)

    return {
        "query": query,
        "top_papers": top_papers,
        "literature_review": review
    }
# ------------------------------
# Research Gap Detection
# ------------------------------

@app.get("/research-gaps")

def research_gaps(query: str):

    # search papers
    arxiv_papers = search_arxiv(query, 15)
    semantic_papers = search_semantic_scholar(query, 15)

    # merge sources
    merged = merge_papers(arxiv_papers, semantic_papers)

    # rank papers
    ranked = rank_papers(query, merged)

    # detect gaps using top 10 papers
    gaps = detect_research_gaps(ranked)

    return {
        "query": query,
        "research_gaps": gaps
    }
# ------------------------------
# Research Roadmap Generator
# ------------------------------

@app.get("/research-roadmap")

def research_roadmap(query: str):

    # search papers
    arxiv_papers = search_arxiv(query, 15)
    semantic_papers = search_semantic_scholar(query, 15)

    # merge
    merged = merge_papers(arxiv_papers, semantic_papers)

    # rank
    ranked = rank_papers(query, merged)

    # generate roadmap
    roadmap = generate_research_roadmap(query, ranked)

    return {
        "query": query,
        "research_roadmap": roadmap
    }
# ------------------------------
# Citation Graph
# ------------------------------

@app.get("/citation-graph")

def citation_graph(query: str):

    arxiv_papers = search_arxiv(query, 10)
    semantic_papers = search_semantic_scholar(query, 10)

    merged = merge_papers(arxiv_papers, semantic_papers)

    ranked = rank_papers(query, merged)

    graph = build_citation_graph(ranked[:10])

    return {
        "query": query,
        "citation_graph": graph
    }

@app.get("/research-assistant")

def research_assistant(query: str):

    return run_research_agent(query)
