import os
import requests

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_semantic_scholar(query, limit=5):

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,citationCount,url"
    }

    headers = {}

    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

    if api_key:
        headers["x-api-key"] = api_key

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=20
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:

            print("Semantic Scholar Error:", response.text)

            return []

        data = response.json()

        papers = []

        for paper in data.get("data", []):

            papers.append({
                "title": paper.get("title"),
                "authors": [
                    a.get("name")
                    for a in paper.get("authors", [])
                ],
                "year": paper.get("year"),
                "citations": paper.get("citationCount", 0),
                "url": paper.get("url")
            })

        return papers

    except Exception as e:

        print(f"Semantic Scholar Error: {e}")

        return []