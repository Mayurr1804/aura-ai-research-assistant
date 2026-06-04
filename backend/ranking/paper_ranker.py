from sentence_transformers import SentenceTransformer, util
import numpy as np
from datetime import datetime

model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_papers(query, papers):

    summaries = [paper["summary"] for paper in papers]

    query_embedding = model.encode(query, convert_to_tensor=True)
    paper_embeddings = model.encode(summaries, convert_to_tensor=True)

    similarity_scores = util.cos_sim(query_embedding, paper_embeddings)[0].cpu().numpy()

    current_year = datetime.now().year

    ranked_results = []

    for i, paper in enumerate(papers):

        citation_score = np.log1p(paper["citations"]) if paper["citations"] else 0

        recency_score = 1 / (1 + (current_year - paper["year"])) if paper["year"] else 0

        final_score = (
            0.5 * similarity_scores[i] +
            0.3 * citation_score +
            0.2 * recency_score
        )

        paper["ranking_score"] = float(final_score * 100)

        ranked_results.append(paper)

    ranked_results.sort(key=lambda x: x["ranking_score"], reverse=True)

    return ranked_results