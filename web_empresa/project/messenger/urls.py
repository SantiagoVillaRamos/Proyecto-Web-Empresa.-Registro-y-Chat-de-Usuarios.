from django.urls import path
from .views import ThreadsListView, ThreadDetailView, add_messenger, start_thread

messenger_patterns = ([
    path('', ThreadsListView.as_view(), name='list'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='detail'),
    path('thread/<int:pk>/add/', add_messenger, name='add'),
    path('thread/start/<username>/', start_thread, name='start'),
], 'messenger')