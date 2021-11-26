import pandas as pd
import math
import random

class GroupRecommendation:
    '''Group Recommendation Strategies'''

    def __init__(self, num_rec):
        self.group_df = pd.read_csv('export/ratings.csv')
        self.num_rec = num_rec

    '''Plurality Voting Strategy 
        group - the list of users that are in the group (cut from all the users)'''
    def pl_voting_artists(self, group):
        group_songs_df = self.group_df.loc[self.group_df['user'].isin(group)]
        rec_artists_df = group_songs_df.groupby(['artist_name'], as_index=False)['rating'].sum()
        rec_artists_df = rec_artists_df.sort_values(by=['rating'], ascending=False)
        rec_artists_df = rec_artists_df[0:self.num_rec]

        # if we want just artist names
        # rec_artists_df = rec_artists_df['artist_name'][0:self.num_rec]

        print('\n Recommended artists with Plurality Voting:')
        print(rec_artists_df)
        return rec_artists_df

    """ Pass a dataframe with the recommended artists and the number of songs that have to be recommended"""
    def group_songs(self, df_ra, num_songs):
        df_artists = df_ra
        df_songs = pd.read_csv('export/songs.csv')

        songs_artist = list(range(0, self.num_rec))
        for i in range(len(df_artists)):
            x = (df_artists['rating'].iloc[i] / df_artists['rating'].sum()) * num_songs
            songs_artist[i] = math.trunc(math.ceil(x))

        print("\n songs per artist: ", songs_artist)

        recommended_songs = list()
        size_dict = df_songs.pivot_table(columns=['artist_name'], aggfunc='size').to_dict()
        k = 0
        for i in songs_artist:
            size = size_dict[df_artists['artist_name'].iloc[k]]
            print("\n----- Amount of songs from  ----- ",df_artists['artist_name'].iloc[k], " ---- ",i)
            for user_index in range(i):

                # get number of songs of each artist
                # print(song_data['track_name'].value_counts()) or down
                # print('size ', size)
                # size = df_artists.loc[df_artists['artist_name'] == df_artists['artist_name'].iloc[k], 'rating'].iloc[0]
                # print(size)
                rand_song = random.sample(range(0,size), size)
                if rand_song[user_index] < size:
                    song = df_songs.loc[df_songs['artist_name'] == df_artists['artist_name'].iloc[k], 'track_name'].iloc[
                        rand_song[user_index]]


                #
                # if song in recommended_songs:
                #     extention += 1
                #     user_index = user_index + extention
                #     print('index ', user_index)
                if song not in recommended_songs:
                    recommended_songs.append(song)
                    print("song number: ", user_index, " is ", song)
            k += 1

        print("\n amount of artists:", k)
        print("\n Recommended songs:")
        print(recommended_songs[0:num_songs])
        print("\n Size of recommended songs: ", len(recommended_songs))
        return recommended_songs

