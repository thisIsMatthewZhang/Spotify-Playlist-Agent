

from langchain_core.tools import BaseTool, StructuredTool, Tool
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Type, Optional
from spotipy import Spotify, SpotifyOAuth
from dotenv import load_dotenv
import random

load_dotenv()

sp: Spotify = Spotify(auth_manager=SpotifyOAuth())


class ArtistSchema(BaseModel):
    """Schema for requesting artist music."""

    num_tracks: int = Field(default=10, description='The number of tracks to be retrieved.')
    artists: list[str] = Field(default=['Baby Jane'], description='List of artists the user wants to get tracks for.')


class ArtistTool(BaseTool):
    """Tool for extracting Spotify information based on artists."""

    name: str = 'Spotify Artist Music Tool'
    description: str = 'Use this tool when the user makes song requests based on artists.'

    args_schema: Type[BaseModel] = ArtistSchema

    @staticmethod
    def get_artist_id(artist_name: str) -> str:
        """Return id of artist"""
        artist_info = sp.search(q='artist:' + artist_name, type='artist')
        if artist_info:
            return artist_info['artists']['items'][0]['id']
        else:
            raise ValueError("No artist found with the name:", artist_name)

    
    @staticmethod
    def get_artist_top_songs(artist_id: str) -> list[str]:
        """Return only the names of the tracks"""
        items = sp.artist_top_tracks(artist_id)
        if items:
            return [item['name'] for item in items['tracks']]
        else:
            raise ValueError("No tracks found for artist.")


    def _run(self, num_tracks, artists):
        all_songs = []
        for a in artists:
            artist_id = self.get_artist_id(a)
            artist_songs = self.get_artist_top_songs(artist_id)
            all_songs.extend(artist_songs)
        chosen_songs = []
        while len(chosen_songs) < num_tracks:
            chosen_song = random.choice(all_songs)
            chosen_songs.append(chosen_song)
            all_songs.remove(chosen_song)
        return chosen_songs
        
