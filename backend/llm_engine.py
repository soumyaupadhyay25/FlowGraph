import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# =========================
# 🔹 SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
You are a query translator.

Return JSON with:
- entity: Order, Delivery, Invoice
- intent: high_value, leakage, trace
- filters: optional

Rules:
- Extract numeric conditions:
  "above 1000", "greater than 1000" → ">1000"
  "below 500", "less than 500" → "<500"
- If unrelated → {"reject": true}
- Output ONLY JSON

Examples:

User: show orders above 1500
Output: {"entity": "Order", "intent": "high_value", "filters": {"amount": ">1500"}}

User: show orders less than 300
Output: {"entity": "Order", "intent": "high_value", "filters": {"amount": "<300"}}

User: show leakage
Output: {"entity": "Order", "intent": "leakage"}

User: trace order 740571
Output: {"entity": "Order", "intent": "trace"}
"""
# =========================
# 🔹 CALL OLLAMA
# =========================
def call_llm(user_input):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": SYSTEM_PROMPT + "\nUser: " + user_input,
            "stream": False
        }
    )

    output = response.json()["response"]
    print("RAW LLM:", output)

    return output


# =========================
# 🔹 INTERPRET QUERY
# =========================
def interpret_query(user_input):

    try:
        llm_output = call_llm(user_input)

        match = re.search(r"\{.*\}", llm_output, re.DOTALL)

        if not match:
            return {"entity": "Order", "intent": "high_value", "filters": {}}

        query = json.loads(match.group(0))

        # 🚫 Guardrail
        if query.get("reject"):
            return {"reject": True}

        # Normalize entity
        entity = query.get("entity", "Order").strip().lower()

        if entity.endswith("s"):
            entity = entity[:-1]

        entity = entity.capitalize()

        if entity not in ["Order", "Delivery", "Invoice"]:
            entity = "Order"

        query["entity"] = entity

        query["raw"] = user_input.lower()

        # Ensure intent exists
        if "intent" not in query:
            query["intent"] = "high_value"

        # ✅ FIX: Ensure filters exists (CORRECT PLACE)
        if "filters" not in query:
            query["filters"] = {}

        print("FINAL QUERY:", query)

        return query

    except Exception as e:
        print("❌ LLM Error:", e)
        return {"entity": "Order", "intent": "high_value", "filters": {}}

        
# =========================
# 🔹 MAIN PIPELINE
# =========================
def generate_response(user_input, execute_query):

    # Step 1: interpret query
    query = interpret_query(user_input)

    if query.get("reject"):
        return {
            "answer": "This system is designed to answer questions related to the dataset only.",
            "data": []
        }

    # Step 2: fetch data from graph
    results = execute_query(query)

    # Step 3: send data BACK to LLM for explanation
    context = json.dumps(results[:20])  # limit for prompt

    prompt = f"""
You are a data analyst.

User asked:
{user_input}

Here is the dataset:
{context}

Answer the question using ONLY this data.
If data is empty, say no results found.

Give clear natural language answer.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    final_answer = response.json()["response"]

    return {
        "answer": final_answer,
        "data": results[:20]
    }
    # 🚫 Guardrail response
    if query.get("reject"):
        return {
            "answer": "This system is designed to answer questions related to the provided dataset only.",
            "data": []
        }

    # ✅ Execute query (from app.py)
    results = execute_query(query)

    return {
        "answer": f"Found {len(results)} results",
        "data": results[:20]
    }