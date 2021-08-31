from django.urls import path
from django.views.generic.base import TemplateView

from game.views import GameView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('game', GameView.as_view(), name='new-game'),
    path('game/<int:id>', GameView.as_view(), name='delete-game'),
    path('game/<int:x>/<int:y>/<int:id>',
         GameView.as_view(), name='game-click'),
]
