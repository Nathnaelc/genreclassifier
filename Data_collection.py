# For data collection from Spotify API
import pandas as pd
import json

# Load the JSON data
with open('Playlist1.json', 'r') as file:
    data = json.load(file)


def export_playlist_to_csv(playlist_name, playlist_items, file_name):
    tracks_data = []
    for item in playlist_items:
        track = item['track']
        if track:  # Ensure there is track data
            tracks_data.append({
                'trackId': track['trackUri'].split(':')[-1],
                'trackName': track['trackName'],
                'artistName': track['artistName'],
                'albumName': track['albumName']
            })
    df_tracks = pd.DataFrame(tracks_data)
    df_tracks.to_csv(file_name, index=False)


# Example: Export 'Reserve' and 'Summer Workout' playlists to CSV
for playlist in data['playlists']:
    if playlist['name'] in ['Reserve', 'Summer Workout', 'Progressive house', 'Unconditional']:
        file_name = f"{playlist['name'].replace(' ', '_')}.csv"
        export_playlist_to_csv(playlist['name'], playlist['items'], file_name)
