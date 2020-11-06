"""Category ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from raterprojectapi.models import GameCategory

class GameCategories(ViewSet):
    """Category Viewset"""
    def retrieve(self, request, pk=None):
        """GET single category by id"""
        try:
            gamecategory = GameCategory.objects.get(pk=pk)

        except GameCategory.DoesNotExist:
            return Response(
                { 'message': 'There is no category with the specified ID.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serialization = GameCategorySerializer(gamecategory)
        return Response(serialization.data)

    def list(self, request):
        """GET all categories"""
        gamecategories = GameCategory.objects.all()
        serialization = GameCategorySerializer(gamecategories, many=True)
        return Response(serialization.data)

class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category"""

    class Meta:
        model = GameCategory
        fields = ('id', 'category', 'game')
        