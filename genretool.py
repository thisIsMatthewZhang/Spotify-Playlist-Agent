# tool used by the AI agent to generate playlists or recommendations if the user specifies a genre criteria
from spotipy import Spotify, SpotifyOAuth
import random
import os
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Type, Optional
from langchain.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

scope: str = 'user-read-recently-played playlist-modify-public'
sp: Spotify = Spotify(auth_manager=SpotifyOAuth(scope=scope))


# schema that agent must conform to
class GenreSchema(BaseModel):
    """Schema used to build playlist/recommendations."""
    
    # REMEMBER: schema fields are what the user/LLM provides to the agent when giving a query (i.e. Langchain expects you to provide this information)
    num_tracks: int = Field(default=10, description='The number of songs the user asks for.')
    name: str = Field(default='SPA\'s Playlist', description='Name for the playlist/list of recommended songs.')
    genre: str = Field(default='rock', description='Genre that the user wants the songs to be focused on.')
    action_type: str = Field(default='recommend songs', description="'create playlist' for creating a new playlist or 'recommend songs' for giving only recommendations.")

    @field_validator('action_type')
    def normalize_action(cls, a) -> str:
        a = a.lower().strip()
        return 'create playlist' if a in 'playlist' else 'recommend songs'

    
# extend BaseTool and create a custom Spotify tool 
class GenreTool(BaseTool):
    """Tool to aid in giving song recommendations or playlists."""

    name: str = 'Spotify Genre Generator Tool'
    description: str = 'Use this tool when asked to create a new playlist with songs containing at least one common genre.' # LLM can use NL to infer when to use this tool

    args_schema: Type[BaseModel] = GenreSchema

    @staticmethod
    def get_recent_artists() -> list[dict]:
        """Retrieve artists from recently played songs."""
        artists = []
        items = sp.current_user_recently_played()['items']
        for item in items:
            a = sp.artist(item['track']['album']['artists'][0]['id'])
            artists.append(a)
        return artists

    @staticmethod
    def find_artist_genres(artist_id: str) -> list[str]:
        """Retrieve genres from artist."""
        genres = []
        artist_data = sp.artist(artist_id)
        if not artist_data['genres']:
            'Logic for scraping artist\'s genres if Spotipy can not find them.'

            ...
        
        genres.extend(artist_data['genres'])
        return list(set(genres))
    
    @staticmethod
    def get_new_releases() -> list[dict]:
        """Curate a list of new album releases and return their ids."""
        albums = sp.new_releases(country='us', limit=5)
        return [a for a in albums['albums']['items']]
    
    def _run(self, num_tracks, name, genre, action_type):
        songs = []
        recent_artists = self.get_recent_artists()
        # recently_played = [item['track']['uri'] for item in sp.current_user_recently_played()['items']]

        for ra in recent_artists:
            if genre in set(self.find_artist_genres(ra['id'])):
                ra_top_tracks = sp.artist_top_tracks(artist_id=ra['id'])
                songs.extend([track['uri'] for track in ra_top_tracks['tracks']])
            
        # get genres of random album artist
        rand_album = random.choice(self.get_new_releases())
        rand_album_artist_genres = set(self.find_artist_genres(rand_album['artists'][0]['id']))
        # if a genre g from random artist's genres is in recent genres, add random song from new album
        if genre in rand_album_artist_genres:
            rand_album_song_uris = [item['uri'] for item in sp.album_tracks(rand_album['id'])['items']]
            songs.extend([random.choice(rand_album_song_uris) for _ in range(num_tracks)])
        songs = list(set(songs))[:num_tracks]
        print(songs)

        if action_type == 'create playlist':
            playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=name)
            sp.playlist_add_items(playlist_id=playlist['id'], items=songs)
            return playlist
        elif action_type == 'recommend songs':
            return sp.tracks(tracks=songs, market='US')