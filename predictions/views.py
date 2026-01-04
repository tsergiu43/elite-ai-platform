import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Match, UserProfile

stripe.api_key = settings.STRIPE_SECRET_KEY

def landing(request): return render(request, 'predictions/landing.html')
def archive(request): return render(request, 'predictions/archive.html')
def why_us(request): return render(request, 'predictions/why_us.html')
def legal(request): return render(request, 'predictions/legal.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(); login(request, user); return redirect('dashboard')
    else: form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def dashboard(request):
    matches = Match.objects.all().order_by('match_date')
    return render(request, 'predictions/dashboard.html', {'matches': matches})

def create_checkout_session(request):
    if not request.user.is_authenticated: return redirect('login')
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price_data': {'currency': 'ron', 'product_data': {'name': 'Acces VIP'}, 'unit_amount': 4900}, 'quantity': 1}],
        mode='payment',
        success_url=request.build_absolute_uri('/dashboard/'),
        cancel_url=request.build_absolute_uri('/dashboard/'),
    )
    return redirect(checkout_session.url, code=303)