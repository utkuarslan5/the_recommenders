import pandas as pd
import random


class Users:
    """ Generate users with random unique playlists """
    def __init__(self):
        self.dict = {}
        print('heloooooooooooooooooooooooooooooo')
        self.song_data = pd.read_csv('songs.csv')
        #
        # print(song_data.head())
        # print(song_data['track_name'].value_counts())

    def generate_users(self, num_users, num_PL_user):
        playlists_rand = random.sample(range(0,4000), 4000)
        k = 0
        for i in range(num_users):
            arr = [0 for x in range(num_PL_user)]
            for j in range(num_PL_user):
                arr[j] = playlists_rand[k]
                k += 1

            self.dict[i] = arr

        print(self.dict)
        return self.dict

    """ Create ratings based on the number of times an artist appears in all of the playlists"""
    def ratings_by_artists(self, df):
        rating_df = df
        rating_df['rating'] = 1
        print(rating_df)
        rating_df = rating_df.groupby(['user', 'artist_name']).sum()
        print(rating_df)
        #rating_df.groupby(['artist_name']).count().reset_index()
        rating_df = rating_df.sort_values(by=['user','rating', 'artist_name'], ascending=False)
        pd.set_option('display.max_columns', None)
        print(rating_df)
        rating_df.to_csv('ratings.csv')
        return rating_df

    """ Create a dataframe which has the songs of each playlist of each user """
    def playlist_assignment(self):
        user_id, pid, playlist_name, track_name2, artist_name, album_name= [], [], [], [], [], []

        for user in self.dict:
            for playlist in self.dict[user]:
                pl_tracks = self.song_data[self.song_data['pid'] == playlist]['track_name'] # take all songs from one playlist
                print('for loop startttttttttttttttttt')
                for i in range(len(pl_tracks)): # take every song in the playlist
                    pl_track = pl_tracks.values[i] # take one song from the playlist
                    user_id.append(user) # append the user id
                    pid_val = playlist
                    pl_name_val = self.song_data.loc[self.song_data['pid'] == playlist, 'playlist'].iloc[0]
                    artist = self.song_data.loc[self.song_data['track_name'] == pl_track, 'artist_name'].iloc[0]
                    alb_name = self.song_data.loc[self.song_data['track_name'] == pl_track, 'album_name'].iloc[0]
                    pid.append(pid_val)
                    playlist_name.append(pl_name_val)
                    track_name2.append(pl_track)
                    artist_name.append(artist)
                    album_name.append(alb_name)

        users_df = pd.DataFrame([user_id, pid, playlist_name, track_name2, artist_name, album_name]).T
        users_df.columns = ['user', 'pid', 'playlist', 'track_name', 'artist_name', 'album_name']
        pd.set_option('display.max_columns', None)
        rating_df = users_df.sort_values(by=['user', 'pid', 'artist_name'])
        print(rating_df.head(2))
        rating_df.to_csv('users.csv')
        return users_df