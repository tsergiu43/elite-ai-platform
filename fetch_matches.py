import os
import requests
import django
from datetime import datetime

# Configurare Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from predictions.models import Match

def fetch_data():
    api_key = os.getenv('FOOTBALL_API_KEY') 
    # Luăm Premier League (soccer_epl)
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={api_key}&regions=eu&markets=h2h"

    print("Fetching new data from Odds API...")
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # Curățăm tot ce e vechi
            Match.objects.all().delete()
            
            for item in data:
                home = item["home_team"]
                away = item["away_team"]
                
                # Logica AI: Alegem echipa cu cota cea mai mică (favorita)
                # Căutăm cotele de la primul bookmaker disponibil
                try:
                    odds = item["bookmakers"][0]["markets"][0]["outcomes"]
                    # Sortăm după preț (cotă) - cea mai mică e prima
                    sorted_odds = sorted(odds, key=lambda x: x["price"])
                    favorite = sorted_odds[0]["name"]
                    prediction = f"WINNER: {favorite}"
                except:
                    prediction = f"WINNER: {home} (Draw No Bet)"
                
                Match.objects.create(
                    home_team=home,
                    away_team=away,
                    predicted_winner=prediction,
                    confidence_score=0.82,
                    match_date=datetime.now(),
                    sport='Soccer'
                )
            print(f"Succes! {len(data)} meciuri importate.")
        else:
            print(f"Eroare API: {data}")
    except Exception as e:
        print(f"Eroare: {e}")

if __name__ == "__main__":
    fetch_data()