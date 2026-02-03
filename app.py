import streamlit as st
import pandas as pd
from whoscored.whoscored_events_data import load_whoscored_events_data   # il tuo scraper
pip install --upgrade webdriver-manager

# Configurazione pagina
st.set_page_config(
    page_title="WhoScored Events Explorer",
    layout="wide",
    page_icon="⚽"
)

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

                    # Statistiche veloci
                    col1, col2 = st.columns(2)
                    col1.metric("Eventi totali", f"{len(df):,}")
                    if "type" in df.columns:
                        goals = len(df[df['type'].apply(lambda x: x.get('displayName') == 'Goal' if isinstance(x, dict) else False)])
                        col2.metric("Goal rilevati", goals)

                    # Tabella principale
                    st.subheader("Eventi partita (ordinati per tempo)")

                    # Colonne utili da mostrare (adatta se vuoi)
                    cols_show = ["minute", "second", "playerName", "type", "outcomeType", "teamId", "x", "y"]
                    available = [c for c in cols_show if c in df.columns]

                    st.dataframe(
                        df[available].sort_values("minute"),
                        use_container_width=True,
                        hide_index=True
                    )

                    # Opzionale: scarica CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Scarica eventi come CSV",
                        csv,
                        "whoscored_events.csv",
                        "text/csv",
                        key="download-csv"
                    )

                else:
                    st.warning("Nessun evento trovato o parsing fallito.")

            except Exception as e:
                st.error(f"Errore durante il caricamento:\n{str(e)}")
                st.info("Controlla che l'URL sia corretto e che la pagina sia un Match Centre valido.")

else:
    # Messaggio iniziale / placeholder
    if not match_url.strip():
        st.info("Inserisci l'URL e premi il bottone per iniziare.")
