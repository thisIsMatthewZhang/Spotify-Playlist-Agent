# 🎧 Spotify Playlist Agent (SPA)
Meet the Spotify Playlist Agent (or SPA)!

SPA is an autonomous AI agent designed to act as your personal music concierge. It is capable of generating tailored song recommendations and creating playlists directly in your Spotify account based on your specific criteria. By leveraging the power of LangChain and Spotipy, SPA operates with high degrees of autonomy, choosing and executing the right tools to fulfill your musical requests without needing step-by-step instructions.

## ✨ Core Features
Autonomous Decision Making: SPA uses its "reasoning engine" to determine whether it needs to fetch songs by artist, genre, or other criteria.

Direct Spotify Integration: Authenticates via SpotifyOAuth to manage your public and private playlists.

Intelligent Recommendations: Combines your recently played history, new releases, and top artist tracks to find the perfect songs.

Action Flexibility: Can either provide a list of recommended songs or "create a playlist" directly in your account.

## 🔧 The Agent's Utility Belt
SPA's capabilities are extended through specialized LangChain tools. Each tool follows a strict schema to ensure the agent provides accurate data.

1. Spotify Genre Tool (GenreTool)
Used when you specify a genre-based request (e.g., "Make a rock playlist").

Logic: It scans your recently played artists for those matching the genre, pulls top tracks from new releases, and ensures variety.

Customization: Allows the agent to specify the num_tracks, the name of the playlist, and the action_type.

2. Spotify Artist Music Tool (ArtistTool)
Activated when you request music from specific artists.

Artist Identification: Automatically searches for and retrieves unique Spotify Artist IDs.

Song Selection: Fetches top-performing tracks for a list of artists and randomly selects from them to meet your requested track count.

## 🛠️ Tech Stack
AI Orchestration: LangChain (Custom BaseTool & StructuredTool).

Spotify API: Spotipy (Python client for the Web API).

Data Validation: Pydantic (for robust input schemas and field validation).

Environment Management: python-dotenv for secure API credential handling.
