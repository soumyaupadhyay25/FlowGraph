from graph import G


# =========================
# 1. ORDERS NOT INVOICED
# =========================
def orders_not_invoiced():
    results = []

    for node in G.nodes:
        if G.nodes[node].get("type") != "Order":
            continue

        deliveries = list(G.successors(node))

        invoiced = False

        for d in deliveries:
            invoices = list(G.successors(d))
            if invoices:
                invoiced = True
                break

        if not invoiced:
            results.append(node)

    return results


# =========================
# 2. HIGH VALUE ORDERS
# =========================
def high_value_orders(threshold=500, operator=">"):
    results = []

    for node in G.nodes:
        if G.nodes[node].get("type") != "Order":
            continue

        total_amount = 0

        deliveries = list(G.successors(node))

        for d in deliveries:
            invoices = list(G.successors(d))

            for inv in invoices:
                amt = G.nodes[inv].get("amount", 0)

                try:
                    amt = float(amt)
                except:
                    amt = 0

                total_amount += amt

        # ✅ STRICT FILTER (FIXED INDENTATION)
        if operator == ">" and total_amount <= threshold:
            continue

        if operator == "<" and total_amount >= threshold:
            continue

        results.append({
            "order": node,
            "amount": total_amount
        })

    return results


# =========================
# 3. TRACE ORDER FLOW
# =========================
def trace_order_flow(query_json):
    results = []

    for node in G.nodes:
        if G.nodes[node].get("type") != "Order":
            continue

        flow = ["Order"]

        deliveries = list(G.successors(node))

        if deliveries:
            flow.append("Delivery")

            invoices = []
            for d in deliveries:
                invoices.extend(list(G.successors(d)))

            if invoices:
                flow.append("Invoice")

        results.append({
            "order": node,
            "flow": " → ".join(flow)
        })

    return results[:10]