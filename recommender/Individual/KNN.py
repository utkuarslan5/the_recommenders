from sklearn.neighbors import NearestNeighbors
import pandas as pd
import math

class KNN:
    pass
    """ KNN """

    def __init__(self, num_nn, num_rec):
        self.num_rec = num_rec
        self.num_nn = num_nn
        self.df_csv = pd.read_csv('export/ratings.csv')
        self.rating_df = self.df_csv.pivot(index='user', columns='artist_name', values='rating')
        self.rating_df = self.rating_df.fillna(0)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        # print(self.rating_df)
    '''
        Recommend artist based on the most common artists between the neighbours
        Sum the ratings for each artist from all nearest neighbours
    '''
    def recommend_artists(self, target_user):
        knn = NearestNeighbors(n_neighbors=self.num_nn, metric='cosine')
        model = knn.fit(self.rating_df)
        user = self.rating_df.iloc[target_user, ]
        # user_print = user[user != 0]
        # print(user_print.sort_values(ascending=False))

        #user_artists_df = pd.DataFrame({'artist_name': user.index, 'rating': user.values})
        # OR ----------------
        # user_dict = user.to_dict()
        # dict_print = {}
        #
        # for artist, rating in user_dict.items():
        #     if rating != 0:
        #         dict_print[artist] = rating
        #         print(artist, " --- ", rating)

        # The indices contain only the index values of users from the user table.
        distances, indices = model.kneighbors([user])
        global neighbors
        neighbors = indices[0][1:].tolist() # the users that are closest to the user we make a recommendation for

        neighbour_df = self.df_csv.loc[self.df_csv['user'].isin(neighbors)]

        #print(neighbors)
        #print(neighbour_df)

        rec_artists_df = neighbour_df.groupby(['artist_name'], as_index=False)['rating'].sum()
        rec_artists_df = rec_artists_df.sort_values(by=['rating'], ascending=False)
        rec_artists_df = rec_artists_df[0:self.num_rec]

        #if we want just artist names
        #rec_artists_df = rec_artists_df['artist_name'][0:self.num_rec]

        print('\n recommended artists:')
        print(rec_artists_df)

        return rec_artists_df

    '''
        Recommending songs from the nearest neighbours' recommended artists
        Song recommendation heuristics:
            1) songs to recommend = n
            2) songs per artist = ceil((rating(artist)/sum(ratings)) x n)
    '''
    def recommend_songs(self, df_ra, num_songs):
        df_artists = df_ra
        df_songs = pd.read_csv('export/users.csv')
        df_songs = df_songs.loc[df_songs['user'].isin(neighbors)]

        songs_artist = list(range(0,self.num_rec))
        for i in range(len(df_artists)):
            x = (df_artists['rating'].iloc[i]/df_artists['rating'].sum())*num_songs
            songs_artist[i] = math.trunc(math.ceil(x))

        #print("\nsongs per artist: ", songs_artist)
        #print("neighbours list: ", neighbors)

        recommended_songs = list()
        size_dict = df_songs.pivot_table(columns=['artist_name'], aggfunc='size').to_dict()
        k = 0
        for i in songs_artist:
            size = size_dict[df_artists['artist_name'].iloc[k]]
            #print("\n----- Amount of songs from  ----- ",df_artists['artist_name'].iloc[k], " ---- ",i)
            for user_index in range(i):

                #get number of songs of each artist
                #print(song_data['track_name'].value_counts()) or down
                #print('size ', size)
                # size = df_artists.loc[df_artists['artist_name'] == df_artists['artist_name'].iloc[k], 'rating'].iloc[0]
                # print(size)
                if user_index < size:
                    song = df_songs.loc[df_songs['artist_name'] == df_artists['artist_name'].iloc[k], 'track_name'].iloc[user_index]
                #
                # if song in recommended_songs:
                #     extention += 1
                #     user_index = user_index + extention
                #     print('index ', user_index)
                if song not in recommended_songs:
                    recommended_songs.append(song)
                    #print("song number: ", user_index, " is ", song)
            k += 1

        print("\n amount of artists:",k)
        print("\n Recommended songs:")
        print(recommended_songs[0:num_songs])
        print("\n Size of recommended songs: ", len(recommended_songs))

        return recommended_songs[0:num_songs]


