import requests


access_token = "BQDf1irnbJlf_k37RRmW7Eo0I3OhzbViRLARzjPqmsLbhHYKjqlg-768olpvlHz6WkKd2V_Bk8uo8wSygabLS-c7N5KYEdRhusq1XJNYSi4rzhPQBZmeL3Kxose-_M9-TI3Q43QwHhAbC6xm_fw3mVHIlo0ZDYZtAMnx2xJtOOoLQl_pClhzl5bW3sagEadXDxXXSWPF_SZO0hFuANVu7vHf1qE1SLOI6E57codq_RWsMPBpaGLesHG-Jkm60b4dsg"
def get_audio_features_for_playlist(playlist_id, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    # pobierz track_id z playlisty
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    track_ids = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        for item in data['items']:
            track = item.get('track')
            if track and track.get('id'):
                track_ids.append(track['id'])
        url = data.get('next')

    # pobierz audio features batchami po 50
    features = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        ids_param = ",".join(batch)
        r = requests.get(
            f"https://api.spotify.com/v1/audio-features?ids={ids_param}",
            headers=headers
        )
        if r.status_code == 403:
            print(f"Niektóre utwory w batchu {i//50+1} są niedostępne.")
            continue
        r.raise_for_status()
        features.extend([f for f in r.json().get('audio_features', []) if f])
    return features


# === przykład użycia ===
playlist_id = "37i9dQZF1DXcBWIGoYBM5M"  # Twoja playlist ID
audio_features = get_audio_features_for_playlist(playlist_id, access_token)

for f in audio_features:
    if f:  # czasem Spotify zwraca None jeśli utwór niedostępny
        print(f"{f['id']}: BPM={f['tempo']}, Energy={f['energy']}, Danceability={f['danceability']}")
