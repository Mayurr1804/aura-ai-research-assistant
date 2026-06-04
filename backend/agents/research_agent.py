from backend.retrieval.arxiv_search import search_arxiv
from backend.retrieval.semantic_scholar import search_semantic_scholar
from backend.retrieval.merge_sources import merge_papers

from backend.ranking.paper_ranker import rank_papers

from backend.analysis.summary_generator import generate_paper_summary
from backend.analysis.literature_review_generator import generate_literature_review
from backend.analysis.research_gap_detector import detect_research_gaps
from backend.analysis.research_roadmap_generator import generate_research_roadmap
from backend.analysis.citation_graph import build_citation_graph

from backend.datasets.pdf_parser import extract_text_from_pdf
from backend.datasets.text_chunker import split_text_into_chunks
from backend.datasets.dataset_agent import detect_datasets_from_chunk
from backend.datasets.dataset_availability_checker import check_dataset_availability
from backend.datasets.dataset_finder import find_datasets

from backend.agents.email_generator import generate_dataset_email


def run_research_agent(query):

   
    arxiv_papers = search_arxiv(query, 5)
    semantic_papers = search_semantic_scholar(query, 5)

    merged = merge_papers(arxiv_papers, semantic_papers)

    ranked = rank_papers(query, merged)

    if not ranked:
        return {"message": "No research papers found."}

  
    top5 = ranked[:5]
    top10 = ranked[:10]

    base_paper = ranked[0]

    
    paper_summaries = []

    for paper in top5:

        summary = generate_paper_summary(
            paper["title"],
            paper["summary"]
        )

        paper_summaries.append({
            "title": paper["title"],
            "summary": summary,
            "pdf_url": paper.get("pdf_url"),
            "paper_url": paper.get("paper_url"),
            "year": paper.get("year"),
            "citations": paper.get("citations")
        })


    literature_review = generate_literature_review(top5)

   

    research_gaps = detect_research_gaps(top10)


    detected_datasets = []
    dataset_email = None
    dataset_availability = None

    pdf_url = base_paper.get("pdf_url")

    if pdf_url:

        try:

            paper_text = extract_text_from_pdf(pdf_url)

            chunks = split_text_into_chunks(paper_text)

            dataset_set = set()

            for chunk in chunks:

                result = detect_datasets_from_chunk(chunk)

                if isinstance(result, list):

                    for d in result:
                        dataset_set.add(d)

            detected_datasets = list(dataset_set)

            dataset_availability = check_dataset_availability(paper_text)

            if dataset_availability in ["request_required", "private"]:

                dataset_email = generate_dataset_email(
                    base_paper.get("title"),
                    base_paper.get("authors")[0]
                )

        except Exception:
            pass

  
    alternative_datasets = find_datasets(query)



    roadmap = generate_research_roadmap(query, ranked)

   
    citation_graph = build_citation_graph(top10)

  

    return {

        "query": query,

        "best_base_paper": {
            "title": base_paper.get("title"),
            "authors": base_paper.get("authors"),
            "year": base_paper.get("year"),
            "citations": base_paper.get("citations"),
            "pdf_url": base_paper.get("pdf_url"),
            "paper_url": base_paper.get("paper_url")
        },

        "top_papers": top5,

        "paper_summaries": paper_summaries,

        "literature_review": literature_review,

        "research_gaps": research_gaps,

        "datasets_detected": detected_datasets,

        "dataset_availability": dataset_availability,

        "dataset_request_email": dataset_email,

        "alternative_datasets": alternative_datasets[:5],

        "research_roadmap": roadmap,

        "citation_graph": citation_graph
    }