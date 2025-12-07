import streamlit as st
import google.generativeai as genai
import os

# --- Configuration de la page ---
st.set_page_config(page_title="Social Garden", page_icon="🌱")

st.title("Social Garden 🌱")
st.write("Bienvenue dans votre espace Social Garden. Posez votre question ci-dessous.")

# --- Gestion de la Clé API ---
# On va chercher la clé dans les "coffre-forts" de Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Erreur : La clé API est manquante. Avez-vous configuré les secrets ?")
    st.stop()

# --- Configuration du Modèle ---
# On utilise le modèle standard. Vous pouvez changer 'gemini-pro' si besoin.
model = genai.GenerativeModel('gemini-1.5-flash') 

# --- Interface Utilisateur ---
user_input = st.text_area("Votre message :", height=150)

if st.button("Envoyer au jardin 🚀"):
    if user_input:
        with st.spinner("Le jardinier réfléchit..."):
            try:
                response = model.generate_content(user_input)
                st.markdown("### Réponse :")
                st.write(response.text)
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
    else:
        st.warning("Veuillez écrire quelque chose avant d'envoyer.")
