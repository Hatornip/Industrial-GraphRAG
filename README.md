# 🕸️ Industrial GraphRAG: Intelligent Impact Analyzer

> **"Bridging the gap between Unstructured Documentation and Deterministic Engineering."**

![Status](https://img.shields.io/badge/Status-POC_Functional-green)
![Tech](https://img.shields.io/badge/Tech-NLP_%2B_Graph_Theory-blue)

## 📋 Context & Problem

In complex Product Line Engineering (PLE), a minor design change on a component can trigger a disastrous "Ripple Effect" on the entire system.

- **LLMs alone (ChatGPT)** are unreliable for this: they hallucinate connections.
- **Standard Databases** lack the flexibility to trace deep transitive dependencies.

**This project proposes a Neuro-Symbolic Architecture combining the semantic power of NLP with the mathematical rigor of Graph Theory.**

## 🚀 Key Features

1.  **Smart Ingestion (NLP):** Automatically extracts technical triplets (_Subject -> Relation -> Object_) from raw documentation using Natural Language Processing.
2.  **Knowledge Graph Construction:** Dynamically builds a Directed Graph using `NetworkX`.
3.  **Deterministic Impact Analysis:** Uses Depth-First Search (DFS) algorithms to identify 100% of impacted components without hallucination.
4.  **Interactive Dashboard:** A `Streamlit` interface allowing engineers to simulate design changes and visualize risks in real-time.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Graph Engine:** NetworkX
- **NLP:** spaCy (scalable to Llama 3)
- **Visualization:** Matplotlib / Pyplot
- **Data:** Pandas

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/hatornip/Industrial-GraphRAG.git
cd Industrial-GraphRAG

# 2. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 3. Run the app
streamlit run app.py
```
