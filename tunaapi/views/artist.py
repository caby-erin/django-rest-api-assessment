from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song
from django.db.models import Count

class ArtistView(ViewSet):
  def retrieve(self, request, pk):
    
    try:
      artist = Artist.objects.annotate(song_count=Count('songs')).get(pk=pk)
      serializer = AllInfoArtistSerializer(artist)
      return Response(serializer.data)
    
    except Artist.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  
  def list(self, request):
    artists = Artist.objects.all()
      
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)
  
  def create (self, request):
    artist = Artist.objects.create(
      name=request.data["name"],
      age=request.data["age"],
      bio=request.data["bio"],
    )
    serializer = ArtistSerializer(artist)
    return Response(serializer.data, status.HTTP_201_CREATED)
  
  def destroy(self, request, pk):
    """Handle DELETE request for an artist"""
    artist = Artist.objects.get(pk=pk)
    artist.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def update(self, request, pk):
    artist = Artist.objects.get(pk=pk)
    artist.name=request.data["name"]
    artist.age=request.data["age"]
    artist.bio=request.data["bio"]
    artist.save()
    
    return Response(None, status=status.HTTP_200_OK)

class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = ('id', 'name', 'age', 'bio')
    depth = 1
    
class SongSerializer(serializers.ModelSerializer):
  class Meta:
    model = Song
    fields = ( 'id', 'title', 'album', 'length' )
  
class AllInfoArtistSerializer(serializers.ModelSerializer):
  songs = SongSerializer(many=True, read_only=True)
  song_count = serializers.IntegerField(default=None)
  class Meta:
    model = Artist
    fields = ( 'id', 'name', 'age', 'bio', 'songs', 'song_count' )
    depth = 1
