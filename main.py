from recommender.Individual.KNN import KNN
from recommender.Group.GroupRecommendation import GroupRecommendation
from recommender.Individual.apriori import Apriori
from recommender.Explanations import Explanations
from recommender.UsersGenerator import UsersGenerator


def main():
    global artists_group, songs_group
    print("\n Generating users . . .")

    num_users = 50
    num_PL_perUser = 10
    # users = UsersGenerator()
    # users.generate_users(num_users, num_PL_perUser)
    #
    # print("Generating the playlists . . .")
    # users_df = users.playlist_assignment()
    # users_df.to_csv('users.csv')
    # print("Generating ratings . . . ")
    # rating_df = users.ratings_by_artists(users_df)
    # rating_df.to_csv('ratings.csv')

    print("Generating individual recommendations KNN . . .")

    art_rec = 15
    song_rec = 15
    neighbours = 5
    target_user = 0
    knn = KNN(neighbours, art_rec)
    knn_artists = knn.recommend_artists(target_user)
    knn_songs = knn.recommend_songs(knn_artists, song_rec)

    # print("Generating groups . . .")
    #
    # total_users_groups = 50
    #
    # g_gen = UsersGenerator()
    # g_gen.generate_users(total_users_groups, num_PL_perUser)
    # groups_df = g_gen.playlist_assignment()
    # groups_df.to_csv('groups_users.csv')
    # g_rating_df = g_gen.ratings_by_artists(groups_df)
    # g_rating_df.to_csv('group_ratings.csv')

    print("Generating Group recommendations with Additive Strategy . . . ")

    art_rec_group = art_rec
    song_rec_group = song_rec
    users_per_group = [2, 4, 6, 10]
    group_rec = GroupRecommendation(art_rec_group)
    for size in users_per_group:
        start_id = 0
        end_id = size
        for i in range(5):
            group = list(range(start_id, end_id))
            print("GROUP: ", group)
            artists_group = group_rec.additive_artists(group)
            songs_group = group_rec.group_songs(artists_group, song_rec_group)
            start_id += size
            end_id += size

    print("\n Generating Apriori . . . ")

    apriori = Apriori()
    features = knn_artists['artist_name'].values.tolist()
    compare = [features[0]]
    support, confidence = 0.0, 0.0
    for feature in features:
        compare.append(feature)
        test_df, spprt, cnfdnce = apriori.calculate_list_support(compare, column='Artist', explain=False)
        flag = 0
        if spprt > support:
            support = spprt
            flag += 1
        if cnfdnce > confidence:
            confidence = cnfdnce
            flag += 1
        if flag >= 1:
            continue
        else:
            compare.pop(-1)
    round(support, 2)
    round(confidence, 2)
    # print(
    #     '\nTotal support for {} is {:.2f} \nand confidence of {} to {} is {:.2f}'.format(compare, support, compare[0],
    #                                                                                      compare[1:], confidence))
    # test_df, support, confidence = apriori.calculate_list_support(features, column='Artist', explain=False)
    # print(
    #     '\nTotal support for {} is {:.2f} \nand confidence of {} to {} is {:.2f}'.format(features, support, features[0],
    #                                                                                      features[1:], confidence))

    explanations = Explanations()
    print("\nGenerating Apriori Explanations . . .")
    explanations.apriori_expl(compare, support, confidence)

    print("\nGenerating Individual Explanations . . .")
    explanations.knn_expl(knn_songs, knn_artists)

    print("\nGenerating Group Explanations . . .")
    explanations.mlp_expl(songs_group, artists_group)

    print('Done!')


if __name__ == "__main__":
    main()
