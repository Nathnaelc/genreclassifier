# Purpose: Enrich the cleaned data with Spotify data
import requests
import pandas as pd


def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    if auth_response.status_code == 200:  # Success
        return auth_response.json().get('access_token')
    else:
        print("Failed to obtain access token")
        return None


def enrich_track_data(df, access_token):
    base_url = 'https://api.spotify.com/v1/'
    headers = {'Authorization': f'Bearer {access_token}'}

    for index, row in df.iterrows():
        track_id = row['trackId']
        audio_features_url = f'{base_url}audio-features/{track_id}'
        track_details_url = f'{base_url}tracks/{track_id}'

        # Fetch audio features
        try:
            audio_features_response = requests.get(
                audio_features_url, headers=headers)
            if audio_features_response.status_code == 200:  # Success
                audio_features_data = audio_features_response.json()
                for feature in ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                                'acousticness', 'instrumentalness', 'liveness', 'valence',
                                'tempo', 'duration_ms', 'time_signature']:
                    df.at[index, feature] = audio_features_data.get(feature)
            else:
                print(
                    f"Audio features for track ID {track_id} could not be fetched.")

            # Fetch track details to get artist ID
            track_details_response = requests.get(
                track_details_url, headers=headers)
            if track_details_response.status_code == 200:  # Success
                track_details_data = track_details_response.json()
                artist_id = track_details_data['artists'][0]['id'] if track_details_data['artists'] else None

                # Fetch genres from the artist's data
                if artist_id:
                    artist_url = f'{base_url}artists/{artist_id}'
                    artist_response = requests.get(artist_url, headers=headers)
                    if artist_response.status_code == 200:
                        artist_data = artist_response.json()
                        df.at[index, 'genres'] = ', '.join(
                            artist_data.get('genres', []))
                    else:
                        print(
                            f"Genres for artist ID {artist_id} could not be fetched.")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for track ID {track_id}: {e}")
        except ValueError as e:
            print(
                f"Failed to decode JSON response for track ID {track_id}: {e}")

    return df


# Your Spotify API credentials and access token retrieval
client_id = '42c5a306556842c480894e512ff6726b'
client_secret = 'f09faadcd6304085aa481de32fc808ed'
access_token = get_spotify_access_token(client_id, client_secret)

# Load the cleaned data and enrich it with Spotify data
df_cleaned = pd.read_csv('enriched_combined_csv.csv')

# Assuming 'df_cleaned' is already loaded from 'cleaned_combined_csv.csv'
# Enrich the DataFrame with additional Spotify data
if access_token:
    df_enriched = enrich_track_data(df_cleaned, access_token)
    df_enriched.to_csv('final.csv', index=False)
else:
    print("Could not enrich data without an access token.")
