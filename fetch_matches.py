import os
import requests
import django

# Setează mediul Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from predictions.models import Match
from django.utils import timezone

def fetch_live_matches():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Parametri: luăm meciurile de azi din Premier League (ID: 39)
    # Poți schimba ID-ul pentru alte ligi
    querystring = {"live": "all", "league": "39"} 

    headers = {
        "X-RapidAPI-Key": os.getenv('FOOTBALL_API_KEY'),
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if "response" in data:
        for item in data["response"]:
            home = item["teams"]["home"]["name"]
            away = item["teams"]["away"]["name"]
            
            # Exemplu simplu de "AI": dacă echipa gazdă are cota mai bună sau e mai bine clasată
            # Aici poți pune logica ta reală de predicție
            prediction = f"Win {home}" 
            
            # Salvăm în baza de date
            Match.objects.update_or_create(
                home_team=home,
                away_team=away,
                defaults={
                    'predicted_winner': prediction,
                    'confidence_score': 0.85, # Aici poți calcula un scor real
                    'match_date': timezone.now(),
                    'sport': 'Football'
                }
            )
        print(f"Importate {len(data['response'])} meciuri!")

if __name__ == "__main__":
    fetch_live_matches()