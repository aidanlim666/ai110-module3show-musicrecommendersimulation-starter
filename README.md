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

Output of `python -m src.main` for the default pop/happy/energy=0.8 profile:

```
User profile: genre=pop, mood=happy, energy=0.8
============================================================

1. Sunrise City  (score: 4.47)
   Neon Echo - pop, happy
     - genre match: pop (+2.0)
     - mood match: happy (+1.0)
     - energy 0.82 is close to target 0.80 (+1.47)

2. Rooftop Lights  (score: 3.44)
   Indigo Parade - indie pop, happy
     - related genre: indie pop ~ pop (+1.0)
     - mood match: happy (+1.0)
     - energy 0.76 is close to target 0.80 (+1.44)

3. Gym Hero  (score: 3.30)
   Max Pulse - pop, intense
     - genre match: pop (+2.0)
     - energy 0.93 is close to target 0.80 (+1.30)

4. Night Drive Loop  (score: 1.42)
   Neon Echo - synthwave, moody
     - energy 0.75 is close to target 0.80 (+1.42)

5. Storm Runner  (score: 1.33)
   Voltline - rock, intense
     - energy 0.91 is close to target 0.80 (+1.33)
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



