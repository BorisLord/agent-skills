# Personalization decisions

Use this reference to turn the base skill into the user's version. Resolve choices progressively; do not require every choice before useful work begins.

## Scope

Choose which modes are active:

- lifestyle coaching only;
- nutrition and weight tracking;
- training and recovery;
- health records and trend explanation;
- medical triage and report explanation;
- medicines and supplements.

Safety triage remains active in every mode.

## Coaching configuration

Record the user's choices for:

- primary goal and success measures beyond body weight;
- strength, endurance, mixed, mobility, return-to-sport, or general health emphasis;
- desired tracking depth: minimal, standard, or detailed;
- check-in rhythm and preferred response length;
- neutral factual, supportive, or accountability-oriented tone;
- calorie/macronutrient tracking versus portion- or habit-based coaching;
- manual data sources that may be used; this version has no device or external-service connector;
- country and language for guidelines and emergency routing;
- local storage path, file format, retention, and fields, if persistence is wanted.

## Change control

Summarize agreed choices before modifying the skill or creating a profile. Treat medical guardrails, evidence labeling, emergency routing, and the prohibition on diagnosis or prescribing as invariants. Keep user preferences in a separate profile or configuration file so future skill updates do not overwrite personal data.

When a choice changes the recommendation materially, present the trade-off and ask one focused question. Otherwise, choose the simplest reversible default and label it.
