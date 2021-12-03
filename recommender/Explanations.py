
class Explanations:

    '''Explanations for all recommendations'''

    '''
    Individual:
        <Song> has been recommended to you because it is from the <Artist> that has been
        listened the most by people with similar taste in playlists
    Group:
        <Song> has been recommended to the group because it is from the <Artist> that has been
        listened the most by the group.
    '''
    def knn_expl(self, songs, artist):
        songs_str = " "
        songs_str = songs_str.join(songs)
        artist = artist['artist_name'].iloc[0]
        if len(songs) == 1:
            explanation = songs_str + " has been recommended to you" \
                                      " because it is from the ", artist, " that " \
                                                                          "has been listened the most by people with similar playlists."
        else:
            print("The songs in the playlist:", songs, "\n")
            explanation = "The playlist has been created for you" \
                          " because it is from the artists that " \
                          "have been listened the most by people with similar playlists."

        print(explanation)
        return explanation

    def apriori_expl(self, artist, support, confidence):
        artist_str = " "
        artist_str = artist_str.join(artist[1:])
        explanation = " " + artist[
            0] + " goes well with " + artist_str + " because they have been coupled together in other playlists with " \
            + str(support) + " support and " + str(confidence) + " confidence."
        print(explanation)
        return explanation

    def add_expl(self, songs, artist):
        songs_str = " "
        songs_str = songs_str.join(songs)
        artist = artist['artist_name'].iloc[0]

        if len(songs) == 1:
            explanation = songs_str + " has been recommended to the group " \
                                      "because it is from the ", artist, " that has " \
                                                                         "been listened the most by the group."
        else:
            print("The songs in the playlist:", songs, "\n")
            explanation = "The playlist has been created for the group" \
                          " because it is from the artists that " \
                          "have been listened the most by the group."

        print(explanation)
        return explanation

    def mlp_expl(self, songs, artist):
        songs_str = " "
        songs_str = songs_str.join(songs)
        artist = artist['artist_name'].iloc[0]

        if len(songs) == 1:
            explanation = songs_str + " has been recommended to the group " \
                          "because it is from the ", artist, " that has " \
                          "been listened the most by the group."
        else:
            print("The songs in the playlist:", songs, "\n")
            explanation = "The playlist has been created for the group" \
                          " because it is from the artists that " \
                          "have been listened the most by the group."

        print(explanation)
        return explanation