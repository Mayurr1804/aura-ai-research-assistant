def merge_papers(arxiv_papers, semantic_papers):

    merged_results = []

    for a_paper in arxiv_papers:

        title = a_paper["title"].lower()

        matched_paper = None

        for s_paper in semantic_papers:

            s_title = s_paper["title"].lower()

            if (
                title in s_title
                or s_title in title
            ):
                matched_paper = s_paper
                break

        merged_paper = {

            "title": a_paper["title"],

            "authors": a_paper["authors"],

            "year": (
                matched_paper["year"]
                if matched_paper else None
            ),

            "summary": a_paper["summary"],

            "pdf_url": a_paper["pdf_url"],

            "citations": (
                matched_paper["citations"]
                if matched_paper else 0
            ),

            "paper_url": (
                matched_paper["url"]
                if matched_paper else None
            )
        }

        merged_results.append(merged_paper)

    # IMPORTANT
    # Agar Arxiv fail ho gaya aur Semantic Scholar me papers hain

    if not merged_results and semantic_papers:

        for paper in semantic_papers:

            merged_results.append({

                "title": paper["title"],

                "authors": paper["authors"],

                "year": paper["year"],

                "summary": "",

                "pdf_url": None,

                "citations": paper["citations"],

                "paper_url": paper["url"]
            })

    return merged_results