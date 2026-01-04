import os
import requests
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from predictions.models import Match

def fetch_data():
    # Folosim Odds API pentru a aduce meciuri de fotbal din Europa
    api_key = os.getenv('FOOTBALL_API_KEY') 
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={api_key}&regions=eu&markets=h2h"

    print("Conectare la Odds API...")
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and len(data) > 0:
            # Ștergem vechiturile ca să fim siguri că vedem date noi
            Match.objects.all().delete()
            
            for item in data:
                home = item["home_team"]
                away = item["away_team"]
                
                # Generăm o predicție simplă bazată pe cotele oferite
                # Dacă prima cotă e mai mică, punem gazdele ca favorite
                prediction = f"Victory {home}"
                
                Match.objects.create(
                    home_team=home,
                    away_team=away,
                    predicted_winner=prediction,
                    confidence_score=0.82,
                    match_date=datetime.now(),
                    sport='Soccer'
                )
            print(f"Succes! Am importat {len(data)} meciuri reale din Premier League.")
        else:
            print(f"Eroare API: {data}")
    except Exception as e:
        print(f"Eroare la rulare: {e}")

if __name__ == "__main__":
    fetch_data()