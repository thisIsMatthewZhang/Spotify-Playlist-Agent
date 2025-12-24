# Say hi to the Spotify Playlist Agent (SPA), a simple AI agent who specializes in improving the experience of Spotify listeners.
# SPA's central functionality lies in curating tracks into custom playlists based on the user's listening patterns. It takes several features
# into account when generating a new playlist - listening history, music genre, new album releases, similarity between artists, etc.
# This agent makes use of the Spotify Web API and Python's spotipy package for interacting with the API. OpenAI is used as the LLM, 
# and LangChain as the orchestration tool.

from genretool import GenreTool
from artisttool import ArtistTool
from spotipy import Spotify, SpotifyOAuth
from langchain_openai.chat_models import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.agent_types import AgentType
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.agents import initialize_agent
import os
from dotenv import load_dotenv

def main():

    load_dotenv()

    os.environ['LANGSMITH_TRACING'] = 'true'

    # currently, langchain does not support a builtin integration tool for the Spotify API 

    user_query_genre = 'Give me 15 song recs that are pop. ' \
                'Give a fun name based on the songs. ' \
                'Mention any tools you use.'

    user_query_artists = 'I would like 15 song recommendations from Charlie Puth, Pit Bull, and Baby Jane.'

    prompt_template = ChatPromptTemplate.from_messages([
        (
            'system', 'You are SPA (Spotify Playlist Agent), a highly dependable assistant for helping users (like me) enhance their Spotify playlists.'
            'You can help with tasks such as creating playlists based on a common genre, common artist(s), or new releases.'
            'You should either recommend songs or create a new playlist depending on what the user says.'
            'Always restate your name and what your purpose is in your thoughts.'
        ),
        ('human', '{user_query}')
    ])

    tools = [GenreTool(), ArtistTool()]
    llm = init_chat_model(model='gpt-4o-mini', model_provider='openai')
    prompt = prompt_template.invoke({'user_query': user_query_artists})

    agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    res = agent.run(prompt)
    print(res)


if __name__ == '__main__':
    main()