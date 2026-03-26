from pyvis.network import Network
from graph import G, build_graph

build_graph()   # 🔥 THIS CALL IS MUST
# =========================
# 🔥 INIT NETWORK
# =========================
net = Network(
    height="100vh",
    width="100%",
    directed=True,
    bgcolor="#020617",   # darker, premium look
    font_color="white"
)

# =========================
# 🔹 ADD NODES (WITH LEVELS)
# =========================
for node, data in G.nodes(data=True):

    node_type = data.get("type", "Unknown")

    # 🎯 TYPE STYLING + HIERARCHY LEVEL
    if node_type == "Order":
        color = "#22c55e"
        size = 18
        level = 1

    elif node_type == "Delivery":
        color = "#f97316"
        size = 16
        level = 2

    elif node_type == "Invoice":
        color = "#ef4444"
        size = 17
        level = 3

    else:
        color = "#3b82f6"
        size = 12
        level = 0

    net.add_node(
        str(node),
        label=str(node),
        color=color,
        size=size,
        level=level,   # 🔥 KEY FOR STRUCTURE
        title=f"""
        <div style="padding:10px">
        <b>Type:</b> {node_type}<br>
        <b>ID:</b> {node}<br>
        <b>Amount:</b> {data.get("amount", "N/A")}
        </div>
        """
    )

# =========================
# 🔹 ADD EDGES
# =========================
for u, v, data in G.edges(data=True):
    net.add_edge(
        str(u),
        str(v),
        title=data.get("relation", ""),
        color="#64748b",
        arrows="to",
        width=1
    )

# =========================
# 🔥 GRAPH OPTIONS (NO CRASH JSON)
# =========================
net.set_options("""
{
  "physics": {
    "enabled": true,
    "barnesHut": {
      "gravitationalConstant": -3000,
      "centralGravity": 0.3,
      "springLength": 140,
      "damping": 0.09
    }
  },
  "interaction": {
    "hover": true,
    "zoomView": true,
    "dragView": true
  },
  "nodes": {
    "shape": "dot",
    "font": {
      "size": 14,
      "color": "white"
    }
  },
  "edges": {
    "smooth": true,
    "color": "#64748b"
  }
}
""")
# =========================
# 💾 SAVE GRAPH (IMPORTANT FIX)
# =========================
net.save_graph("graph.html")

print(f"✅ Graph generated with {len(G.nodes())} nodes and {len(G.edges())} edges")