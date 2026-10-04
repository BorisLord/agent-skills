# Optional LanguageTool checks

Use this reference only when the author requests a checker or accepts a proposed assisted language check. If proofreading needs additional help, suggest it; the need alone does not authorize sending a draft to a service.

## Choose the available checker

Use an already configured, authorized LanguageTool integration or local server when available. A request specifically to check with that configured service is sufficient; do not ask repeatedly. If no integration exists, explain that limitation and continue ordinary editorial proofreading. Installing a checker or provisioning a service is a separate task.

Inspect the integration's current documentation and supported languages before calling it. Language coverage and rule depth vary; identify the article's language and appropriate regional variant rather than claiming universal coverage. See [supported languages](https://help.languagetool.org/hc/en-us/articles/39254526141463-What-languages-does-LanguageTool-support) and the [official HTTP API](https://languagetool.org/http-api/swagger-ui/).

If using the documented HTTP API, send a POST request to its `check` operation with the appropriate language code; query supported languages when necessary. Follow the configured service's authentication, text-size limits and documented request format. The [free public API prohibits automated requests](https://dev.languagetool.org/public-http-api); agent-driven checks require a local instance or a service account that permits automation. No endpoint credentials or paid account are assumed by this skill.

## Evaluate the suggestions

Check the draft after substantive editing, then examine suggestions in their surrounding sentence and paragraph. Apply valid grammar, spelling and punctuation corrections. Review style changes against the approved profile; preserve intentional literary phrasing, dialogue, specialist terminology, proper names and the author's argument. Check quotations against their sources instead of silently rewriting them.

Reread changed passages for meaning and flow. Return corrected prose, keeping any unresolved authorial choices outside the article. Describe the check accurately: using a grammar checker does not certify factual accuracy, originality, authorial authenticity or overall literary quality. An unavailable tool or unsupported language is a stated limitation, not a reason to pretend the check ran.
