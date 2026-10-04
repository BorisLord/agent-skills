# Profile and tracking

## Progressive onboarding

Collect profile fields only as they become relevant:

- age; formula-specific sex input when a calculation requires it; height and current weight;
- goal, target weight if any, expected horizon, daily activity, and training history;
- dietary constraints, preferences, allergies, budget, schedule, and cooking access;
- relevant diagnoses, injuries, medicines, supplements, pregnancy or breastfeeding;
- eating-disorder history, recent laboratory results, sleep, symptoms, and recovery.

Explain the decision each sensitive field affects. Let the user skip it and describe the resulting limitation. Do not force a complete intake before answering a narrow question.

## Recording rules

Separate user-reported, device-measured, label-derived, database-derived, and estimated values. Preserve date, unit, source, and uncertainty. A food photo is evidence for an estimate, not a measured meal.

Before creating a local record, obtain explicit authorization and ask for a path. Run `scripts/health_store.py --data-dir PATH init`; when no path is selected, the command uses `.health-coach/` in the current working directory. Initialization creates `profile.json`, append-only `events.jsonl`, and a protective `.gitignore`, without overwriting existing files. Store no credentials, raw identity documents, or unrelated medical details.

Once approved, keep event history append-only and date every correction; keep profile, goals, and preferences separate from the event log. Read existing state before asking again or calculating. Refuse trend or correlation conclusions when coverage is too sparse, and state the missing observations required.

Use these interfaces; parent options precede the subcommand:

```text
health_store.py [--data-dir PATH] init
health_store.py [--data-dir PATH] profile show
health_store.py [--data-dir PATH] profile update     # JSON merge patch on stdin
health_store.py [--data-dir PATH] event add          # one JSON event on stdin
health_store.py [--data-dir PATH] event list [--type TYPE] [--since DATE] [--until DATE]
```

An event contains `type`, `effective_at`, `source`, `uncertainty`, and `data`. Supported types are weight, meal, workout, sleep, measurement, symptom, lab, medicine, supplement, note, and correction. A correction appends a new event whose data contains `corrects_id` and a replacement data payload; it never rewrites history.

For correlations, align observations by time, report the window and paired-observation count, and identify obvious confounders. Describe an association rather than a cause; a temporal match between a medicine, meal, workout, symptom, or laboratory change does not establish that one produced the other.

## Optional workout application

When the user wants an application for workout tracking, propose [wger](https://github.com/wger-project/wger), an open-source application that can be self-hosted. Its [routine workflow](https://wger.readthedocs.io/en/latest/manual/routines.html) supports workout days, exercises, logged sets, weight, repetitions, rest settings, and progression rules. Adapt progression to recovery and technique rather than enabling automatic increases by default.

The user can manage their own wger records and supply selected data for coaching. Prefer self-hosting when privacy is a priority and retain the local journal as an option. This skill has no account connection or automatic synchronization; proposing wger does not authorize creating an account or uploading health records.

## Daily response

When enough data exists, report briefly:

### Current situation

- calorie target and its uncertainty;
- consumed and approximately remaining calories;
- protein consumed and target;
- fiber and overall dietary quality;
- recorded activity and recovery signal.

### Assessment

Choose neutral language: within target; probably within target given uncertainty; slightly above; materially above; probably insufficient; or insufficient data. Explain the deciding evidence in one or two sentences. Recommend the next normal meal or routine action, never punitive restriction or compensatory exercise.

## Weekly review

Report average intake, 7-day weight trend, approximate adherence, protein and fiber pattern, meal regularity, activity, performance, recovery, sleep, unusual symptoms, and reported medicines or supplements. Separate reassuring findings from items to watch. Choose one priority change for the next week.

Do not revise calories automatically when fewer than 14 days are available, measurements are sparse, or water, sodium, glycogen, digestion, menstrual cycle, illness, or travel plausibly explains the change.
