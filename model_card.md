# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

SongSearcher

---

## 2. Intended Use  

SongSearcher is a song recommender that recommends songs based on a 10-track catalog.
---

## 3. How the Model Works  

Every song in the catalog has a genre, a mood, an energy level (0 to 1), and an "acousticness" level (0 to 1), along with title, artist, tempo, valence, and danceability that aren't currently used in scoring. A user profile states a favorite genre, a favorite mood, a target energy level, and whether they like acoustic music.
The recommender scores a song by adding up points from all four independent categories.
---

## 4. Data  

The data has 10 songs total, with genres pop, lofi, rock, ambient, jazz, synthwave, and indie pop.
Lofi is the best-covered genre with 3 songs, pop has 2 (plus 1 indie pop that partially counts as related), and rock, ambient, jazz, and synthwave each have exactly 1 song.
Moods represented are chill, happy, intense, relaxed, moody, focused.
---

## 5. Strengths  


The recommender works best for users whose taste sits near the "center of mass" of the catalog — pop or lofi fans at mid-range energy get a well-differentiated top 5. The scoring logic captures the patterns I'd expect: strong all-around matches float to the top, energy-closeness correctly finds the nearest song even at extreme targets, and contradictory profiles get penalized sensibly rather than canceling out into a misleading score. The explanation strings make it easy to see what drove each score, which made the ranking logic straightforward to verify during testing.
---

## 6. Limitations and Bias 

Energy gap and genre matching formulas both structurally favo users whose taste centers on the catalog's most common values, not just users with compatible taste. The energy score is capped by the dataset's actual energy range, so a user who likes very low or very high energy music can never score as high as a medium range user.

---

## 7. Evaluation  

I ran the recommender against 10 user profiles.
The biggest surprise was that of the out of range energy profile, which produced a negative per-field score.

*High-Energy Pop vs. Chill Lofi** — High-Energy Pop's top pick (Sunrise City, 4.88) is driven by a near-max energy target (0.9) matched against a genuinely upbeat pop song, while Chill Lofi's top pick (Library Rain, 4.92) rewards low energy (0.3) and high acousticness (0.86). This makes sense: the two profiles are near-opposites on the energy axis and the scoring formula is symmetric around the target, so it correctly surfaces different songs rather than converging on a middle ground.

**Chill Lofi vs. Deep Intense Rock** — Chill Lofi's top 3 all score above 3.8 (three real lofi/chill songs exist), whereas Deep Intense Rock's #2 result already drops to 2.88. This is not a flaw in either profile's logic — it reflects that the catalog has 3 lofi songs but only 1 rock song, so "intense rock" simply runs out of good matches faster. It shows the recommender is honest about catalog coverage, even if it doesn't say so explicitly.

**High-Energy Pop vs. Deep Intense Rock** — Both target high energy (0.9 vs 0.85) and both surface Gym Hero and Sunrise City in their top 5, but in different order and with different reasoning strings (genre match vs. only mood/energy match) — confirming genre is doing real ranking work on top of the shared energy signal, not just energy alone.

**High-Energy Pop vs. Contradictory: High Energy + Sad** — Same genre and nearly the same energy target, but "sad" isn't a mood in the dataset, so the Contradictory profile's mood line disappears from every explanation and its scores are uniformly ~0.9 lower than High-Energy Pop's for the same songs (e.g., Sunrise City 4.88 → not even in the sad profile's top slot; Gym Hero 3.96 → 3.97 without the mood point but a slightly closer energy match). This confirms unmatched moods contribute exactly zero rather than partial credit or an error — a silent rather than a loud failure.

**Deep Intense Rock vs. Contradictory: Loves Acoustic but Max Energy** — Both target rock/intense at high energy, but the Contradictory profile adds `likes_acoustic=True`. Storm Runner still wins both times, but its score drops from 4.91 to 4.37 because Storm Runner's acousticness (0.10) fails the `>=0.6` acoustic threshold — the "loves acoustic" preference actively costs this profile points on every song, since no rock/intense song in the catalog is also acoustic. This is the clearest evidence that contradictory preferences don't cancel out gracefully; they just make every candidate slightly worse, with no candidate ever satisfying both.

**Edge Case: Zero Energy vs. Edge Case: Max Energy** — Zero Energy's top pick (Spacewalk Thoughts, 0.28 actual energy) and Max Energy's top pick (Night Drive Loop, 0.75 actual energy) are correctly the two farthest-apart songs energy-wise in the catalog, showing the closeness formula correctly identifies extremes — but neither ever reaches the catalog's true energy floor/ceiling (song energies only range 0.28–0.93), so both profiles' top scores (3.58 and 3.62) are capped well below what an in-range-target profile achieves (4.8–4.9), even though both got the objectively best available match.

**Edge Case: Out-of-Range Energy vs. Deep Intense Rock** — Out-of-Range Energy (target=1.5) still picks a sensible genre-matched winner (Coffee Shop Stories, jazz) but its total score (2.31) is far lower than any in-range profile's winner (4.8–4.9), and its energy term is literally negative. Compared to Deep Intense Rock's clean +1.41 energy bonus, this pair demonstrates the missing input validation concretely: an invalid target doesn't get rejected, it just quietly produces a worse-than-broken number.

**Edge Case: Unknown Genre/Mood vs. Genre Only** — Unknown Genre/Mood (genre="polka", mood="melancholy") scores every song purely on energy + acoustic match since neither genre nor mood ever hits, landing all 5 results in a tight, unremarkable 1.3–1.6 band. Genre Only (only genre="indie pop" set) scores on genre alone, producing a sharper 2.00/1.00/1.00/0.00/0.00 split. Together these show two different ways a profile can end up "thin": one dilutes every song equally (unknown genre/mood), while the other creates hard ties at zero once genre is exhausted (sparse profile) — both are low-confidence recommendation sets, but for different structural reasons.

---

## 8. Future Work  

I'd first fix the input-validation gap that let an out-of-range energy target produce a negative score.
I'd also replace the binary mood match with something gradient-based and put the unused fields to work instead of ignoring them. 


## 9. Personal Reflection  

Building this made me realize a recommender's "personality" comes almost entirely from arbitrary-looking weight choices rather from any deep understanding of taste. The most interesting discovery was how quietly things can go wrong (an invalid input didn't crash, it just produced a wrong-but-plausible-looking number, and a user's mood preference that wasn't in the dataset didn't error either, it just contributed nothing while looking indistinguishable from a fine match).
