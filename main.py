# main.py (Version Finale avec IA Groq et Anti-Bug Web)
import streamlit as st
import random
from groq import Groq

st.set_page_config(page_title="Géo-Cartes Stratégie", layout="wide")
st.title("Monde 🌍 PROJET GÉO-CARTES : CONQUÊTE MONDIALE")

# INITIALISATION DE L'IA GROQ VIA LES SECRETS SÉCURISÉS
client_groq = None
if "GROQ_API_KEY" in st.secrets:
    client_groq = Groq(api_key=st.secrets["GROQ_API_KEY"])

# INITIALISATION DE LA MÉMOIRE SÉCURISÉE
if "mode" not in st.session_state: st.session_state.mode = 1
if "etape" not in st.session_state: st.session_state.etape = "MENU_MODE"
if "continents" not in st.session_state: st.session_state.continents = []
if "base_joueur" not in st.session_state: st.session_state.base_joueur = None
if "argent" not in st.session_state: st.session_state.argent = 100
if "plutonium" not in st.session_state: st.session_state.plutonium = 0
if "silo" not in st.session_state: st.session_state.silo = 0
if "unites" not in st.session_state: st.session_state.unites = []
if "inventions" not in st.session_state: st.session_state.inventions = []
if "reponse_ia" not in st.session_state: st.session_state.reponse_ia = ""

def generer_continents_espaces():
    noms = ["Amérique", "Europe", "Afrique", "Asie", "Océanie", "Antarctique"]
    continents = []
    for nom in noms:
        x = random.randint(50, 700)
        y = random.randint(50, 450)
        continents.append({"nom": nom, "x": x, "y": y})
    st.session_state.continents = continents

# ---- ÉTAPE 1 : LE MENU PRINCIPAL ----
if st.session_state.etape == "MENU_MODE":
    with st.container(key="zone_menu"):
        st.write("### Choisissez le mode de gestion de votre Empire :")
        
        if st.button("🚀 MODE 5 : COURSE ARMA-SPATIALE (Plutonium & Fusées)", key="btn_menu_mode_5", use_container_width=True):
            st.session_state.mode = 5
            generer_continents_espaces()
            st.session_state.etape = "SELECTION_BASE"
            st.rerun()
            
        if st.button("⚔️ MODE 4 : COMPTEUR PLANÉTAIRE EN DIRECT", key="btn_menu_mode_4", use_container_width=True):
            st.session_state.mode = 4
            generer_continents_espaces()
            st.session_state.etape = "SELECTION_BASE"
            st.rerun()

# ---- ÉTAPE 2 : PLACER SA BASE ----
elif st.session_state.etape == "SELECTION_BASE":
    with st.container(key="zone_selection_base"):
        st.subheader("📍 Choisissez votre Nation de départ sur la carte :")
        
        for c in st.session_state.continents:
            if st.button(f"S'installer sur le continent : {c['nom']}", key=f"choix_base_{c['nom']}_unique", icon="🏰"):
                st.session_state.base_joueur = c
                st.session_state.etape = "PARTIE"
                st.rerun()

# ---- ÉTAPE 3 : LE JEU ----
elif st.session_state.etape == "PARTIE":
    with st.container(key="zone_partie_principale"):
        col_carte, col_controles = st.columns(2)
        
        with col_carte:
            st.write("### 🌍 Situation Géopolitique")
            if st.session_state.base_joueur:
                st.success(f"Votre Quartier Général (QG) est basé en : **{st.session_state.base_joueur['nom']}**")
            
            st.write("#### 🛡️ Vos structures déployées :")
            if not st.session_state.unites:
                st.write("_Aucune unité installée._")
            for u in st.session_state.unites:
                st.write(f"- **{u['type']}** sur le territoire")
                
            st.write("#### 💡 Vos décrets validés :")
            if not st.session_state.inventions:
                st.write("_Aucun décret actif._")
            for inv in st.session_state.inventions:
                st.caption(f"📜 **{inv['nom']}** : {inv['effet']}")

            # ZONE DE DIALOGUE AVEC L'IA GROQ
            if st.session_state.reponse_ia:
                st.write("---")
                st.info(f"🤖 **Rapport du Conseil de l'IA (Groq) :**\n\n{st.session_state.reponse_ia}")

        with col_controles:
            st.write("### 📊 Panneau de Contrôle")
            st.metric(label="💰 Trésor Public", value=f"{st.session_state.argent} Or")
            
            if st.session_state.mode == 5:
                st.metric(label="☢️ Plutonium en Stock", value=f"{st.session_state.plutonium} kg")
                st.progress(min(st.session_state.silo * 10, 100), text=f"Silo Spatial : {st.session_state.silo}/10")

            st.write("---")
            st.write("#### Actions d'État")
            
            if st.button("Acheter un Tank de combat (45 Or)", key="btn_action_tank", use_container_width=True):
                if st.session_state.argent >= 45:
                    st.session_state.argent -= 45
                    st.session_state.unites.append({"type": "Tank v1"})
                    st.rerun()
                    
            if st.session_state.mode == 5:
                if st.button("⛏️ Construire Mine de Plutonium (60 Or)", key="btn_action_mine", use_container_width=True):
                    if st.session_state.argent >= 60:
                        st.session_state.argent -= 60
                        st.session_state.unites.append({"type": "Mine de Plutonium"})
                        st.session_state.plutonium += 1
                        st.rerun()
                        
                if st.button("🚀 Travailler sur le Silo (30 Or)", key="btn_action_silo", use_container_width=True):
                    if st.session_state.argent >= 30 and st.session_state.silo < 10:
                        st.session_state.argent -= 30
                        st.session_state.silo += 1
                        st.rerun()

            st.write("---")
            st.write("#### 🛠️ Décret / Invention sur Mesure (Géré par Groq)")
            with st.form("atelier_invention", clear_on_submit=True):
                nom_inv = st.text_input("Nom de l'Invention", key="input_nom_invention")
                effet_inv = st.text_input("Que fait-elle ? (Effet libre)", key="input_effet_invention")
                soumettre = st.form_submit_button("Soumettre à l'IA (-40 Or)", use_container_width=True)
                
                if soumettre and nom_inv and effet_inv:
                    if st.session_state.argent >= 40:
                        st.session_state.argent -= 40
                        st.session_state.inventions.append({"nom": nom_inv, "effet": effet_inv})
                        
                        # APPEL À L'API GROQ SI LA CLÉ EST CONFIGURÉE
                        if client_groq:
                            try:
                                prompt = f"Dans un jeu de stratégie mondiale, le joueur invente l'unité ou loi '{nom_inv}' avec l'effet suivant : '{effet_inv}'. En tant qu'IA adverse ou conseiller d'État, réponds en deux courtes phrases maximum de manière immersive pour dire comment ton camp réagit stratégiquement ou si cette arme est un danger."
                                completion = client_groq.chat.completions.create(
                                    model="llama3-8b-8192",
                                    messages=[{"role": "user", "content": prompt}]
                                )
                                st.session_state.reponse_ia = completion.choices[0].message.content
                            except Exception as e:
                                st.session_state.reponse_ia = f"Erreur de connexion à l'IA : {str(e)}"
                        else:
                            st.session_state.reponse_ia = f"Invention '{nom_inv}' validée ! (Ajoute ta clé API Groq dans les Advanced Settings de Streamlit pour activer les réponses de l'IA)."
                        st.rerun()

            if st.button("⏭️ Passer le Tour (Gain +40 Or)", key="btn_passer_tour_global", type="primary", use_container_width=True):
                st.session_state.argent += 40
                st.rerun()
