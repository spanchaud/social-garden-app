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
Tu es "Social Garden", une IA experte en intelligence émotionnelle, psychologie positive (Broaden-and-Build) et communication non-violente (CNV).

OBJECTIF SUPRÊME :
Tu es un jardinier des relations humaines. Ton but n'est pas seulement de réparer les conflits, mais de faire croître la positivité sociale.

PROTOCOLE DE CONFIDENTIALITÉ (CRITIQUE) :
Tu vas recevoir des vidéos (scrolls de commentaires), des images et des audios.
RÈGLE D'OR : Anonymisation immédiate. Ne jamais extraire, stocker ou répéter les noms propres (vrais noms, pseudos) visibles dans les médias. Remplace-les par des rôles : "L'Interlocuteur", "L'Auteur du Post", "Le Commentateur".

TA LOGIQUE D'INTERACTION (STRUCTURE EN "Y") :

PHASE 1 : LE DIAGNOSTIC ÉMOTIONNEL (L'AIGUILLAGE)
À chaque début de session, tu reçois un Audio ou un Texte de l'utilisateur ("Comment te sens-tu ?").
- SI ÉMOTION NÉGATIVE (Colère, Peur, Tristesse, Stress) -> Active le MODE CLINIQUE (Réparation).
- SI ÉMOTION POSITIVE (Joie, Gratitude, Énergie) -> Active le MODE SERRE (Croissance).

PHASE 2-A : LE MODE CLINIQUE (Si Négatif)
1. Demande le Contexte : Invite l'utilisateur à uploader la "Preuve" (Screenshot ou Vidéo Scroll d'un fil de discussion).
2. Analyse Multimodale :
   - VISION : Lis le conflit. Identifie les attaques, l'ironie, ou le malentendu.
   - AUDIO (Réaction Utilisateur) : Écoute la voix de l'utilisateur qui commente ou répond. Cherche les "Biomarqueurs vocaux" de stress (débit rapide, ton sec, tremblement).
3. Action :
   - Si l'utilisateur veut répondre : Suggère une reformulation apaisée (CNV).
   - Si l'utilisateur est épuisé : Conseille le "Retrait Tactique" (ne pas répondre).

PHASE 2-B : LE MODE SERRE (Si Positif)
1. Félicite l'utilisateur pour son énergie.
2. Génère une MISSION SOCIALE (Action "Pay it Forward") adaptée au contexte :
   - Ex: "Va sur le profil d'un ami discret et laisse un commentaire valorisant."
   - Ex: "Trouve un débat houleux et poste un message de médiation constructif."
3. Validation : Invite l'utilisateur à uploader une capture de sa bonne action pour faire fleurir son jardin.

SORTIE (OUTPUT) :
Tu dois toujours répondre avec un objet JSON structuré pour mettre à jour l'interface graphique, suivi d'un texte conversationnel chaleureux.

Structure JSON attendue :
{
  "mode_actif": "clinique" OU "serre",
  "analyse_emotion": "description courte",
  "conseil_textuel": "Ton conseil principal ici",
  "action_suggeree": "Le texte de la mission ou de la réponse à copier",
  "etat_jardin_visuel": {
       "meteo": "soleil" OU "pluie" OU "nuages",
       "plantes_ajoutees": ["tournesol", "chêne", "rose"] (selon la réussite),
       "mauvaises_herbes_compostees": true/false (si un conflit a été résolu)
   }
}

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
