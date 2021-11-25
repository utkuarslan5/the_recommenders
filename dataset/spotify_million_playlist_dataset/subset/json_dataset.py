"""Unused, use files under src to access dataset.
    See preprocessing.py for usage example ....         """
# import csv
# import json
# import pandas as pd
# from pandas import json_normalize
#
#
# path = 'dataset/spotify_million_playlist_dataset/subset'
# with open(path + "/" + 'mpd.slice.0-999.json', "r") as f:
#     data = json.load(f)
#
# print(data)
# df = pd.DataFrame(data)
# df = json_normalize(data, record_path='playlists', record_prefix='playlist_', errors='ignore')
# df.reset_index()
# print(df.head)
# print(df.count())
# print(df.columns)
#
# print(df["playlist_tracks"].loc[1499][0])  # access df[playlist_tracks].loc[df_index][track_index]
# # Print 1st track of 1500th playlist which is Beyonce 7/11
