from sklearn.neighbors import NearestNeighbors
import pandas as pd


class KNN:
    pass
    """ KNN """
    def __init__(self):
        #self.df = df #song
        self.df_csv = pd.read_csv('export/ratings.csv')
        self.df_csv.c
        self.rating_df = self.df_csv.pivot(index='user', columns='artist_name', values='rating')
        self.rating_df = self.rating_df.fillna(0)
        # print(song_data.head())
        # print(song_data['track_name'].value_counts())

    def train(self):
        knn = NearestNeighbors(n_neighbors=5, metric='cosine')
        Model = knn.fit(self.rating_df)
        artists = self.rating_df.iloc[1,]

        # The indices contain only the index values of users from the user table.
        distances, indices = Model.kneighbors([artists])
        print("distances: " , distances)
        print("indices (users close to our user): ", indices)
        print("type:", type(indices))
        neighbors = indices[0][1:].tolist() # the users that are closest to the user we make a recommendation for
        print("neighbours: ", neighbors)

        neighbour_df = pd.DataFrame(columns=['user', 'artist_name', 'rating'])
        neighbour_df = self.df_csv[self.df_csv['user'].isin(neighbors)]
        pd.set_option('display.max_rows', 429)

        # print("neighbour dffffffffffffffffffffffffffffffffffff")
        #print(neighbour_df)
        #
        new_df = neighbour_df.groupby(['user','artist_name'], as_index=False)['rating'].sum()
        new_df2 = new_df.sort_values(by=['rating'], ascending=False)
        print(new_df2[0:10])


        Recommended_Song = new_df2['artist_name'][0:10]
        print('recommended songs: ')
        print(Recommended_Song)

        # neighbor_songs = pd.DataFrame(columns=['user', 'artist_name', 'rating'])
        # for item in neighbors:
        #     neighbor_songs = neighbor_songs.append(self.df_csv[self.df_csv.user == item], ignore_index=True)
        # print("neighbour songs:")
        # print(neighbor_songs)
        #
        # # for each artist find the total ratings of all neighbours
        # neighbor_songs = pd.DataFrame({'rating': neighbor_songs['rating'], 'artist_name': neighbor_songs['artist_name']})
        # neighbor_songs = neighbor_songs.groupby(['artist_name']).sum()
        # neighbor_songs = neighbor_songs.sort_values(by=['rating'], ascending=False)
        #
        # print("song listen counts1:")
        # print(neighbor_songs)
        #
        # neighbor_songs = neighbor_songs.sort_values('rating', ascending=False)
        # print("song listen counts2:")
        # print(neighbor_songs)
        #
        # neighbor_songs = neighbor_songs.reset_index(drop=True)
        # print("neighbor songs")
        # print(neighbor_songs)
        #
        # Recommended_Song = neighbor_songs['artist_name'][0:10]
        # print('recommended songs: ')
        # print(Recommended_Song)


