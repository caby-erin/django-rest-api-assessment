from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from tunaapi.models import Song, Artist, Genre
from rest_framework import serializers, status

class SongView(ViewSet):
  def retrieve(self, request, pk):
    song = Song.objects.get(pk=pk)
    serializer = AllInfoSongSerializer(song)
    return Response(serializer.data)
  
  def list(self, request):
    songs = Song.objects.all()
    
    artist = request.query_params.get('artist_id', None)
    if artist is not None:
      songs = songs.filter(artist_id_id=artist)
    
    selected_genre = request.query_params.get('genre_id', None)
    if selected_genre is not None:
      selected_genre = selected_genre.filter(genres__genre_id__id=selected_genre)
      
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    artist_id = Artist.objects.get(pk=request.data["artistId"])
    
    song = Song.objects.create(
      title=request.data["title"],
      artist_id=artist_id,
      album=request.data["album"],
      length=request.data["length"],
    )
    serializer = SongSerializer(song)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def destroy(self, request, pk):
    """Handle DELETE request for an artist"""
    song = Song.objects.get(pk=pk)
    song.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def update(self, request, pk):
    song = Song.objects.get(pk=pk)
    song.title = request.data["title"]
    song.album = request.data["album"]
    song.length = request.data["length"]
    artist_id = Artist.objects.get(pk=request.data["artistId"])
    song.artist_id = artist_id
    song.save()
    
    serializer = SongSerializer(song)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class SongSerializer(serializers.ModelSerializer):
  class Meta:
    model = Song
    fields = ('id', 'title', 'album', 'artist_id', 'length')


class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = ( 'id', 'description')
    depth = 1
  
class AllInfoSongSerializer(serializers.ModelSerializer):
  genres = GenreSerializer(many=True, read_only=True)
  class Meta:
    model = Song
    fields = ('id', 'title', 'album', 'artist_id', 'length', 'genres')
    depth = 2
