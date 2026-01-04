import os
import requests
import django
from datetime import datetime

# Configurare mediu Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from predictions.models import Match

def fetch_data():
    # Luăm cheia din Environment Variables (Render)
    api_key = os.getenv('FOOTBALL_API_KEY')
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Premier League (39), La Liga (140), Serie A (135)
    leagues = [39, 140, 135]
    today = datetime.now().strftime('%Y-%m-%d')
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print(f"--- Incepere import API-Football pentru: {today} ---")
    
    # Ștergem datele vechi pentru a evita duplicatele
    Match.objects.all().delete()

    for league_id in leagues:
        # Sezonul 2025 (valabil pentru Ianuarie 2026)
        querystring = {"date": today, "league": str(league_id), "season": "2025"}
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if "response" in data and len(data["response"]) > 0:
                for item in data["response"]:
                    home = item["teams"]["home"]["name"]
                    away = item["teams"]["away"]["name"]
                    
                    # Logica AI Simpla: Predictie bazata pe echipa gazda
                    prediction = f"HOME VICTORY: {home}"
                    
                    Match.objects.create(
                        home_team=home,
                        away_team=away,
                        predicted_winner=prediction,
                        confidence_score=0.88,
                        match_date=datetime.now(),
                        sport='Football'
                    )
                print(f"Liga {league_id}: Succes! Importate {len(data['response'])} meciuri.")
            else:
                print(f"Liga {league_id}: Nu sunt meciuri azi.")
        except Exception as e:
            print(f"Eroare la conexiunea cu API-ul: {e}")

if __name__ == "__main__":
    fetch_data()