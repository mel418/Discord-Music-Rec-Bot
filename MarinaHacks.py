import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#from random import randint
from os import getenv
import dotenv
import asyncio

dotenv.load_dotenv()

TOKEN = getenv('TOKEN')

# Initialize the client object
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

spotify_client_credentials = SpotifyClientCredentials(
    client_id=getenv('spotid'),
    client_secret=getenv('spotsecret')
)
sp = spotipy.Spotify(client_credentials_manager=spotify_client_credentials)

# Define the on_ready event handler
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# Define the on_message event handler
@client.command()

async def hello(message):
        #if randint(0,25) == 1:
        await message.channel.send('Hello, world!')
    

# example uri : spotify:artist:1uNFoZAHBGtllmzznpCI3s

@client.command()
async def recommend(ctx):
    whatever = ctx.message.content.split()[1]
    whatever = whatever.replace('\\', '')
    try:
        id = whatever.split(':')[2]
    except:
        id = whatever.split('/')[4].split('?')[0]
        
    ah = sp.recommendations(seed_artists=[id], seed_tracks=[id],limit=5)
    track_names = [track['external_urls']['spotify'] for track in ah['tracks']]
    for NO in track_names:
        await ctx.channel.send(NO) 

client.run(TOKEN)