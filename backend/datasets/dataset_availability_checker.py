import re


def check_dataset_availability(paper_text):

    text = paper_text.lower()

    # detect links
    link_pattern = r"https?://\S+"
    links = re.findall(link_pattern, paper_text)

    # Case 1 — dataset link found
    if links:
        return {
            "availability": "public",
            "dataset_link": links[0]
        }

    # Case 2 — dataset available upon request
    if "available upon request" in text:
        return {
            "availability": "request_required"
        }

    # Case 3 — dataset not publicly available
    if "not publicly available" in text:
        return {
            "availability": "private"
        }

    # Case 4 — authors cannot share data
    if "do not have permission to share" in text:
        return {
            "availability": "not_shareable"
        }

    return {
        "availability": "unknown"
    }