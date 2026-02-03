import streamlit as st
import pandas as pd
from whoscored.whoscored_events_data import load_whoscored_events_data   # il tuo scraper
from utils.driver import DriverContext, get_driver

# Context manager for driver lifecycle
with DriverContext() as driver:
    driver.get(url)
    # Perform scraping operations

# Simple driver getter
with get_driver() as driver:
    driver.get(url)

# Configurazione pagina
st.set_page_config(
    page_title="WhoScored Events Explorer",
    layout="wide",
    page_icon="⚽"
)
from scraping_countermeasures.rate_limiter import RateLimiter
from scraping_countermeasures.delays import add_random_delay
from scraping_countermeasures.user_agent_rotation import get_random_user_agent

# Rate limiting
limiter = RateLimiter(max_requests=10, time_window=60)
limiter.wait_if_needed()

# Random delays
add_random_delay(min_delay=1, max_delay=3)

# User agent rotation
headers = {'User-Agent': get_random_user_agent()}

st.title("WhoScored Match Events Viewer ⚽📊")

st.markdown("""
Inserisci l'URL del **Match Centre** di WhoScored (live o post-match).  
Esempio:  
`https://www.whoscored.com/Matches/1729345/Live/England-Premier-League-2025-2026-Manchester-United-Liverpool`
""")

# ── Casella per inserire l'URL ────────────────────────────────
match_url = st.text_input(
    "URL Match Centre WhoScored",
    placeholder="https://www.whoscored.com/Matches/......",
    help="Copia l'URL dalla barra del browser quando sei nella pagina Match Centre"
)

# Bottone per avviare lo scraping
if st.button("Carica eventi partita", type="primary", disabled=not match_url.strip()):
    if not match_url.strip():
        st.warning("Inserisci un URL valido.")
    else:
        with st.spinner("Scraping dati da WhoScored... (10–30 secondi)"):
            try:
                # Chiamata alla tua funzione (con cache se l'hai decorata)
                df = load_whoscored_events_data(match_url)

                if df is not None and not df.empty:
                    st.success(f"Caricati **{len(df):,}** eventi!")
                else:
                    st.warning("Nessun evento trovato o parsing fallito.")

            except Exception as e:
                st.error(f"Errore durante il caricamento:\n{str(e)}")
                st.info("Controlla che l'URL sia corretto e che la pagina sia un Match Centre valido.")

else:
    # Messaggio iniziale / placeholder
    if not match_url.strip():
        st.info("Inserisci l'URL e premi il bottone per iniziare.")
