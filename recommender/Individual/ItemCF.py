import numpy as np
import pandas as pd

from pandas.api.types import CategoricalDtype
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


class ItemCF:
    def __init__(self, target_playlist_id, num_seed, k, len_threshold):
        """
        Parameters
        ----------
        target_playlist_id : int
            Unique identifier of a playlist for which we're trying to suggest songs
        num_seed : int
            Number of seed tracks used to create recommendations
        k : int
            The parameter for kNN algorithm in order to find top k most similar songs to the seed track
        """
        self.target_playlist_id = target_playlist_id
        self.num_seed = num_seed
        self.k = k
        self.len_threshold = len_threshold

    def get_seed_tracks(self, df):
        """Randomly picks num_seed songs from the target playlist to serve as seed tracks. Song recommendations will be
        created based on the similarity to seed tracks.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing full information about playlists and songs

        Returns
        -------
        seed_track_ids
            Unique song identifiers of seed tracks
        """
        seed_track_ids = df.loc[df.pid == self.target_playlist_id].sample(n=self.num_seed).tid.tolist()
        return seed_track_ids

    def filter_by_playlist_length(self, df):
        """Filters a given dataframe to contain only playlist with more than len_threshold songs.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing full information about playlists and songs
        len_threshold : int
            Threshold used to filter a dataframe based on playlist length

        Returns
        -------
        filtered_df
            Filtered dataframe containing only playlists longer than len_threshold
        """
        filtered_df = df.groupby('pid').filter(lambda x: len(x) > self.len_threshold).copy()
        return filtered_df

    def create_playlist_song_matrix(self, df):
        """Creates a binary playlist-song matrix with unique playlist identifiers as rows and unique song identifiers
        as columns. An entry of a matrix is 1 if a song is contained in the playlist, 0 otherwise.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing full information about playlists and songs

        Returns
        -------
        pt_df
            Dataframe which stores a binary playlist-song matrix
        """
        # create playlist and song categories
        playlist_type = CategoricalDtype(df['pid'].unique(), ordered=True)
        song_type = CategoricalDtype(df['tid'].unique(), ordered=True)

        # creation of a playlist-song matrix using a compressed row matrix format
        # this is necessary because sparsity prevents us from using groupby or pivot on dataframe directly
        row = df['tid'].astype(song_type).cat.codes
        col = df['pid'].astype(playlist_type).cat.codes
        sparse_matrix = csr_matrix((df['count'], (row, col)),
                                   shape=(song_type.categories.size, playlist_type.categories.size))

        # convert back to dataframe
        # CSR helps avoid issues with memory and computational complexity but has rather limiting indexing options
        pt_df = pd.DataFrame(sparse_matrix.todense(), index=song_type.categories, columns=playlist_type.categories)
        return pt_df

    def exclude_target_playlist_songs(self, df, seed_track_id):
        """Creates a slice of a dataframe containing a playlist-song matrix which excludes the songs which are already
        in the target playlist. This is necessary because the goal is to recommend songs which are not present in the playlist.
        The seed track is kept in order to compute the similarities with other songs.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing a binary playlist-song matrix

        seed_track_id : int
            Unique identifier of a seed track

        Returns
        -------
        slice_df
            Dataframe which stores a binary playlist-song matrix excluding the songs already present in the playlist
        """
        song_ids = df.loc[df[self.target_playlist_id] == 1].index.tolist()
        song_ids.remove(seed_track_id)
        slice_df = df[~df.index.isin(song_ids)].copy()
        return slice_df

    def find_k_most_similar_songs(self, df, seed_track_id):
        """Finds k most similar songs to the seed track using a kNN algorithm with a cosine similarity as a similarity measure.
        The songs are considered more similar if they co-occur more often across different playlists.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing a binary playlist-song matrix excluding the songs which are already in the playlist

        seed_track_id : int
            Unique identifier of a seed track

        Returns
        -------
        sim_tracks_id
            List of unique song identifiers for the top k most similar songs to the seed track

        track_distances
            List of distances between a seed track and top k most similar songs to it
        """
        # exclude songs already in the target playlist
        slice_df = self.exclude_target_playlist_songs(df, seed_track_id)

        # apply knn to get top k most similar tracks to the seed track
        # n_neighbors is k+1 because the algorithm will return the seed track itself among most similar ones
        knn = NearestNeighbors(metric='cosine', algorithm='brute')
        knn.fit(csr_matrix(slice_df.values))
        distances, indices = knn.kneighbors(csr_matrix(slice_df.values), n_neighbors=self.k + 1)

        # to get actual cosine similarities since sklearn outputs distances
        distances = 1 - distances

        # retrieve ids of top k most similar tracks and their distances to the seed track
        seed_track_loc = slice_df.index.get_loc(seed_track_id)
        track_distances = distances[seed_track_loc].tolist()
        sim_tracks_loc = indices[seed_track_loc].tolist()
        sim_tracks_id = slice_df.iloc[sim_tracks_loc, :].index.tolist()

        # remove the seed track itself from list of ids and distances
        track_distances.pop(0)
        sim_tracks_id.pop(0)

        return sim_tracks_id, track_distances

    def get_song_and_artist_name(self, df, song_id):
        """Given a unique song identifier, returns a song and artist name.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing full information about playlists and songs
        song_id : int
            Unique id of a song for which we need a name and an artist

        Returns
        -------
        song_name
            Name of a song
        artist_name
            Name of an artist performing a song
        """
        song_df = df.drop(['pid', 'playlist'], axis=1).sort_values(by=['tid']).copy()
        song_df.drop_duplicates(subset=['tid'], inplace=True)

        song_name = song_df.loc[song_df.tid == song_id, 'track_name'].item()
        artist_name = song_df.loc[song_df.tid == song_id, 'artist_name'].item()

        return song_name, artist_name

    def get_playlist_name(self, df, playlist_id):
        """Given a unique playlist identifier, returns a playlist name.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing full information about playlists and songs
        playlist_id : int
            Unique id of a playlist for which we need a name

        Returns
        -------
        playlist
            Name of a playlist
        """
        playlist_df = df.drop(['track_name', 'artist_name', 'album_name', 'tid'], axis=1).sort_values(by=['pid']).copy()
        playlist_df.drop_duplicates(subset=['pid'], inplace=True)

        playlist = playlist_df.loc[playlist_df.pid == playlist_id, 'playlist'].item()
        return playlist

    def get_song_recommendation(self, df, seed_track_id, similar_song_id):
        """Given a dataframe, seed track identifier and an identifier of a similar song, it prints out a recommendation of
        a similar song based on its similarity to the seed track.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing full information about playlists and songs
        seed_track_id : int
            Unique id of a playlist for which we need a name
        similar_song_id : int
            Unique id of a song to be recommended based on its similarity to the seed track
        """
        (seed_track_name, seed_track_artist) = self.get_song_and_artist_name(df, seed_track_id)
        (song_name, artist_name) = self.get_song_and_artist_name(df, similar_song_id)

        print('Suggested song for your playlist ' + self.get_playlist_name(df, self.target_playlist_id) +
              ' is ' + song_name + ' by ' + artist_name + ' based on its similarity to ' + seed_track_name +
              ' by ' + seed_track_artist + '.')
        print()

    def calculate_song_idf(self, df, song_id):
        """Given a unique song identifier, calculate inverse document frequency using a formula
        log10(|P|/|Pt|) where P is the set of all playlists and Pt is the set of all playlists containing
        a given song.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing a binary playlist-song matrix
        playlist_id : int
            Unique id of a song for which we need to calculate idf

        Returns
        -------
        idf
            Inverse document frequency of a given song
        """
        idf = np.log10(len(df.columns) / df.loc[df.index == song_id].sum(axis=1).item())
        return idf

    def execute(self, df):
        """Given a dataframe with information about songs and playlists, it executes an item-based collaborative filtering
        algorithm in order to create song recommendations for a target playlist.

        Parameters
        ----------
        df : DataFrame
            Pandas dataframe containing full information about songs and playlists
        """
        # filter playlists by length
        filtered_df = self.filter_by_playlist_length(df)
        # create binary playlist-song matrix
        pt_df = self.create_playlist_song_matrix(filtered_df)

        # randomly choose seed tracks
        seed_ids = self.get_seed_tracks(df)

        all_recs_id, all_distances = [], []

        # find k most similar songs to each seed track
        for seed_track_id in seed_ids:
            sim_tracks_id, track_distances = self.find_k_most_similar_songs(pt_df, seed_track_id)
            all_recs_id.extend(sim_tracks_id)
            all_distances.extend(track_distances)

        # calculate final similarity scores by using idf as weight for each song and get final recommendations
        final_sim_scores = [all_distances[i] * self.calculate_song_idf(pt_df, all_recs_id[i]) for i in
                            range(0, len(all_recs_id))]
        final_recs = [all_recs_id for _, all_recs_id in sorted(zip(final_sim_scores, all_recs_id), reverse=True)]
        final_recs = list(set(final_recs))

        # get song recommendations
        for similar_song_id in final_recs:
            self.get_song_recommendation(filtered_df, seed_track_id, similar_song_id)