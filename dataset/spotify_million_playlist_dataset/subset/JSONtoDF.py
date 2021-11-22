import pandas as pd
import pandas.io.json
import json

data = json.load(open('mpd.slice.0-999.json'))

#json to dataframe ---------------------------------------------------------------------------------
lat,lng,el, album = [],[],[], []
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