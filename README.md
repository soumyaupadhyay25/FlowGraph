# 🚀 FlowGraph AI

FlowGraph AI is an intelligent graph-based system that visualizes relationships between business entities (like products, orders, deliveries) and enables users to query insights using natural language powered by AI.

It combines **graph analytics + backend processing + LLM intelligence** into a single interactive web application.

---

## 🌐 Live Demo

👉 https://flowgraph.onrender.com

---

## 🧠 Overview

FlowGraph AI transforms structured data into a **network graph** and allows users to:

* Visualize relationships between entities
* Detect anomalies like broken flows
* Ask questions in natural language
* Get AI-generated insights

---

## ✨ Features

* 📊 Interactive graph visualization (nodes & edges)
* 🔍 AI-powered query system
* ⚡ Real-time backend processing
* 🧩 Modular architecture (graph + query + LLM)
* 🌐 Deployed on cloud (Render)

---

## 🏗️ Architecture

```
User (Browser UI)
        │
        ▼
Frontend (HTML + JS)
        │
        ▼
Flask Backend (app.py)
        │
        ├───────────────┬───────────────────┐
        ▼               ▼                   ▼
 Graph Engine      Query Engine        LLM Engine
 (graph.py)       (query_engine.py)   (llm_engine.py)
        │               │                   │
        ▼               ▼                   ▼
   NetworkX Graph   Business Logic     OpenAI API
        │                                   │
        ▼                                   ▼
   Graph JSON Response              AI Response (text)
        │                                   │
        └───────────────┬───────────────────┘
                        ▼
                Flask Response (API)
                        │
                        ▼
                Frontend Visualization
```

---

## 📁 Project Structure

```
FlowGraph/
│
├── backend/
│   ├── app.py                # Flask server (main entry point)
│   ├── graph.py              # Graph creation using NetworkX
│   ├── graph_viz.py          # Graph visualization prep
│   ├── ingest.py             # Data ingestion pipeline
│   ├── llm_engine.py         # LLM API integration
│   ├── query_engine.py       # Query logic layer
│   ├── requirements.txt      # Python dependencies
│   ├── Procfile              # Deployment config (Render)
│   └── data/                 # JSON dataset (nodes & relations)
│
├── frontend/                 # UI (HTML, JS, CSS)
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

* **Backend:** Flask (Python)
* **Graph Processing:** NetworkX
* **Frontend:** HTML, JavaScript
* **AI Integration:** OpenAI API
* **Deployment:** Render
* **Dev Tunneling:** ngrok

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/soumyaupadhyay25/FlowGraph.git
cd FlowGraph/backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variable

```bash
OPENAI_API_KEY=your_api_key_here
```

### 4. Run locally

```bash
python app.py
```

### 5. (Optional) Use ngrok

```bash
ngrok http 5000
```

---

## 🔌 API Endpoints

### `/graph`

* Returns graph data (nodes + edges)

### `/chat`

* Accepts user query
* Returns AI-generated response

---

## 🧪 Example Queries

* Identify incomplete sales orders
* Find broken delivery flows
* Detect anomalies in order lifecycle

---

## ⚠️ Notes

* Queries may take slightly longer due to:

  * Free tier hosting (Render)
  * External API calls (LLM)
  * First request may be slow (cold start)

---

## 🛠️ Known Limitations

* No caching (queries recompute every time)
* Depends on external API availability
* Large datasets may slow graph rendering

---

## 🚧 Future Improvements

* ⚡ Query optimization & caching
* 🎯 Better UI/UX
* 🔍 Advanced graph filtering
* 📈 Analytics dashboard
* 🔐 Authentication system

---

## 👤 Author

**Soumya Upadhyay**


---

## 🧾 Additional Info

> Queries might take a little longer to run as this project uses free-tier services.
> Please test with a bit of patience for best results.
