# Training and recovery

## Plan from constraints

Clarify the sport or outcome, current level, recent training, available days and session duration, equipment, injuries or symptoms, preferences, and fixed event date. Ask about medical clearance only when risk or the requested intensity makes it relevant.

Build the minimum viable plan around specificity, gradual progression, recovery, and adherence. Give session purpose, duration, intensity cue, and stop criteria. Prefer talk test or perceived exertion when heart-rate zones are unverified. Treat wearable calorie, recovery, HRV, and readiness values as noisy signals, not diagnoses.

Use [exercise-sources.md](exercise-sources.md) when selecting exercises from free catalogs, finding instructions or demonstration media, or offering an optional local dataset download. For tracking sessions, use the wger option in [profile-and-tracking.md](profile-and-tracking.md).

Use `scripts/health_metrics.py` for deterministic calculations:

- `strength` for Epley estimated 1RM over 1–12 repetitions and volume load;
- `cardio` for speed and pace;
- `heart-rate` for conventional Karvonen heart-rate-reserve bands only when resting and maximum heart rates are supplied;
- `activity-energy` when the MET value is supplied, preserving high uncertainty;
- `sleep` for sleep efficiency without diagnostic classification.

Use current official population guidance as a health baseline, then adapt to the user's training goal. French adult guidance currently uses progressive daily activity plus regular strength, mobility, and balance work; verify the live guidance before quoting exact targets: https://www.mangerbouger.fr/bouger-plus/a-tout-age-et-a-chaque-etape-de-la-vie/les-recommandations-pour-les-adultes/augmenter-l-activite-physique

For long-term health, a short, modest, safe session is preferable to inactivity when no medical restriction applies. Reward consistency over an ideal program; scale duration and intensity to current capacity while preserving safe technique. "Some activity is better than none" never overrides injury or emergency stop criteria. For longevity goals, combine this module with [healthy-aging.md](healthy-aging.md).

## Progression and review

Change one major load variable at a time: frequency, duration, volume, intensity, or density. Evaluate performance, technique, perceived effort, pain, sleep, mood, motivation, and life stress before progression. Use easier sessions or reduced load when recovery signals worsen across several days.

Do not prescribe "calorie compensation" exercise after eating. Fuel demanding training and protect rest days. Coordinate weight-loss targets with performance and recovery rather than optimizing scale loss alone.

## Pain and illness

Differentiate ordinary exertion from pain or systemic symptoms. Ask about onset, location, mechanism, severity, swelling, loss of function, neurological symptoms, fever, and progression. Stop the planned session and apply medical triage when symptoms suggest acute injury, concussion, cardiopulmonary compromise, heat illness, rhabdomyolysis, or another serious condition.

Do not diagnose an injury from a description or image. Offer safe load modification only when red flags are absent and give explicit criteria for professional assessment and return to activity.
