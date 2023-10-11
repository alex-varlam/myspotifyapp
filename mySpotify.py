import base64
import datetime
from baserest import BaseRest
from urllib.parse import urlencode


class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api.spotify.com/v1'
        self.restSession = BaseRest()
        self.get_token()

    @property
    def headers(self):
        return {
            'Authorization': f'Bearer {self.return_valid_token()}'
        }

    def get_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        client_credentials = f"{self.client_id}:{self.client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode())
        headers = {
            'Authorization': f'Basic {client_credentials_b64.decode()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data_json = {
            "grant_type": "client_credentials"
        }
        response = self.restSession.send_post(apiPath=token_url, data_json=data_json, headers=headers)
        self.access_token = response['access_token']
        expires_in = response['expires_in']
        self.expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)

    def return_valid_token(self):
        if self.check_token_expire():
            self.get_token()
        return self.access_token

    def check_token_expire(self):
        now = datetime.datetime.now()
        return self.expires < now

    def __get_resource(self, type, _id):
        url = f'{self.base_url}/{type}/{_id}'
        return self.restSession.send_get(url, headers=self.headers)

    def get_album(self, _id):
        return self.__get_resource('albums', _id)

    def get_artist(self, _id):
        return self.__get_resource('artists', _id)

    def get_track_audio_features(self, _id):
        return self.__get_resource('audio-features',_id)

    def get_track_audio(self, search_query):
        resp = self.search(search_query, 'track')
        _id = resp['tracks']['items'][0]['id']
        return self.get_track_audio_features(_id)

    def search(self, search_query, search_type):
        ''' search_query can be dict with the following possible keys:
        - track - song to search
        - album - further filter by album
        - artist- further filter by artist
        - genre. Or it can be a simple string
        '''
        if isinstance(search_query, dict):
            search_string = ' '.join([f'{key}:{value}' for key,value in search_query.items()])
        else:
            search_string = search_query
        url = f'{self.base_url}/search'
        data_json = urlencode({
            'q': search_string,
            'type': search_type
        })
        url_search = f"{url}?{data_json}"
        print(url_search)
        return self.restSession.send_get(url_search, headers=self.headers)

    def get_playlists(self, user_id='x6d9x32ukp7o3vxr0wvtmk87u'):
        url= f"{self.base_url}/users/{user_id}/playlists"
        return self.restSession.send_get(url, headers=self.headers)

    def get_id_of_my_playlist(self, playlist_name):
        play_list = self.get_playlists()
        for item in play_list['items']:
            if item['name'] == playlist_name:
                return item['id']
        raise Exception('Playlist does not exist for my profile')

    def get_tracks_from_playlist(self, playlist_name):
        _id = self.get_id_of_my_playlist(playlist_name)
        url = f"{self.base_url}/playlists/{_id}/tracks"
        return self.restSession.send_get(url, headers = self.headers)

    def get_track_ids(self, track_list):
        track_ids = []
        for track in track_list:
            print(track)
            response = self.search(track, 'track')
            track_ids.append(response['tracks']['items'][0]['id'])
        print(track_ids)
        return track_ids

    def get_recommendations(self, seed_tracks, limit=20, seed_genres=None, audio_features=None):
        seed_track_ids = ','.join(self.get_track_ids(seed_tracks))
        url = f'{self.base_url}/recommendations'
        url += f'?limit={limit}'
        url += f'&seed_tracks={seed_track_ids}'
        if seed_genres:
            url += f'&seed_genres={seed_genres}'
        if audio_features:
            url += ''.join(f"&{key}={value}" for key, value in audio_features.items())
        print(url)
        resp = self.restSession.send_get(url, headers=self.headers)
        dict_tracks = []
        for item in resp['tracks']:
            dict_tracks.append(
                {
                    'name': item['name'],
                    'artist': item['artists'][0]['name'],
                    'track id': item['id']
                }
            )
        return dict_tracks

    # def get_top(self, type='tracks'):
    #     url = f"{self.base_url}/me/top/{type}"
    #     return self.restSession.send_get(url, headers=self.headers)

