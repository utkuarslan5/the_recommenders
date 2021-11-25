import pandas as pd
import pandas.io.json
import json

path = 'dataset/spotify_million_playlist_dataset/subset'
files = ['mpd.slice.0-999.json', 'mpd.slice.1000-1999.json', 'mpd.slice.2000-2999.json', 'mpd.slice.3000-3999.json',
         'mpd.slice.4000-4999.json']
# data = json.load(open('../dataset/spotify_million_playlist_dataset/subset/mpd.slice.0-999.json'))

# json to dataframe ---------------------------------------------------------------------------------
pid, lat, lng, el, album, pos, pid = [], [], [], [], [], [], []
for i in range(len(files)):
    with open(files[i], "r") as f:
        data = json.load(f)
    for result in data['playlists']:
        for track_result in result['tracks']:
            lng.append(track_result[u'track_name'])
            el.append(track_result[u'artist_name'])
            album.append(track_result[u'album_name'])
            pos.append(track_result[u'pos'])
            lat.append(result[u'name'])
            pid.append(result[u'pid'])

df = pd.DataFrame([pid, lat, lng, el, album, pos]).T
df.columns = ['pid', 'playlist', 'track_name', 'artist_name', 'album_name', 'track_pos']
pd.set_option('display.max_columns', None)
final_df = df.sort_values(by=['pid', 'artist_name'])
print(final_df.head(100))

# dataframe to csv ---------------------------------------------------------------------------------
final_df.to_csv('songs.csv')
