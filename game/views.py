import json

from django.http import JsonResponse
from django.views import View

from game.models import Game


class GameView(View):
    def get(self, request, *args, **kwargs):
        # Check if game exist, if not force a game-over
        if not Game.objects.filter(id=kwargs['id']).exists():
            return JsonResponse({
                'result': 'game-over',
                'mines': []
            })

        game = Game.objects.get(id=kwargs['id'])

        return JsonResponse(game.click_handler(x=kwargs['x'], y=kwargs['y']))

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        game = Game()
        game.create_board(data['x'], data['y'], data['mines'])

        return JsonResponse({'game_id': game.id})

    def delete(self, request, *args, **kwargs):
        if not Game.objects.filter(id=kwargs['id']).exists():
            return JsonResponse({'result': "Invalid Game"})

        Game.objects.filter(id=kwargs['id']).delete()

        return JsonResponse({'result': "ok"})
