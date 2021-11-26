from recommender.Individual.KNN import KNN
from recommender.Group.GroupRecommendation import GroupRecommendation
from recommender.Individual.apriori import Apriori


def main():
    print("Generating users . . .")

    num_users = 11
    num_PL_perUser = 2
    # users = UsersGenerator()
    # users.generate_users(num_users,num_PL_perUser)
    #
    # print("Generating the playlists . . .")
    # users_df = users.playlist_assignment()
    # users_df.to_csv('users.csv')
    # print("Generating ratings . . . ")
    # rating_df = users.ratings_by_artists(users_df)
    # rating_df.to_csv('ratings.csv')

    print("Generating individual recommendations KNN . . .")

    art_rec = 10
    song_rec = 10
    neighbours = 5
    target_user = 0
    knn = KNN(neighbours, art_rec)
    artists = knn.recommend_artists(target_user)
    songs = knn.recommend_songs(artists, song_rec)

    print("Generating groups . . .")

    # total_users_groups = 50
    #
    # g_gen = UsersGenerator()
    # g_gen.generate_users(total_users_groups, num_PL_perUser)
    # groups_df = g_gen.playlist_assignment()
    # groups_df.to_csv('groups_users.csv')
    # g_rating_df = g_gen.ratings_by_artists(groups_df)
    # g_rating_df.to_csv('group_ratings.csv')

    # print("Done")

    print("Generating Group recommendations with Plurality Voting . . . ")

    art_rec_group = 10
    song_rec_group = 10
    users_per_group = []
    group_rec = GroupRecommendation(song_rec_group)
    group = [0, 1, 2, 3, 4, 5]
    artists_group = group_rec.pl_voting_artists(group)
    songs_group = group_rec.group_songs(artists_group, song_rec)

    print("\n Generating Apriori . . . ")

    apriori = Apriori()
    test_df = apriori.calculate_pair_support('Killing Me Softly', 'Get Lucky', column='Album')
    test_df.to_csv('test.csv')
    print('Done!')


if __name__ == "__main__":
    main()
