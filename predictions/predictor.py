import random
from .models import Match

def generate_predictions():
    # Luăm toate meciurile care au textul de așteptare
    pending_matches = Match.objects.filter(predicted_winner="Analiză în curs...")
    
    for match in pending_matches:
        # Algoritm de simulare a predicției
        teams = [match.home_team, match.away_team, "Draw"]
        winner = random.choice(teams)
        confidence = round(random.uniform(0.65, 0.98), 2)
        
        # Salvăm rezultatul în baza de date
        match.predicted_winner = winner
        match.confidence_score = confidence
        match.save()
        
    print(f"Succes! S-au generat predicții pentru {len(pending_matches)} meciuri.")