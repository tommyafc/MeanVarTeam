# In whoscored/whoscored_events_data.py
import soccerdata as sd

def load_whoscored_events_data(match_url: str):
    # Estrai match_id dall'URL (es. /Matches/1901138/...)
    match_id = match_url.split('/Matches/')[1].split('/')[0]
    
    try:
        ws = sd.WhoScored()
        events = ws.read_events(match_id=int(match_id))
        return events  # è già un DataFrame
    except Exception as e:
        print(f"Errore soccerdata: {e}")
        return None
