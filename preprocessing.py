
import matplotlib.pyplot as plt
from dataset.spotify_million_playlist_dataset.src import *
from dataset.spotify_million_playlist_dataset.src import stats

[title, artist, track, length, followers] = stats.process_mpd(
    "D:/PycharmProjects/the_recommenders/dataset/spotify_million_playlist_dataset/subset")
platlist_length_histogram = sorted(length.items())
x, y = zip(*platlist_length_histogram)
plt.plot(x, y, 'k')
plt.xlabel("Number of tracks")
plt.ylabel("Playlists")
plt.text(60, .025, r'$\mu=%s$' % (stats.total_tracks/stats.total_playlists))
plt.grid(True)
plt.title("Playlist length histogram")
plt.show()
