from mySpotify import SpotifyAPI

client_id = '5b9c409d9b7c4a86985fa5bc52cf5f1a'
client_secret = '5b91c3bf2d11406a9d108210913349d1'

music = [
    {'track': 'Wasted', 'artist': 'Tomberlin'},
    {'track': 'What the Fuck', 'artist':'The Boxer Rebellion'},
    {'track': 'Call Me In The Afternoon', 'artist':'Half Moon Run'},
    {'track': 'Inside Out', 'artist':'Spoon'}
]

spot = SpotifyAPI(client_id, client_secret)
# print(spot.access_token)
# print(spot.expires)
# response = spot.search('Coming Of Age artist:Maddie', 'track')
# print(response)
response2 = spot.search({'track':'Hard On Everyone', 'album':'Total Freedom'}, 'track')
# print(response2)
# get_audio = spot.get_track_audio_features('3nJEx6rRNcFXdIUSNkuMPz')
# x = spot.get_tracks_from_playlist('Running')
# print(x)
# seed_tracks=''
# for item in music:
#     r = spot.search({'track': item['track'], 'artist': item['artist']}, 'track')
#     seed_tracks += f"{r['tracks']['items'][0]['id']},"
# seed_tracks=seed_tracks[:-1]
# y = spot.get_track_audio({'track':'Dramamine', 'artist':'Modest Mouse'})
dict_audio = {
    'tempo': 180,
    'energy': 0.7,
    'danceability': 0.7
}
dict_track_list = spot.get_recommendations(music, limit=20, seed_genres='indie', audio_features=dict_audio)
for track in dict_track_list:
    print(f"{track['name']} --> {track['artist']}")
# print('Get artist')
# response2 = spot.get_artist(response['tracks']['items'][0]['artists'][0]['id'])
# print(response2)
