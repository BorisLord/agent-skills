# Free exercise sources

## Select for the user's request

Use these catalogs to find candidates matching the goal, experience, available equipment, location, session time, preferred movements, and injury or pain constraints. Load only the needed entries; choose a small useful set rather than listing every matching exercise. For each recommendation, give its purpose, sets or duration, repetitions where relevant, effort cue, key technique points, an easier alternative when useful, and a source link. Translate instructions into the user's language without changing their meaning.

Catalog metadata and tags are not clinical clearance. Check instructions and technique; apply the medical safety workflow for pain or symptoms. Identify missing fields rather than inventing equipment, difficulty, or media. Several catalogs may share upstream data; overlapping entries are not independent evidence. No catalog guarantees every fitness exercise.

When the user prefers a ready-made session or structured program, direct them to [DAREBEE workouts](https://darebee.com/workouts.html) or [programs](https://darebee.com/programs.html). Select a relevant original page after checking the goal, equipment, difficulty, impact, session length, and recovery demands. Explain why it fits and any needed adaptation; give the source link rather than copying the complete illustrated workout. DAREBEE's internal testing is not individualized medical clearance. When no suitable page has been verified, link the catalog and state the selection criteria instead of inventing a workout title or URL.

## Catalogs and access

| Source | Use | Free access and reuse |
| --- | --- | --- |
| [DAREBEE](https://darebee.com/) | Ready-made workouts, programs, challenges, and exercise guides. | [Free access without sign-up or subscription, supported by donations](https://darebee.com/about.html). Content is copyrighted, not an open dataset; link to original pages instead of bundling, mirroring, or republishing it. |
| [Free Exercise DB](https://github.com/yuhonas/free-exercise-db) | Default standalone catalog: muscles, equipment, level, instructions, and images. | Public-domain/Unlicense JSON, available online or as a download without a key. Some fields are incomplete. |
| [wger](https://github.com/wger-project/wger) | Exercise descriptions and media; also an optional workout tracker. | [Public exercise API](https://wger.readthedocs.io/en/latest/api/api.html) without authentication. Check the current data and individual media licenses before copying or redistributing; software and content licenses differ. |
| [Kinetic Exercises Database](https://github.com/kinetic-place/exercises-db) | Structured muscles, equipment, instructions, and difficulty; English and Spanish entries. | Downloadable JSON under MIT; retain the license when copying. A hosted API is also advertised as free: verify current availability and terms before use. |
| [RepDB free exercise dataset](https://github.com/RepDB/exercise-dataset) | Illustrated instructions in English, German, and Spanish. | Free tier with required [attribution and restricted reuse](https://github.com/RepDB/exercise-dataset/blob/main/LICENSE-DATA.md). Link to the original catalog for coaching; do not bundle or republish its dataset, use paid preview assets, or use images for generative-AI derivation. |

Prefer free access that meets the request. Check current terms before proposing another source; an API demo or trial does not establish ongoing free access. Use generic exercise queries without uploading workout logs or health profiles. No external account connection or automatic synchronization is bundled.

## Optional local download

The skill contains source links and instructions only; do not include exercise datasets in its package. Consult catalogs online unless the user explicitly requests or accepts a local download. Offer this option when offline access or repeated lookups would help, explaining the source, downloaded content, approximate size when known, and chosen directory. Obtain agreement on the source and destination before writing; an approved download does not authorize later refreshes or extra media downloads.

Prefer Free Exercise DB's JSON for a simple local catalog. After approval, download from the official repository at an identified commit into the user's chosen data directory, outside the skill and repository. Preserve the upstream license and record the source URL, commit, retrieval date, and file checksum. Parse the JSON and check that the expected exercise fields exist before using it. Surface download or validation errors; do not silently substitute a different source or overwrite an existing cache. Download images or another dataset only when included in the user's approval and permitted by its license.

Search the local file by the relevant equipment, muscles, level, or exercise name and read only matching records. Link recommendations to upstream exercise records; local availability does not make the instructions clinically validated. Keep public exercise data separate from the user's health profile and journal. Refresh only on request or approval, retaining provenance for the replacement snapshot.
