# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Every song has genre, mood, energy, tempo_bpm, valence, danceability, and acousticness, plus artist. The recipe spends weight on genre, mood, energy and acousticness, becase those four best distinguish songs from each other.
UserProfile stores favorite_genre, favorite_mood, target_energy, and likes_acoustic (boolean). 
Recommender computes scores based on four criteria:
- +2 if song's genre exactly matches user's favorite (+1 if genres are related but not exact match)
- +1 if mood matches
- up to +1.5 based on how close the song's energy is to the user's target_energy
- +0.5 if the song's acousticness is the same as the user's likes_acoustic preference
Songs are chosen by scoring every song in the catalog with the above formula, then sorting the list from highest to lowest, and the top k songs are returend as recommendations.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main`, which runs every profile defined in `src/main.py` — three baseline profiles and several adversarial/edge-case profiles designed to stress-test the scoring logic.

### Baseline Profiles

**High-Energy Pop** — `{genre: pop, mood: happy, energy: 0.9, likes_acoustic: False}`

```
1. Sunrise City  (score: 4.88)
   Neon Echo - pop, happy
     - genre match: pop (+2.0)
     - mood match: happy (+1.0)
     - energy 0.82 is close to target 0.90 (+1.38)
     - matches non-acoustic preference: acousticness=0.18 (+0.5)

2. Gym Hero  (score: 3.96)
   Max Pulse - pop, intense
     - genre match: pop (+2.0)
     - energy 0.93 is close to target 0.90 (+1.46)
     - matches non-acoustic preference: acousticness=0.05 (+0.5)

3. Rooftop Lights  (score: 3.79)
   Indigo Parade - indie pop, happy
     - related genre: indie pop ~ pop (+1.0)
     - mood match: happy (+1.0)
     - energy 0.76 is close to target 0.90 (+1.29)
     - matches non-acoustic preference: acousticness=0.35 (+0.5)

4. Storm Runner  (score: 1.98)
   Voltline - rock, intense
     - energy 0.91 is close to target 0.90 (+1.48)
     - matches non-acoustic preference: acousticness=0.10 (+0.5)

5. Night Drive Loop  (score: 1.77)
   Neon Echo - synthwave, moody
     - energy 0.75 is close to target 0.90 (+1.27)
     - matches non-acoustic preference: acousticness=0.22 (+0.5)
```

**Chill Lofi** — `{genre: lofi, mood: chill, energy: 0.3, likes_acoustic: True}`

```
1. Library Rain  (score: 4.92)
   Paper Lanterns - lofi, chill
     - genre match: lofi (+2.0)
     - mood match: chill (+1.0)
     - energy 0.35 is close to target 0.30 (+1.42)
     - matches acoustic preference: acousticness=0.86 (+0.5)

2. Midnight Coding  (score: 4.82)
   LoRoom - lofi, chill
     - genre match: lofi (+2.0)
     - mood match: chill (+1.0)
     - energy 0.42 is close to target 0.30 (+1.32)
     - matches acoustic preference: acousticness=0.71 (+0.5)

3. Focus Flow  (score: 3.85)
   LoRoom - lofi, focused
     - genre match: lofi (+2.0)
     - energy 0.40 is close to target 0.30 (+1.35)
     - matches acoustic preference: acousticness=0.78 (+0.5)

4. Spacewalk Thoughts  (score: 2.97)
   Orbit Bloom - ambient, chill
     - mood match: chill (+1.0)
     - energy 0.28 is close to target 0.30 (+1.47)
     - matches acoustic preference: acousticness=0.92 (+0.5)

5. Coffee Shop Stories  (score: 1.90)
   Slow Stereo - jazz, relaxed
     - energy 0.37 is close to target 0.30 (+1.40)
     - matches acoustic preference: acousticness=0.89 (+0.5)
```

**Deep Intense Rock** — `{genre: rock, mood: intense, energy: 0.85, likes_acoustic: False}`

```
1. Storm Runner  (score: 4.91)
   Voltline - rock, intense
     - genre match: rock (+2.0)
     - mood match: intense (+1.0)
     - energy 0.91 is close to target 0.85 (+1.41)
     - matches non-acoustic preference: acousticness=0.10 (+0.5)

2. Gym Hero  (score: 2.88)
   Max Pulse - pop, intense
     - mood match: intense (+1.0)
     - energy 0.93 is close to target 0.85 (+1.38)
     - matches non-acoustic preference: acousticness=0.05 (+0.5)

3. Sunrise City  (score: 1.96)
   Neon Echo - pop, happy
     - energy 0.82 is close to target 0.85 (+1.46)
     - matches non-acoustic preference: acousticness=0.18 (+0.5)

