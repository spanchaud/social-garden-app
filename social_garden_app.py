import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Social Garden", page_icon="🌱")
st.title("Social Garden 🌱")
st.write("Bienvenue dans votre espace Social Garden.")

# --- 2. LE CERVEAU DE VOTRE APP (IMPORTANT !) ---
# C'est ici que vous devez coller les instructions que vous aviez dans AI Studio.
# Copiez votre texte entre les trois guillemets ci-dessous.
SYSTEM_PROMPT = """
Tu es Social Garden, un assistant expert en jardinage social et réseautage.
Ton but est d'aider l'utilisateur à cultiver ses relations professionnelles.
Réponds toujours de manière bienveillante, encourageante et structurée.
Si l'utilisateur pose une question hors sujet, ramène-le doucement au jardinage social.
"""

# --- 3. CONNEXION CLÉ API ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Erreur de clé API. Vérifiez vos 'Secrets' dans Streamlit.")
    st.stop()

# --- 4. CONFIGURATION DU MODÈLE ---
# On utilise 'gemini-pro' qui est plus stable pour éviter l'erreur 404
model = genai.GenerativeModel('gemini-pro') 

# --- 5. INTERFACE DE DISCUSSION ---

# Initialiser l'historique si c'est la première fois
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": [SYSTEM_PROMPT]}, # On injecte la personnalité au début cachée
        {"role": "model", "parts": ["Bien compris. Je suis prêt à agir en tant que Social Garden."]}
    ]

# Afficher les anciens messages (sauf le prompt système caché)
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0])

# Zone de saisie pour l'utilisateur
if prompt := st.chat_input("Posez votre question à Social Garden..."):
    # 1. Afficher le message de l'utilisateur
    st.chat_message("user").markdown(prompt)
    
    # 2. L'ajouter à l'historique
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    
    # 3. Demander la réponse à l'IA
    try:
        chat = model.start_chat(history=st.session_state.messages)
        response = chat.send_message(prompt)
        
        # 4. Afficher la réponse
        with st.chat_message("model"):
            st.markdown(response.text)
            
        # 5. Sauvegarder la réponse
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
        
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")
