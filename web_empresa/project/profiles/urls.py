from django.urls import path
from .views import ListsProfile, DetailProfile

profiles_patterns = ([
    # list, hace referencia a la raiz
    path('', ListsProfile.as_view(), name='lists'),
    # detail, donde le pasamos le username
    path('<username>/', DetailProfile.as_view(), name='detail'),
], "profiles")