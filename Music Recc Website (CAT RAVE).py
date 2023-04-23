from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os import getenv
import dotenv

dotenv.load_dotenv()

spotify_client_credentials = SpotifyClientCredentials(
    client_id=getenv('spotid'),
    client_secret=getenv('spotsecret')
)
sp = spotipy.Spotify(client_credentials_manager=spotify_client_credentials)

app = Flask(__name__, template_folder='MarinaHack')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        artist_id = request.form.get('artist_id')
        ah = sp.recommendations(seed_artists=[artist_id], seed_tracks=[artist_id], limit=5)
        track_names = [track['external_urls']['spotify'] for track in ah['tracks']]
        return render_template('recommendations.html', track_names=track_names)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)