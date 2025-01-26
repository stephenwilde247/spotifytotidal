#  ____  _                       ___   ___  
# / ___|| |_ _____   ________ _ / _ \ / _ \ 
# \___ \| __/ _ \ \ / /_  / _` | (_) | | | |
#  ___) | ||  __/\ V / / / (_| |\__, | |_| |
# |____/ \__\___| \_/ /___\__,_|  /_/ \___/ 
#          Spotify to Tidal
        

import os
import csv
import tidalapi
import time

# To export your playlists go to here https://exportify.net/

# Authenticate with Tidal
def authenticate_tidal():
    """Authenticate with Tidal using OAuth."""
    session = tidalapi.Session()
    session.login_oauth_simple()  # Needed auth link
    return session

# Fetch track data from a CSV file
def fetch_tracks_from_csv(csv_file):
    """Fetch track data from a CSV file."""
    tracks = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tracks.append({
                "Track Name": row["Track Name"],  # Correct column name for track
                "Artist": row["Artist Name(s)"]   # Correct column name for artist
            })
    return tracks

# Create a playlist and add tracks to it
def add_tracks_to_tidal(tidal_session, tracks, playlist_name):
    """Create a new playlist in Tidal and add tracks."""
    user = tidal_session.user
    description = ""  # Add an empty string as description you can change this

    try:
        # Create the playlist with the name
        tidal_playlist = user.create_playlist(title=playlist_name, description=description)
        print(f"Created playlist: {playlist_name}")

        for track in tracks:
            search_query = f'{track["Track Name"]} {track["Artist"]}'
            search_results = tidal_session.search(search_query)
            print(f"Searching for: {search_query}")
            
            if 'tracks' in search_results and search_results['tracks']:
                tidal_track = search_results['tracks'][0]  # Get the first track from the search results
                print(f"Found track: {track['Track Name']} by {track['Artist']} (Track ID: {tidal_track.id})")
                
                # Add the track to the playlist
                tidal_playlist.add([tidal_track.id])  # Using add() to add tracks
                print(f"Added {track['Track Name']} to playlist.")
            else:
                print(f"Track '{track['Track Name']}' by {track['Artist']} not found in search results.")
            
            time.sleep(1)  # To avoid hitting rate limits
            
    except Exception as e:
        print(f"Error adding tracks to playlist: {e}")

def main():
    # Authenticate with Tidal
    tidal_session = authenticate_tidal()

    
    playlists_folder = "allPlaylists" 

    # This will loop over all the csv files
    for filename in os.listdir(playlists_folder):
        if filename.endswith(".csv"):
            playlist_file = os.path.join(playlists_folder, filename)
            print(f"Processing playlist: {filename}")

            # Read tracks from the CSV file (Finaly fucking fixed this)
            tracks = fetch_tracks_from_csv(playlist_file)

            # Create a Tidal playlist with the same name as the CSV file (without the extension)
            playlist_name = os.path.splitext(filename)[0]

            # Add tracks to Tidal
            add_tracks_to_tidal(tidal_session, tracks, playlist_name)

def end():
    print("All playlists should have been cmpleted")
    
if __name__ == "__main__":
    main()
    end()
