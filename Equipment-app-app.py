import streamlit as st
import pandas as pd
import random

# --- 1. LOGIN LOGIK ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

def login():
    st.sidebar.title("Login Bereich")
    username = st.sidebar.text_input("Benutzername")
    password = st.sidebar.text_input("Passwort", type="password")
    if st.sidebar.button("Einloggen"):
        if username and password: # Hier später echte Prüfung einbauen
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()

# --- 2. DATEN-GENERATOR (500 INSERATE) ---
@st.cache_data # Damit die 500 Items nicht bei jedem Klick neu geladen werden
def get_fake_data():
    sportarten = ["Mountainbike", "Rennrad", "Surfboard", "Ski", "Snowboard", "Hantel-Set", "Kajak", "Zelt"]
    staedte = ["Berlin", "München", "Hamburg", "Köln", "Frankfurt", "Stuttgart", "Leipzig"]
    
    daten = []
    for i in range(500):
        artikel = random.choice(sportarten)
        daten.append({
            "ID": i + 1,
            "Name": f"{artikel} von Profi {i}",
            "Kategorie": artikel,
            "Preis": random.randint(10, 150),
            "Ort": random.choice(staedte)
        })
    return daten

# --- HAUPTPROGRAMM ---
if not st.session_state.logged_in:
    st.title("🔑 Willkommen bei SportShare")
    st.info("Bitte logge dich links in der Sidebar ein, um Equipment zu sehen.")
    login()
else:
    # Navigation nach dem Login
    st.sidebar.write(f"Eingeloggt als: **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
        
    page = st.sidebar.radio("Navigation", ["Marktplatz", "Mein Profil"])

    if page == "Marktplatz":
        st.title("🏆 SportShare Marktplatz")
        
        listings = get_fake_data()
        df = pd.DataFrame(listings)
        
        # Filter
        suche = st.text_input("Suche nach Stadt oder Equipment...")
        if suche:
            df = df[df['Name'].str.contains(suche, case=False) | df['Ort'].str.contains(suche, case=False)]
        
        st.write(f"Zeige {len(df)} Ergebnisse")
        st.dataframe(df, use_container_width=True)

import streamlit as st
from PIL import Image # Hilft beim Verarbeiten von Bildern

st.title("➕ Neues Equipment vermieten")

with st.form("upload_form", clear_on_submit=True):
    # 1. Text-Infos
    titel = st.text_input("Name des Equipments (z.B. Carbon Rennrad)")
    beschreibung = st.text_area("Besonderheiten & Infos (Zustand, Größe, Zubehör...)")
    
    col1, col2 = st.columns(2)
    with col1:
        kategorie = st.selectbox("Kategorie", ["Fahrrad", "Wassersport", "Wintersport", "Fitness"])
    with col2:
        preis = st.number_input("Preis pro Tag (€)", min_value=1)
    
    # 2. Bild-Upload
    uploaded_file = st.file_uploader("Lade ein Foto hoch", type=["jpg", "jpeg", "png"])
    
    submitted = st.form_submit_button("Inserat jetzt live schalten")

    if submitted:
        if titel and uploaded_file:
            # Bild anzeigen zur Bestätigung
            image = Image.open(uploaded_file)
            st.image(image, caption="Vorschau deines Equipments", width=300)
            
            # LOGIK ZUM SPEICHERN:
            # Da die App live ist, müssten wir das Bild jetzt in einer Cloud 
            # oder Datenbank speichern. Für den ersten Test fügen wir es 
            # der Liste im aktuellen Programm-Lauf hinzu:
            neues_item = {
                "Name": titel,
                "Kategorie": kategorie,
                "Preis": preis,
                "Beschreibung": beschreibung,
                "Bild": image # In einer echten App speichern wir hier die URL zum Bild
            }
            st.success(f"Super! Dein {titel} ist jetzt (theoretisch) für andere sichtbar.")
        else:
            st.error("Bitte gib einen Namen an und lade ein Bild hoch!")