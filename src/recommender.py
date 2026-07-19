import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv into a list of dicts, converting numeric fields to int/float."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            for field in int_fields:
                song[field] = int(song[field])
            for field in float_fields:
                song[field] = float(song[field])
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences using the weighted recipe from the README; returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    user_genre = (user_prefs.get("genre") or user_prefs.get("favorite_genre") or "").lower()
    song_genre = (song.get("genre") or "").lower()
    if user_genre and song_genre:
        if song_genre == user_genre:
            score += 2.0
            reasons.append(f"genre match: {song['genre']} (+2.0)")
        elif user_genre in song_genre or song_genre in user_genre:
            score += 1.0
            reasons.append(f"related genre: {song['genre']} ~ {user_prefs.get('genre') or user_prefs.get('favorite_genre')} (+1.0)")

    user_mood = (user_prefs.get("mood") or user_prefs.get("favorite_mood") or "").lower()
    song_mood = (song.get("mood") or "").lower()
    if user_mood and song_mood and song_mood == user_mood:
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    target_energy = user_prefs.get("energy", user_prefs.get("target_energy"))
    if target_energy is not None and song.get("energy") is not None:
        closeness = 1 - abs(song["energy"] - target_energy)
        energy_points = 1.5 * closeness
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} is close to target {target_energy:.2f} (+{energy_points:.2f})"
        )

    likes_acoustic = user_prefs.get("likes_acoustic", user_prefs.get("acoustic"))
    acousticness = song.get("acousticness")
    if likes_acoustic is not None and acousticness is not None:
        if likes_acoustic and acousticness >= 0.6:
            score += 0.5
            reasons.append(f"matches acoustic preference: acousticness={acousticness:.2f} (+0.5)")
        elif not likes_acoustic and acousticness <= 0.4:
            score += 0.5
            reasons.append(f"matches non-acoustic preference: acousticness={acousticness:.2f} (+0.5)")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts by score descending, and returns the top k as (song, score, explanation)."""
    judged = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches on genre, mood, energy, or acousticness"
        judged.append((song, score, explanation))

    judged.sort(key=lambda item: item[1], reverse=True)

    return judged[:k]
