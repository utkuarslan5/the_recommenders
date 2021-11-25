from KNN import KNN
from Users import Users

def main():

    print("Generating users . . .")

    num_users = 11
    # num_PL_perUser = 2
    # users = Users()
    # users.generate_users(num_users,num_PL_perUser)
    #
    # print("Generating the playlists . . .")
    # df = users.playlist_assignment()
    #
    # print("Generating ratings . . . ")
    # rating_df = users.ratings_by_artists(df)

    print("Loading recommendations KNN . . .")

    art_rec = 10
    song_rec = 50
    neighbours = 5
    knn = KNN(neighbours, art_rec)
    artists = knn.recommend_artists()
    songs = knn.recommend_songs(artists, song_rec)

if __name__ == "__main__":
   main()