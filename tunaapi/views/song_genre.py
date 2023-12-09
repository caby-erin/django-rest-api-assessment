from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre

class SongGenreView(ViewSet):
  def retrieve(self, request, pk):
    song_genre = SongGenre.objects.get(pk=pk)
    serializer = SongGenreSerializer(song_genre)
    return Response(serializer.data)
  
  def list(self, reqest):
    song_genres = SongGenre.objects.all()
    serializer = SongGenreSerializer(song_genres, many=True)
    return Response(serializer.data)
  
class SongGenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = SongGenre
    fields = ('id', 'song_id', 'genre_id')
    depth = 2
