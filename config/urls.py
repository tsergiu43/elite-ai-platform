from django.contrib import admin
from django.urls import path, include
from predictions.views import landing, dashboard, archive, why_us, legal, create_checkout_session, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', landing, name='landing'),
    path('dashboard/', dashboard, name='dashboard'),
    path('archive/', archive, name='archive'),
    path('why-us/', why_us, name='why_us'),
    path('legal/', legal, name='legal'),
    path('register/', register, name='register'),
    path('subscribe/', create_checkout_session, name='subscribe'),
]