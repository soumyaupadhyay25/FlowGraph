import networkx as nx
from ingest import build_graph_from_data

G = nx.DiGraph()

def build_graph():
    G.clear()
    build_graph_from_data(G)

    print("✅ Graph ready")