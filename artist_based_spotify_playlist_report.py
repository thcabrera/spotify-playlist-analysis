import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

artists_data = {} # id -> name, count

def get_playlist_id_from_link(link):
    return link[link.rindex('/') + 1:link.index('?')]

def process_artist(a_id, a_name):
    if a_id not in artists_data:
        artists_data[a_id] = {
            "name": a_name,
            "count": 0
        }
    artists_data[a_id]["count"] += 1
    
def print_results(total):
    ordered_data = dict(sorted(artists_data.items(), key=lambda item: item[1]["count"], reverse=True))
    i = 0
    for a_id in ordered_data:
        i += 1
        count = artists_data[a_id]["count"]
        print(f'[{i}] {artists_data[a_id]["name"]} - {count} - {"%.2f" % (count / total * 100)}% ')

def process_tracks(tracks):
    for item in tracks["items"]:
        for artist in item["track"]["artists"]:
            artist_id = artist["id"]
            artist_name = artist["name"]
            process_artist(artist_id, artist_name)

def has_next_track(total, offset_counter):
    return offset_counter < total

if __name__ == "__main__":

    CLIENT_ID = ""
    SPOTIPY_CLIENT_SECRET = ""

    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    p = input("Enter a link to a spotify playlist: ")
    p_id = get_playlist_id_from_link(p)
    playlist = sp.playlist(p_id)["tracks"]
    total = playlist["total"]
    offset_counter = 0
    process_tracks(playlist)
    while has_next_track(total, offset_counter):
        offset_counter += len(playlist["items"])
        playlist = sp.playlist_tracks(playlist_id = p_id,
                                       offset=offset_counter)
        process_tracks(playlist)
    print_results(total)