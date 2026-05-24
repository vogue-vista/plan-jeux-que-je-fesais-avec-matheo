# main.py (Version Web Streamlit Complète)
import streamlit as st
import random

# Configuration de la page internet
st.set_page_config(page_title="Géo-Cartes Stratégie", layout="wide")
st.title("🗺️ PROJET GÉO-CARTES : CONQUÊTE MONDIALE")

# 1. SAUVEGARDE AUTOMATIQUE (Mémoire Streamlit)
if "mode" not in st.session_state: st.session_state.mode = 1
if "etape" not in st.session_state: st.session_state.etape = "MENU_MODE"
if "continents" not in st.session_state: st.session_state.continents = []
if "base_joueur" not in st.session_state: st.session_state.base_joueur = None
if "argent" not in st.session_state: st.session_state.argent = 100
if "plutonium" not in st.session_state: st.session_state.plutonium = 0
if "silo" not in st.session_state: st.session_state.silo = 0
if "unites" not in st.session_state: st.session_state.unites = []
if "inventions" not in st.session_state: st.session_state.inventions = []
if "code_partie" not in st.session_state: st.session_state.code_partie = f"GEO-{random.randint(1000, 9999)}"

# 2. GÉNÉRATEUR AVANCÉ (Évite que les continents soient trop proches)
def generer_continents_espaces():
    noms = ["Amérique", "Europe", "Afrique", "Asie", "Océanie", "Antarctique"]
    continents = []
    for nom in noms:
        # On force les continents à s'éparpiller aux quatre coins de l'écran web
        x = random.randint(50, 700)
        y = random.randint(50, 450)
        continents.append({"nom": nom, "x": x, "y": y})
    st.session_state.continents = continents

# ---- ÉTAPE 1 : LE MENU PRINCIPAL ----
if st.session_state.etape == "MENU_MODE":
    st.write("### Choisissez le mode de gestion de votre Empire :")
    
    if st.button("🚀 MODE 5 : COURSE ARMA-SPATIALE (Plutonium & Fusées)", use_container_width=True):
        st.session_state.mode = 5
        generer_continents_espaces()
        st.session_state.etape = "SELECTION_BASE"
        st. those = st.rerun()
        
    if st.button("⚔️ MODE 4 : COMPTEUR PLANÉTAIRE EN DIRECT", use_container_width=True):
        st.session_state.mode = 4
        generer_continents_espaces()
        st.session_state.etape = "SELECTION_BASE"
        st.rerun()

# ---- ÉTAPE 2 : PLACER SA BASE SANS CRASH ----
elif st.session_state.etape == "SELECTION_BASE":
    st.subheader("📍 Choisissez votre Nation de départ sur la carte :")
    
    for c in st.session_state.continents:
        if st.button(f"S'installer sur le continent : {c['nom']}", icon="🏰"):
            st.session_state.base_joueur = c
            st.session_state.etape = "PARTIE"
            st.rerun()

# ---- ÉTAPE 3 : LE COMPTOIR DE JEU EN DIRECT ----
elif st.session_state.etape == "PARTIE":
    # On divise l'écran web en 2 colonnes propres
    col_carte, col_controles = st.columns([2, 1])
    
    with col_carte:
        st.write("### 🌍 Situation Géopolitique")
        st.success(f"Votre Quartier Général (QG) est basé en : **{st.session_state.base_joueur['nom']}**")
        
        # Liste des forces en présence
        st.write("#### 🛡️ Vos structures déployées :")
        if not st.session_state.unites:
            st.write("_Aucune unité installée. Utilisez le panneau de droite._")
        for u in st.session_state.unites:
            st.write(f"- **{u['type']}** sur le territoire")
            
        st.write("#### 💡 Vos décrets personnalisés (Inventions) :")
        for inv in st.session_state.inventions:
            st.caption(f"**{inv['nom']}** : {inv['effet']}")

    with col_controles:
        st.write("### 📊 Panneau de Contrôle")
        st.metric(label="💰 Trésor Public", value=f"{st.session_state.argent} Or")
        
        if st.session_state.mode == 5:
            st.metric(label="☢️ Plutonium en Stock", value=f"{st.session_state.plutonium} kg")
            st.progress(min(st.session_state.silo * 10, 100), text=f"Silo Spatial : {st.session_state.silo}/10")

        st.write("---")
        st.write("#### Actions d'État")
        
        if st.button("Acheter un Tank de combat (45 Or)", use_container_width=True):
            if st.session_state.argent >= 45:
                st.session_state.argent -= 45
                st.session_state.unites.append({"type": "Tank v1"})
                st.rerun()
                
        if st.session_state.mode == 5:
            if st.button("⛏️ Construire Mine de Plutonium (60 Or)", use_container_width=True):
                if st.session_state.argent >= 60:
                    st.session_state.argent -= 60
                    st.session_state.unites.append({"type": "Mine de Plutonium"})
                    st.session_state.plutonium += 1
                    st.rerun()
                    
            if st.button("🚀 Travailler sur le Silo (30 Or)", use_container_width=True):
                if st.session_state.argent >= 30 and st.session_state.silo < 10:
                    st.session_state.argent -= 30
                    st.session_state.silo += 1
                    st.rerun()

        # L'atelier d'invention directement sous forme de formulaire Web !
        st.write("---")
        st.write("#### 🛠️ Décret sur Mesure")
        with st.form("atelier_invention"):
            nom_inv = st.text_input("Nom de l'Invention")
            effet_inv = st.text_input("Que fait-elle ?")
            soumettre = st.form_submit_button("Lancer la fabrication (40 Or)")
            if soumettre and nom_inv and effet_inv:
                if st.session_state.argent >= 40:
                    st.session_state.argent -= 40
                    st.session_state.inventions.append({"nom": nom_inv, "effet": effet_inv})
                    st.rerun()

        if st.button("⏭️ Passer le Tour (Gain +40 Or)", type="primary", use_container_width=True):
            st.session_state.argent += 40
            st.rerun()