4. Rooftop Lights  (score: 1.86)
   Indigo Parade - indie pop, happy
     - energy 0.76 is close to target 0.85 (+1.36)
     - matches non-acoustic preference: acousticness=0.35 (+0.5)

5. Night Drive Loop  (score: 1.85)
   Neon Echo - synthwave, moody
     - energy 0.75 is close to target 0.85 (+1.35)
     - matches non-acoustic preference: acousticness=0.22 (+0.5)
```

### Adversarial / Edge-Case Profiles

**Contradictory: High Energy + Sad** — `{genre: pop, mood: sad, energy: 0.95, likes_acoustic: False}` (mood "sad" doesn't exist in the dataset)

```
1. Gym Hero  (score: 3.97)
   Max Pulse - pop, intense
     - genre match: pop (+2.0)
     - energy 0.93 is close to target 0.95 (+1.47)
     - matches non-acoustic preference: acousticness=0.05 (+0.5)

2. Sunrise City  (score: 3.80)
   Neon Echo - pop, happy
     - genre match: pop (+2.0)
     - energy 0.82 is close to target 0.95 (+1.30)
     - matches non-acoustic preference: acousticness=0.18 (+0.5)

3. Rooftop Lights  (score: 2.71)
   Indigo Parade - indie pop, happy
     - related genre: indie pop ~ pop (+1.0)
     - energy 0.76 is close to target 0.95 (+1.22)
     - matches non-acoustic preference: acousticness=0.35 (+0.5)

4. Storm Runner  (score: 1.94)
   Voltline - rock, intense
     - energy 0.91 is close to target 0.95 (+1.44)
     - matches non-acoustic preference: acousticness=0.10 (+0.5)

5. Night Drive Loop  (score: 1.70)
   Neon Echo - synthwave, moody
     - energy 0.75 is close to target 0.95 (+1.20)
     - matches non-acoustic preference: acousticness=0.22 (+0.5)
```

**Contradictory: Loves Acoustic but Max Energy** — `{genre: rock, mood: intense, energy: 1.0, likes_acoustic: True}` (acoustic preference and max energy pull in opposite directions)

```
1. Storm Runner  (score: 4.37)
   Voltline - rock, intense
     - genre match: rock (+2.0)
     - mood match: intense (+1.0)
     - energy 0.91 is close to target 1.00 (+1.36)

2. Gym Hero  (score: 2.40)
   Max Pulse - pop, intense
     - mood match: intense (+1.0)
     - energy 0.93 is close to target 1.00 (+1.40)

3. Sunrise City  (score: 1.23)
   Neon Echo - pop, happy
     - energy 0.82 is close to target 1.00 (+1.23)

4. Rooftop Lights  (score: 1.14)
   Indigo Parade - indie pop, happy
     - energy 0.76 is close to target 1.00 (+1.14)

5. Midnight Coding  (score: 1.13)
   LoRoom - lofi, chill
     - energy 0.42 is close to target 1.00 (+0.63)
     - matches acoustic preference: acousticness=0.71 (+0.5)
```

**Edge Case: Zero Energy** — `{genre: ambient, mood: relaxed, energy: 0.0, likes_acoustic: True}`

```
1. Spacewalk Thoughts  (score: 3.58)
   Orbit Bloom - ambient, chill
     - genre match: ambient (+2.0)
     - energy 0.28 is close to target 0.00 (+1.08)
     - matches acoustic preference: acousticness=0.92 (+0.5)

2. Coffee Shop Stories  (score: 2.45)
   Slow Stereo - jazz, relaxed
     - mood match: relaxed (+1.0)
     - energy 0.37 is close to target 0.00 (+0.95)
     - matches acoustic preference: acousticness=0.89 (+0.5)

3. Library Rain  (score: 1.48)
   Paper Lanterns - lofi, chill
     - energy 0.35 is close to target 0.00 (+0.98)
     - matches acoustic preference: acousticness=0.86 (+0.5)

4. Focus Flow  (score: 1.40)
   LoRoom - lofi, focused
     - energy 0.40 is close to target 0.00 (+0.90)
     - matches acoustic preference: acousticness=0.78 (+0.5)

5. Midnight Coding  (score: 1.37)
   LoRoom - lofi, chill
     - energy 0.42 is close to target 0.00 (+0.87)
     - matches acoustic preference: acousticness=0.71 (+0.5)
