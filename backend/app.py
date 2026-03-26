from flask import Flask, jsonify, send_file, request
from graph import G, build_graph
from query import orders_not_invoiced, high_value_orders
from llm_engine import generate_response
import os
import re



def execute_query(query_json):
    raw = query_json.get("raw", "").lower()
    intent = query_json.get("intent")
    filters = query_json.get("filters", {})

    print("RAW:", raw)
    print("INTENT FROM LLM:", intent)

    
    if any(word in raw for word in ["product"]):
        intent = "product_analysis"

    elif any(word in raw for word in ["leak", "not billed", "not invoiced", "broken", "incomplete"]):
        intent = "leakage"

    elif any(word in raw for word in ["trace", "flow"]):
        intent = "trace"

    elif any(word in raw for word in ["above", "below", "greater", "less"]):
        intent = "high_value"

    print("FINAL INTENT:", intent)

   
    if intent == "high_value":

        match = re.search(r"\d+", raw)

        if match:
            value = float(match.group())

            if "below" in raw or "less" in raw:
                print("FILTER:", "<", value)
                return high_value_orders(value, "<")
            else:
                print("FILTER:", ">", value)
                return high_value_orders(value, ">")

        return high_value_orders()

   
    if intent == "leakage":
        print("RUNNING LEAKAGE FUNCTION")
        return orders_not_invoiced()

    if intent == "trace":
        from query import trace_order_flow
        return trace_order_flow(query_json)

    
    if intent == "product_analysis":
        from query import product_with_most_invoices
        return product_with_most_invoices()

    return []


app = Flask(__name__)

build_graph()


@app.route("/")
def home():
    return send_file("../frontend/index.html")


@app.route("/graph")
def show_graph():
    file_path = os.path.join(os.getcwd(), "graph.html")

    if not os.path.exists(file_path):
        return "❌ graph.html not found. Run graph_viz.py first."

    return send_file(file_path)


@app.route("/high-value")
def high_value():
    data = high_value_orders()
    return jsonify({
        "count": len(data),
        "orders": data[:20]
    })


@app.route("/leakage")
def leakage():
    data = orders_not_invoiced()
    return jsonify({
        "count": len(data),
        "orders": data[:20]
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    result = generate_response(user_input, execute_query)

    return jsonify(result)



if __name__ == "__main__":
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)