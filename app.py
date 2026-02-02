import streamlit as st
import pandas as pd
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver import get_driver   # importa la tua funzione


@st.cache_data(ttl="30min", show_spinner="Scraping WhoScored... può richiedere 10–25 secondi")
def load_whoscored_events_data(match_centre_url: str) -> pd.DataFrame | None:
    """
    Scarica e parsifica gli eventi dal Match Centre di WhoScored.
    Usa cache per evitare di rifare lo scraping ogni volta.
    """
    try:
        with get_driver() as driver:
            driver.get(match_centre_url)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            script_tag = soup.select_one('script:-soup-contains("matchCentreData")')

            if not script_tag:
                st.error("Non trovato 'matchCentreData' nella pagina.")
                return None

            # Estrazione più robusta del JSON
            text = script_tag.text
            start_marker = "matchCentreData: "
            if start_marker not in text:
                st.error("Formato inatteso di matchCentreData.")
                return None

            json_part = text.split(start_marker, 1)[1].split(",\n")[0].strip()
            # Pulizia finale (a volte c'è una parentesi o virgola in più)
            if json_part.endswith("}"):
                json_part = json_part.rstrip("} \n") + "}"
            elif json_part.endswith("},"):
                json_part = json_part[:-1]

            try:
                match_json = json.loads(json_part)
            except json.JSONDecodeError as e:
                st.error(f"Errore parsing JSON: {e}")
                st.code(json_part[:800] + "...", language="json")
                return None

            player_id_name_dict = match_json.get("playerIdNameDictionary", {})
            events_list = match_json.get("events", [])

            if not events_list:
                st.warning("Nessun evento trovato in matchCentreData.")
                return None

            df = pd.json_normalize(events_list)

            # Mapping nomi giocatori
            if "playerId" in df.columns:
                df["playerId"] = df["playerId"].astype("Int64")  # gestisce NaN meglio
                df["playerName"] = df["playerId"].apply(
                    lambda x: player_id_name_dict.get(str(x)) if pd.notna(x) else None
                )

            if "relatedPlayerId" in df.columns:
                df["relatedPlayerId"] = df["relatedPlayerId"].astype("Int64")
                df["relatedPlayerName"] = df["relatedPlayerId"].apply(
                    lambda x: player_id_name_dict.get(str(x)) if pd.notna(x) else None
                )

            # Colonna tempo leggibile
            if "minute" in df.columns:
                df["time"] = df["minute"].astype(str) + df["second"].fillna(0).astype(int).astype(str).str.zfill(2)
                df["time"] = df["time"].str.replace(r"(\d+)$", r":\1", regex=True)

            return df

    except Exception as e:
        st.error(f"Errore durante lo scraping:\n{str(e)}")
        return None


# ── Interfaccia Streamlit ─────────────────────────────────────────────

st.set_page_config(page_title="WhoScored Events Explorer", layout="wide")

st.title("WhoScored Match Events Scraper & Viewer ⚽📊")

st.markdown("""
Inserisci l'URL del **Match Centre** di WhoScored (esempio live o post-match)  
Es: `https://1xbet.whoscored.com/Matches/1946104/Live/England-League-Cup-2025-2026-Tottenham-Doncaster`
""")

default_url = "https://1xbet.whoscored.com/Matches/1946104/Live/England-League-Cup-2025-2026-Tottenham-Doncaster"

match_url = st.text_input("URL Match Centre", value=default_url)

if st.button("Scarica eventi", type="primary"):
    with st.spinner("Caricamento dati da WhoScored (Selenium)..."):
        df = load_whoscored_events_data(match_url)

    if df is not None and not df.empty:
        st.success(f"Caricati **{len(df)}** eventi!")

        # ── Statistiche veloci ───────────────────────────────
        col1, col2, col3 = st.columns(3)
        col1.metric("Eventi totali", len(df))
        if "teamId" in df.columns:
            col2.metric("Team differenti", df["teamId"].nunique())
        if "type" in df.columns:
            goals = df[df["type"] == {"id": 16, "displayName": "Goal"}].shape[0] if isinstance(df["type"].iloc[0], dict) else 0
            col3.metric("Goal rilevati", goals)

        # ── Filtri base ──────────────────────────────────────
        st.subheader("Filtri rapidi")

        event_types = df["type"].dropna().unique() if "type" in df.columns else []
        selected_types = st.multiselect("Tipo evento", options=event_types, default=event_types[:5])

        if "period" in df.columns:
            periods = sorted(df["period"].unique())
            selected_periods = st.multiselect("Periodo", options=periods, default=periods)

        # Applicazione filtri
        filtered_df = df.copy()
        if selected_types:
            filtered_df = filtered_df[filtered_df["type"].isin(selected_types)]
        if "period" in df.columns and selected_periods:
            filtered_df = filtered_df[filtered_df["period"].isin(selected_periods)]

        # ── Tabella ──────────────────────────────────────────
        st.subheader("Eventi (ordinati per tempo)")

        cols_to_show = ["minute", "second", "time", "type", "playerName", "relatedPlayerName", "teamId", "outcomeType", "x", "y"]
        available_cols = [c for c in cols_to_show if c in filtered_df.columns]

        st.dataframe(
            filtered_df[available_cols + ["id"]].sort_values("minute"),
            use_container_width=True,
            hide_index=True
        )

        # ── Bonus: visualizza JSON raw (opzionale) ──────────
        with st.expander("Mostra JSON raw (primi 2000 char)"):
            st.json(match_json)  # se vuoi debug

    else:
        st.warning("Nessun dato caricato o DataFrame vuoto.")
