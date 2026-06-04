import arxiv
import time


def search_arxiv(query: str, max_results: int = 5):
    """
    Search research papers from ArXiv
    """

    try:

        # arxiv rate limit se bachne ke liye
        time.sleep(2)

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers = []

        for result in search.results():

            paper = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "published": str(result.published.date()),
                "summary": result.summary,
                "pdf_url": result.pdf_url
            }

            papers.append(paper)

        return papers

    except Exception as e:

        print(f"Arxiv Error: {e}")

        return []