import streamlit as st
import soccerdata as sd
import re

@st.cache_data(ttl=3600, show_spinner="Caricamento eventi da WhoScored via soccerdata...")
def load_whoscored_events_data(match_url: str):
    """
    Estrae match_id dall'URL e scarica gli eventi con soccerdata.
    Restituisce DataFrame o None in caso di errore.
    """
    try:
        # Estrai match_id dall'URL (es. /Matches/1901138/...)
        match = re.search(r'/Matches/(\d+)', match_url)
        if not match:
            st.error("Impossibile estrarre match_id dall'URL. Deve contenere '/Matches/NUMERO/'")
            return None
        
        match_id = int(match.group(1))
        
        # Inizializza WhoScored (league/season opzionali, ma aiutano per caching)
        # Puoi lasciare leagues/seasons vuoti se vuoi solo un match
        ws = sd.WhoScored(
            leagues=None,          # o es. "ENG-Premier League" se conosci la lega
            seasons=None,          # o "2526" per 2025/26
            no_cache=False,        # usa cache se possibile
            proxy=None,            # aggiungi proxy/Tor se bloccato
            headless=True
        )
        
        # Scarica eventi (default: pd.DataFrame)
        events_df = ws.read_events(match_id=match_id)
        
        if events_df is None or events_df.empty:
            st.warning(f"Nessun evento trovato per match_id {match_id}")
            return None
        
        return events_df
    
    except Exception as e:
        st.error(f"Errore durante il caricamento con soccerdata:\n{str(e)}")
        st.info("Possibili cause: match_id non valido, partita senza eventi, limite rate WhoScored, bisogno di proxy.")
        return None
