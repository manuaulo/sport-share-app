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

    elif page == "Mein Profil":
        st.title(f"Profil von {st.session_state.user}")
        st.write("Hier kannst du deine eigenen Inserate verwalten.")
        st.button("Neues Equipment hochladen")