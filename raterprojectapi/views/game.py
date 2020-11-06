"""View module for handling requests about games"""
from raterprojectapi.models import category
from raterprojectapi.models import gamecategory
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Game, Player, GameCategory, Category
from raterprojectapi.views.category import CategorySerializer


class Games(ViewSet):
    """Rater Gamer"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        player = Player.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.release_year = request.data["releaseYear"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.time = request.data["time"]
        game.age = request.data["age"]
        game.player = player

        game.save()

        categories = Category.objects.all()
       
        for category in categories:
            game_category = GameCategory(game=game, category=category)
            game_category.save()

        


      

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a game
    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     gamer = Gamer.objects.get(user=request.auth.user)

    #     # Do mostly the same thing as POST, but instead of
    #     # creating a new instance of Game, get the game record
    #     # from the database whose primary key is `pk`
    #     game = Game.objects.get(pk=pk)
    #     game.title = request.data["title"]
    #     game.maker = request.data["maker"]
    #     game.number_of_players = request.data["numberOfPlayers"]
    #     game.skill_level = request.data["skillLevel"]
    #     game.gamer = gamer

    #     gametype = GameType.objects.get(pk=request.data["gameTypeId"])
    #     game.gametype = gametype
    #     game.save()

    #     # 204 status code means everything worked but the
    #     # server is not sending back any data in the response
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single game
    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         game = Game.objects.get(pk=pk)
    #         game.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except Game.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        games = Game.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        # game_type = self.request.query_params.get('type', None)
        # if game_type is not None:
        #     games = games.filter(gametype__id=game_type)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

class GameCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    class Meta:
        model = GameCategory
        fields = ('category', 'game')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name')

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Player
        fields = ('id', 'user')
        depth = 1

class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for games
    Arguments:
        serializer type
    """
    player = PlayerSerializer(many=False)
    categories = CategorySerializer(many=True)
    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'description', 'designer', 'release_year','number_of_players', 'time', 'age', 'player', 'categories')
        depth = 1