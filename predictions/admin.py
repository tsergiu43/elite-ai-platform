from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'sport', 'match_date', 'predicted_winner', 'confidence_score')
    list_filter = ('sport', 'match_date')
    search_fields = ('home_team', 'away_team')