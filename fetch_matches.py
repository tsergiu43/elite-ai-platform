import os
import requests
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from predictions.models import Match

def fetch_data():
    api_key = os.getenv('FOOTBALL_API_KEY')
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Setăm data de azi: 2026-01-04
    today = "2026-01-04" 
    
    # Parametri pentru Premier League (39) și sezonul curent (2025)
    querystring = {"date": today, "league": "39", "season": "2025"} 

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print(f"Checking matches for {today}...")
    try:
        response = requests.get(url, headers=headers, params=querystring)
        res_data = response.json()

        if "response" in res_data and len(res_data["response"]) > 0:
            # Opțional: Ștergem meciurile vechi înainte de import
            Match.objects.all().delete()
            
            for item in res_data["response"]:
                home = item["teams"]["home"]["name"]
                away = item["teams"]["away"]["name"]
                Match.objects.create(
                    home_team=home,
                    away_team=away,
                    predicted_winner=f"Win {home}",
                    confidence_score=0.85,
                    match_date=datetime.now(),
                    sport='Football'
                )
            print("Import realizat cu succes!")
        else:
            print("Nu s-au găsit meciuri pentru această dată.")
    except Exception as e:
        print(f"Eroare la API: {e}")

if __name__ == "__main__":
    fetch_data()