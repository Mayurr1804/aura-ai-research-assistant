import networkx as nx


def build_citation_graph(papers):

    G = nx.DiGraph()

    for paper in papers:

        title = paper.get("title")

        citations = paper.get("citations", 0)

        G.add_node(title, citations=citations)

    # simple linking for visualization
    for i in range(len(papers)-1):

        source = papers[i+1]["title"]
        target = papers[i]["title"]

        G.add_edge(source, target)

    nodes = []
    edges = []

    for node in G.nodes(data=True):

        nodes.append({
            "id": node[0],
            "citations": node[1]["citations"]
        })

    for edge in G.edges():

        edges.append({
            "source": edge[0],
            "target": edge[1]
        })

    return {
        "nodes": nodes,
        "edges": edges
    }