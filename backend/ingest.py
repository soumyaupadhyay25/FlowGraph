import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)   # go one level up


# =========================
# LOAD JSONL FOLDER
# =========================
def load_jsonl_folder(folder_path):
    all_data = []

    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return all_data

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    all_data.append(json.loads(line))
                except:
                    continue

    print(f"✅ Loaded {len(all_data)} from {folder_path}")
    return all_data


# =========================
# BUILD GRAPH
# =========================
def build_graph_from_data(G):

    # 🔥 CORRECT INDENTATION STARTS HERE
    delivery_items = load_jsonl_folder(
        os.path.join(ROOT_DIR, "data/outbound_delivery_items")
    )

    invoice_items = load_jsonl_folder(
        os.path.join(ROOT_DIR, "data/billing_document_items")
    )

    invoice_headers = load_jsonl_folder(
        os.path.join(ROOT_DIR, "data/billing_document_headers")
    )

    # =========================
    # NODES
    # =========================
    for row in delivery_items:
        order = row.get("referenceSdDocument")
        delivery = row.get("deliveryDocument")

        if order:
            G.add_node(f"Order_{order}", type="Order")

        if delivery:
            G.add_node(f"Delivery_{delivery}", type="Delivery")

    for row in invoice_items:
        delivery = row.get("referenceSdDocument") or row.get("deliveryDocument")
        invoice = row.get("billingDocument")

        if delivery:
            G.add_node(f"Delivery_{delivery}", type="Delivery")

        if invoice:
            G.add_node(f"Invoice_{invoice}", type="Invoice")

    # =========================
    # INVOICE AMOUNT
    # =========================
    for row in invoice_headers:
        invoice = row.get("billingDocument")

        if not invoice:
            continue

        try:
            amount = float(row.get("totalNetAmount") or 0)
        except:
            amount = 0

        G.add_node(
            f"Invoice_{invoice}",
            type="Invoice",
            amount=amount
        )

    # =========================
    # EDGES
    # =========================
    for row in delivery_items:
        o = row.get("referenceSdDocument")
        d = row.get("deliveryDocument")

        if o and d:
            G.add_edge(f"Order_{o}", f"Delivery_{d}")

    for row in invoice_items:
        d = row.get("referenceSdDocument") or row.get("deliveryDocument")
        i = row.get("billingDocument")

        if d and i:
            G.add_edge(f"Delivery_{d}", f"Invoice_{i}")

    # =========================
    # 🔥 PROPAGATE AMOUNT (IMPORTANT FIX)
    # =========================
    for node in G.nodes():

        if G.nodes[node].get("type") == "Invoice":
            amount = G.nodes[node].get("amount", 0)

            for delivery in G.predecessors(node):
                for order in G.predecessors(delivery):
                    if G.nodes[order].get("type") == "Order":
                        # 🔥 accumulate instead of overwrite
                        G.nodes[order]["amount"] = G.nodes[order].get("amount", 0) + amount

    print("🔥 Graph built")
    print("Nodes:", len(G.nodes))
    print("Edges:", len(G.edges))