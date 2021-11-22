import pandas as pd
import pandas.io.json
import json
files = ['mpd.slice.0-999.json', 'mpd.slice.1000-1999.json', 'mpd.slice.2000-2999.json', 'mpd.slice.3000-3999.json', 'mpd.slice.4000-4999.json']
data = json.load(open('mpd.slice.0-999.json'))

#json to dataframe ---------------------------------------------------------------------------------
lat,lng,el, album = [],[],[], []
for i in range(len(files)):
    data = json.load(open(files[i]))
    for result in data['playlists']:
        for track_result in result['tracks']:
            lng.append(track_result[u'track_name'])
            el.append(track_result[u'artist_name'])
            album.append(track_result[u'album_name'])

            lat.append(result[u'name'])

df = pd.DataFrame([lat,lng, el, album]).T
df.columns = ['playlist', 'track_name', 'artist_name', 'album_name']
pd.set_option('display.max_columns', None)
final_df = df.sort_values(by=['playlist', 'artist_name'])
print(final_df.head(100))

# dataframe to csv ---------------------------------------------------------------------------------
final_df.to_csv('songs.csv')