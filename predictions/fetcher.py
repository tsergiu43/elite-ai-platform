from .models import Match
from django.utils import timezone
from datetime import timedelta

def fetch_upcoming_matches():
    # Simulăm meciurile din săptămâna curentă (Ianuarie 2026)
    meciuri_2026 = [
        ("Real Madrid", "Atletico Madrid"),
        ("Bayern Munich", "Dortmund"),
        ("Juventus", "AC Milan"),
        ("PSG", "Marseille"),
        ("Arsenal", "Man City"),
        ("Inter Milan", "Napoli")
    ]

    count = 0
    for home, away in meciuri_2026:
        # Punem meciul să fie mâine la ora 20:00
        data_viitoare = timezone.now().replace(hour=20, minute=0) + timedelta(days=1)
        
        Match.objects.get_or_create(
            home_team=home,
            away_team=away,
            match_date=data_viitoare,
            defaults={
                'sport': 'football',
                'predicted_winner': 'Analiză în curs...',
                'confidence_score': 0.0
            }
        )
        count += 1
    print(f"Succes! Am generat {count} meciuri pentru sezonul 2026.")