```

**Edge Case: Max Energy** — `{genre: synthwave, mood: focused, energy: 1.0, likes_acoustic: False}`

```
1. Night Drive Loop  (score: 3.62)
   Neon Echo - synthwave, moody
     - genre match: synthwave (+2.0)
     - energy 0.75 is close to target 1.00 (+1.12)
     - matches non-acoustic preference: acousticness=0.22 (+0.5)

2. Gym Hero  (score: 1.90)
   Max Pulse - pop, intense
     - energy 0.93 is close to target 1.00 (+1.40)
     - matches non-acoustic preference: acousticness=0.05 (+0.5)

3. Storm Runner  (score: 1.86)
   Voltline - rock, intense
     - energy 0.91 is close to target 1.00 (+1.36)
     - matches non-acoustic preference: acousticness=0.10 (+0.5)

4. Sunrise City  (score: 1.73)
   Neon Echo - pop, happy
     - energy 0.82 is close to target 1.00 (+1.23)
     - matches non-acoustic preference: acousticness=0.18 (+0.5)

5. Rooftop Lights  (score: 1.64)
   Indigo Parade - indie pop, happy
     - energy 0.76 is close to target 1.00 (+1.14)
     - matches non-acoustic preference: acousticness=0.35 (+0.5)
```

**Edge Case: Out-of-Range Energy** — `{genre: jazz, mood: moody, energy: 1.5, likes_acoustic: True}` (energy above the expected 0-1 range)

```
1. Coffee Shop Stories  (score: 2.31)
   Slow Stereo - jazz, relaxed
     - genre match: jazz (+2.0)
     - energy 0.37 is close to target 1.50 (+-0.19)
     - matches acoustic preference: acousticness=0.89 (+0.5)

2. Night Drive Loop  (score: 1.38)
   Neon Echo - synthwave, moody
     - mood match: moody (+1.0)
     - energy 0.75 is close to target 1.50 (+0.38)

3. Gym Hero  (score: 0.65)
   Max Pulse - pop, intense
     - energy 0.93 is close to target 1.50 (+0.65)

4. Storm Runner  (score: 0.61)
   Voltline - rock, intense
     - energy 0.91 is close to target 1.50 (+0.61)

5. Sunrise City  (score: 0.48)
   Neon Echo - pop, happy
     - energy 0.82 is close to target 1.50 (+0.48)
```

Note the `(+-0.19)` above: when `target_energy` exceeds 1.0, `closeness = 1 - abs(song.energy - target)` goes negative, so `energy_points` becomes negative and the f-string prints a literal double sign. This is a real bug surfaced by the adversarial profile — `score_song` never validates that `target_energy` is within `[0, 1]`.

**Edge Case: Unknown Genre/Mood** — `{genre: polka, mood: melancholy, energy: 0.5, likes_acoustic: False}` (neither value appears anywhere in the dataset)

```
1. Night Drive Loop  (score: 1.62)
   Neon Echo - synthwave, moody
     - energy 0.75 is close to target 0.50 (+1.12)
     - matches non-acoustic preference: acousticness=0.22 (+0.5)

2. Rooftop Lights  (score: 1.61)
   Indigo Parade - indie pop, happy
     - energy 0.76 is close to target 0.50 (+1.11)
     - matches non-acoustic preference: acousticness=0.35 (+0.5)

3. Sunrise City  (score: 1.52)
   Neon Echo - pop, happy
     - energy 0.82 is close to target 0.50 (+1.02)
     - matches non-acoustic preference: acousticness=0.18 (+0.5)

4. Storm Runner  (score: 1.39)
   Voltline - rock, intense
     - energy 0.91 is close to target 0.50 (+0.89)
     - matches non-acoustic preference: acousticness=0.10 (+0.5)

5. Midnight Coding  (score: 1.38)
   LoRoom - lofi, chill
     - energy 0.42 is close to target 0.50 (+1.38)
```

**Edge Case: Genre Only** — `{genre: indie pop}` (sparse profile — mood, energy, and acoustic preference all missing)

```
1. Rooftop Lights  (score: 2.00)
   Indigo Parade - indie pop, happy
     - genre match: indie pop (+2.0)

2. Sunrise City  (score: 1.00)
   Neon Echo - pop, happy
     - related genre: pop ~ indie pop (+1.0)

3. Gym Hero  (score: 1.00)
   Max Pulse - pop, intense
     - related genre: pop ~ indie pop (+1.0)

4. Midnight Coding  (score: 0.00)
   LoRoom - lofi, chill
     - no strong matches on genre, mood, energy, or acousticness

5. Storm Runner  (score: 0.00)
   Voltline - rock, intense
     - no strong matches on genre, mood, energy, or acousticness
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



