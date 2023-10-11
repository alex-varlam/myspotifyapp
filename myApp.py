from flask import Flask, render_template, request, redirect, url_for
from mySpotify import SpotifyAPI

app = Flask(
    __name__, static_url_path="", static_folder="templates", template_folder="templates"
)

client_id = '5b9c409d9b7c4a86985fa5bc52cf5f1a'
client_secret = '5b91c3bf2d11406a9d108210913349d1'

def song_to_dict(string_input):
    song = string_input.split(' - ')
    return {'track': song[0], 'artist': song[1]}


@app.route("/index", methods=["GET", "POST"])
def index():
    music = []
    dict_track_list = []
    if request.method == "POST":
        song1 = request.form.get('song1')
        if song1:
            music.append(song_to_dict(song1))
        song2 = request.form.get('song2')
        if song2:
            music.append(song_to_dict(song2))
        song3 = request.form.get('song3')
        if song3:
            music.append(song_to_dict(song3))
        genre = request.form.get('genre')
        dict_audio = {}
        for key in ['tempo', 'energy', 'danceability']:
            val_audio = request.form.get(key)
            if val_audio:
                dict_audio[key] = val_audio

        spot = SpotifyAPI(client_id, client_secret)
        dict_track_list = spot.get_recommendations(music, limit=20, seed_genres=genre, audio_features=dict_audio)

    template = 'seeds.html'
    return render_template(template, track_list=dict_track_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001, debug=True)