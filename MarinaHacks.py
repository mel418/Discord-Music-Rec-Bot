import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#from random import randint
from os import getenv
import dotenv

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
        await message.channel.send('Hello, plebeian!')
    

# example uri : spotify:artist:1uNFoZAHBGtllmzznpCI3s

    

@client.command()
async def genre_track_recommend(ctx, genre1, genre2, genre3):
    results = sp.search(q=f'genre:{genre1} OR genre:{genre2} OR genre:{genre3}', type='track', limit=5)
    #print(results)
    if not results['tracks']['items']:
        response = sp.recommendation_genre_seeds()
        genre_names = [genre_name.capitalize() for genre_name in response['genres']] 
        available_genres = '\n'.join(genre_names)
        badGenres = (f'Sorry, no tracks found for some of the selected genres. '
                    f'Please choose up to three genres, separated by commas and spaces again.\n'
                    f'You can choose from the following genres:\n{available_genres}\n'
                    f'Some common groups of genres: jazz, blues, funk\n'
                    f'reggae, ska, dancehall\n'
                    f'country, folk, bluegrass\n'
                    f'hip-hop, rap, R&B\n'
                    f'classical, opera, baroque\n'
                    f'Example: !genre_track_recommend rock pop electronic')
        await ctx.send(badGenres)
    else:
        track_names = [track['external_urls']['spotify'] for track in results['tracks']['items']]
        for NO in track_names:
            await ctx.channel.send(NO)



@client.command() #original:paste url of song and get 5 recommendations
async def recommend_url(ctx):
    whatever = ctx.message.content.split()[1]
    whatever = whatever.replace('\\', '')
    try:
        id = whatever.split(':')[2]
    except:
        id = whatever.split('/')[4].split('?')[0]
        
    ah = sp.recommendations(seed_artists=[id], seed_tracks=[id],limit=5) #let the user choose the limit
    track_names = [track['external_urls']['spotify'] for track in ah['tracks']]
    for NO in track_names:
        await ctx.channel.send(NO) 

client.run(TOKEN)
