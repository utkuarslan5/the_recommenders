import matplotlib.pyplot as plt
from dataset.spotify_million_playlist_dataset.src import *
from dataset.spotify_million_playlist_dataset.src import stats
from scipy.interpolate import make_interp_spline, BSpline

path = ""  # path goes here
[title, artist, track, length, followers] = stats.process_mpd(path)
playlist_length_histogram = sorted(length.items())
x, y = zip(*playlist_length_histogram)
xbar = make_interp_spline(x,y)
ybar = BSpline(xbar)
plt.hist(x, y, bin(20))
plt.xlabel("Number of tracks")
plt.ylabel("Playlists")
plt.text(60, .025, r'$\mu=%s$' % (stats.total_tracks / stats.total_playlists))
plt.grid(True)
plt.title("Playlist length histogram")
plt.show()
