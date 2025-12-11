import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import spacy

st.set_page_config(page_title="Industrial GraphRAG", layout="wide")

@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

def extract_relations(text):
    G = nx.DiGraph()
    doc = nlp(text)
    
    relations_found = []
    
    for sent in doc.sents:
        subj = None
        obj = None
        verb = "impacts"
        
        for token in sent:
            if "subj" in token.dep_:
                subj = token.text
            if "obj" in token.dep_:
                obj = token.text
            if token.pos_ == "VERB":
                verb = token.lemma_
        
        if subj and obj:
            G.add_edge(subj, obj, label=verb)
            relations_found.append(f"{subj} --[{verb}]--> {obj}")
            
    return G, relations_found

def get_impact_path(G, source):
    if source not in G:
        return []
    return list(nx.dfs_preorder_nodes(G, source=source))

# --- INTERFACE UTILISATEUR ---

st.title("🤖 Intelligent Impact Analyzer (POC)")
st.markdown("""
Cet outil démontre comment l'IA peut aider à la **gestion de configuration (PLE)**.  
Il extrait la connaissance d'une documentation technique pour prédire les impacts d'un changement de design.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Documentation Technique")
    st.info("Copiez ici les règles de conception ou le manuel technique.")
    
    default_text = """
    The Battery powers the Engine.
    The Engine drives the Wheels.
    The Wheels support the Chassis.
    The Chassis holds the PassengerSeat.
    The CoolingSystem cools the Engine.
    The Chipset controls the CoolingSystem.
    """
    
    text_input = st.text_area("Base de connaissance", value=default_text, height=200)
    
    if st.button("🚀 Analyser & Construire le Graphe"):
        G, relations = extract_relations(text_input)
        st.session_state['graph'] = G
        st.session_state['relations'] = relations
        st.success(f"Graphe construit ! {len(relations)} relations identifiées.")

with col2:
    st.subheader("2. Visualisation & Simulation")
    
    if 'graph' in st.session_state:
        G = st.session_state['graph']
        
        nodes = list(G.nodes())
        if nodes:
            target = st.selectbox("Quel composant souhaitez-vous modifier ?", nodes)
            
            impacted_nodes = get_impact_path(G, target)
            
            if len(impacted_nodes) > 1:
                st.error(f"⚠️ ALERTE CRITIQUE : Modifier '{target}' va impacter {len(impacted_nodes)-1} autres composants !")
                st.write("Chaine de propagation :", " → ".join(impacted_nodes))
            else:
                st.success(f"✅ Modification de '{target}' sûre. Aucun impact en cascade détecté.")

            fig, ax = plt.subplots(figsize=(10, 6))
            pos = nx.spring_layout(G, seed=42, k=0.5)
            
            normal_nodes = [n for n in G.nodes() if n not in impacted_nodes]
            nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, node_color='#e0e0e0', node_size=2000)
            
            if impacted_nodes:
                nx.draw_networkx_nodes(G, pos, nodelist=impacted_nodes, node_color='#ff4b4b', node_size=2500)
                nx.draw_networkx_nodes(G, pos, nodelist=[target], node_color='#333333', node_size=2500)

            nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
            nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, width=1.5)
            
            edge_labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')
            
            st.pyplot(fig)
            
    else:
        st.warning("Veuillez d'abord générer le graphe depuis la colonne de gauche.")

