import requests


def search_huggingface_datasets(query):

    url = f"https://huggingface.co/api/datasets?search={query}"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    results = []

    for item in data[:5]:

        dataset_name = item.get("id")

        results.append({
            "name": dataset_name,
            "source": "HuggingFace",
            "link": f"https://huggingface.co/datasets/{dataset_name}"
        })

    return results



def search_kaggle_datasets(query):

    # Kaggle public API search endpoint (simplified)

    url = f"https://www.kaggle.com/api/v1/datasets/list?search={query}"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    results = []

    for item in data[:5]:

        dataset_name = item.get("title")

        dataset_ref = item.get("ref")

        results.append({
            "name": dataset_name,
            "source": "Kaggle",
            "link": f"https://www.kaggle.com/datasets/{dataset_ref}"
        })

    return results



def find_datasets(query):

    hf_results = search_huggingface_datasets(query)

    kaggle_results = search_kaggle_datasets(query)

    combined = hf_results + kaggle_results

    return combined