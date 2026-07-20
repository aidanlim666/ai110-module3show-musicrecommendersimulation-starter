"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Baseline profiles: each leans clearly into one genre/mood/energy combo,
# so the top recommendations should make intuitive sense.
USER_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.85, "likes_acoustic": False},

    # --- Adversarial / edge-case profiles ---
    # Contradiction: wants a hyped-up energy level but a "sad" mood that
    # (per data/songs.csv) doesn't even appear in the dataset's mood column.
    "Contradictory: High Energy + Sad": {"genre": "pop", "mood": "sad", "energy": 0.95, "likes_acoustic": False},

    # Contradiction: claims to like acoustic songs but sets energy to the max,
    # which pulls toward loud/electric tracks, i.e. two preferences pulling
    # opposite directions on the same axis.
    "Contradictory: Loves Acoustic but Max Energy": {"genre": "rock", "mood": "intense", "energy": 1.0, "likes_acoustic": True},

    # Boundary values: energy pinned at the extremes (0.0 and 1.0) to check
    # the closeness math (1 - abs(song_energy - target)) doesn't break at edges.
    "Edge Case: Zero Energy": {"genre": "ambient", "mood": "relaxed", "energy": 0.0, "likes_acoustic": True},
    "Edge Case: Max Energy": {"genre": "synthwave", "mood": "focused", "energy": 1.0, "likes_acoustic": False},

    # Out-of-range energy (should be clamped/handled gracefully, not just
    # trusted, since a real UI could pass bad input).
    "Edge Case: Out-of-Range Energy": {"genre": "jazz", "mood": "moody", "energy": 1.5, "likes_acoustic": True},

    # Unknown genre/mood not present anywhere in the dataset, to confirm the
    # recommender falls back sensibly instead of erroring or matching nothing
    # in a confusing way.
    "Edge Case: Unknown Genre/Mood": {"genre": "polka", "mood": "melancholy", "energy": 0.5, "likes_acoustic": False},

    # Sparse profile: only genre is set, everything else is missing, to check
    # that score_song tolerates missing keys instead of raising.
    "Edge Case: Genre Only": {"genre": "indie pop"},
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== Profile: {name} ===")
        print(f"Preferences: {user_prefs}")
        print("=" * 60)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']}  (score: {score:.2f})")
            print(f"   {song['artist']} - {song['genre']}, {song['mood']}")
            for reason in explanation.split("; "):
                print(f"     - {reason}")

        print()


if __name__ == "__main__":
    main()
