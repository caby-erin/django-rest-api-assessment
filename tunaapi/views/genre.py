from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from tunaapi.models import Genre, SongGenre, Song
from rest_framework import serializers, status

class GenreView(ViewSet):
  def retrieve(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    serializer = AllInfoGenreSerializer(genre)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    genre = Genre.objects.create(
      description=request.data["description"]
    )
    serializer = GenreSerializer(genre)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def update(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.description = request.data["description"]
    genre.save()
    
    return Response(None, status=status.HTTP_200_OK)
  
class SongGenreSerializer(serializers.ModelSerializer):
  """JSON serializer for Song Genre"""
  class Meta:
    model = SongGenre
    fields = ( 'song_id', )
    depth = 1
  
class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = ('id', 'description')
    depth = 1

class AllInfoGenreSerializer(serializers.ModelSerializer):
  songs = SongGenreSerializer(many=True, read_only=True)
  class Meta:
    model = Genre
    fields = ('id', 'description', 'songs')
    depth = 1
