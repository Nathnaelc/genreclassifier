# Purpose: Clean the final.csv dataset and map detailed genres to broad categories
import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('final.csv')  # Update the path

# Define a mapping of detailed genres to broad categories
genre_mapping = {
    # EDM
    'edm': 'EDM', 'electro house': 'EDM', 'progressive electro house': 'EDM',
    'dutch house': 'EDM', 'big room': 'EDM', 'melodic dubstep': 'EDM',
    'brostep': 'EDM', 'dutch edm': 'EDM', 'future bass': 'EDM',
    'progressive trance': 'EDM', 'house': 'EDM', 'indietronica': 'EDM',
    'complextro': 'EDM', 'slap house': 'EDM', 'canadian electronic': 'EDM',
    'vapor twitch': 'EDM', 'electronic trap': 'EDM', 'stutter house': 'EDM',
    'bass trap': 'EDM', 'australian dance': 'EDM', 'trance': 'EDM',
    'future house': 'EDM', 'german techno': 'EDM', 'belgian edm': 'EDM',
    'swedish tropical house': 'EDM', 'melbourne bounce': 'EDM', 'trancecore': 'EDM',
    'belgian dance': 'EDM', 'gaming edm': 'EDM', 'progressive house': 'EDM', 'tropical house': 'EDM',
    'metropopolis': 'EDM', 'uk dance': 'EDM', 'sky room': 'EDM', 'hopebeat': 'EDM', 'dubstep': 'EDM',
    'swedish electropop': 'EDM', 'electropowerpop': 'EDM',

    # Pop
    'pop': 'Pop', 'pop edm': 'Pop', 'pop dance': 'Pop', 'dance pop': 'Pop', 'canadian pop': 'Pop', 'uk pop': 'Pop',
    'nyc pop': 'Pop', 'pop rap': 'Pop', 'shimmer pop': 'Pop',
    'swedish pop': 'Pop', 'la pop': 'Pop', 'singer-songwriter pop': 'Pop',
    'norwegian pop': 'Pop', 'australian pop': 'Pop', 'danish pop': 'Pop',
    'russian edm': 'Pop', 'australian electropop': 'Pop', 'pop soul': 'Pop',
    'latin pop': 'Pop', 'indian edm': 'Pop', 'korean r&b': 'Pop',
    'uk alternative pop': 'Pop', 'pop nacional': 'Pop', 'italian pop': 'Pop',
    'nz pop': 'Pop', 'latin viral pop': 'Pop', 'pop rock': 'Pop',
    'pop emo': 'Pop', 'pop punk': 'Pop', 'mellow gold': 'Pop',
    'candy pop': 'Pop', 'irish pop': 'Pop', 'piano rock': 'Pop',

    # Indie/Alternative
    'indie poptimism': 'Indie/Alternative', 'alt z': 'Indie/Alternative',
    'indie electropop': 'Indie/Alternative', 'modern indie pop': 'Indie/Alternative',
    'indie pop': 'Indie/Alternative', 'indie pop rap': 'Indie/Alternative',
    'indie anthem-folk': 'Indie/Alternative', 'modern alternative rock': 'Indie/Alternative',
    'indie r&b': 'Indie/Alternative', 'swedish indie': 'Indie/Alternative',
    'neo-synthpop': 'Indie/Alternative', 'post-teen pop': 'Indie/Alternative',
    'neon pop punk': 'Indie/Alternative', 'indie rock': 'Indie/Alternative',
    'modern rock': 'Indie/Alternative', 'celtic rock': 'Indie/Alternative',
    'country pop': 'Indie/Alternative', 'folk-pop': 'Indie/Alternative',
    'chill r&b': 'Indie/Alternative', 'uk contemporary r&b': 'Indie/Alternative',
    'canadian contemporary r&b': 'Indie/Alternative', 'indie pop': 'Indie/Alternative',
    'french indie pop': 'Indie/Alternative', 'pov: indie': 'Indie/Alternative',
    'contemporary country': 'Indie/Alternative',
}


# Function to map detailed genres to broad categories
def map_genre_to_category(genre_list, mapping):
    # Initialize an empty set to hold broad genres for this track
    broad_genres = set()

    # Check for NaN and return None to filter these out later
    if pd.isna(genre_list):
        return None

    for genre in genre_list.split(', '):
        if genre in mapping:
            broad_genres.add(mapping[genre])
            break  # Break after adding the first matched broad genre

    # Return the first genre in the set or None if no match was found
    return list(broad_genres)[0] if broad_genres else None


# Apply the updated mapping function
df['broad_genre'] = df['genres'].apply(
    map_genre_to_category, args=(genre_mapping,))

# Drop rows where 'broad_genre' is None (tracks that couldn't be classified into any main genre)
df = df.dropna(subset=['broad_genre'])

# Fill missing audio features with the median of each column
audio_features_cols = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
df[audio_features_cols] = df[audio_features_cols].fillna(
    df[audio_features_cols].median())

# Save the cleaned and genre-labeled dataset
df.to_csv('cleaned_and_genre_mapped_final.csv', index=False)
