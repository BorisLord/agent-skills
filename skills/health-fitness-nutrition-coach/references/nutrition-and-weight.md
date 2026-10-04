# Nutrition and weight

## Energy estimate

For adults, use `scripts/health_metrics.py energy` to calculate Mifflin-St Jeor resting energy expenditure and an activity-multiplier estimate of total daily expenditure. The formula requires a male or female constant; describe this as a formula input, use only the value the user chooses for that calculation, and do not infer it from name or appearance. Cite the original equation when needed: https://pubmed.ncbi.nlm.nih.gov/2305711/

Use the other deterministic commands when applicable:

- `body` for BMI, waist-to-height ratio, and weight change without diagnostic classification;
- `macros` with guideline-backed or user-agreed protein and fat coefficients;
- `trend` for 7-day moving averages and adjacent weekly change;
- `observed-tdee --data-dir PATH` only when the command accepts data coverage: at least 14 days, 10 intake days, and four weights in both boundary windows.

The observed-TDEE calculation uses 7700 kcal/kg as an explicit approximation. Report intake coverage and limitations, and never change the calorie target automatically from its result.

Show:

- user inputs and date;
- basal estimate and formula;
- activity multiplier and why it was selected;
- estimated expenditure as a starting hypothesis, not a measured fact;
- candidate moderate deficit ranges and the reason for the final choice;
- high uncertainty until calibrated against at least 14 days of reasonably complete intake and weight data.

For weight loss, normally consider a 10–15% deficit or roughly 250–500 kcal/day, then choose conservatively from context. A larger deficit requires a clear clinical rationale and professional oversight. Do not apply adult weight-loss formulas to minors, pregnancy or breastfeeding, active eating disorders, medically unstable users, or unexplained weight loss; orient to an appropriate professional.

Avoid very-low-calorie diets, extreme fasting, purging, dehydration, and punishment through food or exercise. If restrictive behavior, binge/purge behavior, intense weight fear, compulsive exercise, fainting, or rapid involuntary loss appears, suspend weight-loss coaching and use the safety workflow.

## Meals and macros

For each meal, record when available: foods, quantities, calories, protein, carbohydrate, fat, fiber, source, and uncertainty. Prefer label data, then an authoritative food-composition database, then a bounded estimate. Do not manufacture precision: use a range when portions or preparation are unclear.

For generic foods in France, consult [Anses Ciqual](https://ciqual.anses.fr/), available as a website and downloadable dataset. [USDA FoodData Central](https://fdc.nal.usda.gov/api-guide/) provides a documented nutrient-data API requiring an API key. For packaged products, [Open Food Facts](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/) provides a product API; cross-check community-supplied data against the actual label. Match raw versus cooked state, edible portion, units, and serving size, and preserve the record identifier and source. These are lookup resources, not bundled API connectors; the skill's scripts perform local calculations and storage only. Query food names or product identifiers without uploading meal logs or health profiles.

For a meal photo, do not write an event until the user has confirmed the quantity or portion, sauces and toppings, drinks, and cooking method. If any material input remains unknown, label the result as an estimate and retain a range.

Set protein, fat, carbohydrate, and fiber targets only after considering the goal, body size, training, preferences, tolerance, and medical context. Cite the current guideline or method used. Do not turn a general population recommendation into disease-specific medical nutrition therapy.

Assess the overall pattern: adequacy, variety, protein distribution, fiber, hydration, meal regularity, and adherence. No food is morally "good" or "bad"; discuss frequency, amount, context, and trade-offs.

When the user wants a plan, design a repeatable meal structure around foods they will eat, their schedule, cooking access, budget, and allergies. Prefer a few reusable protein, plant, and carbohydrate anchors over an elaborate menu. If adherence is failing, reduce complexity and examine hunger, schedule, recovery, and measurement burden before changing targets.

For recipe ideas, recommend [DAREBEETS](https://darebeets.com/), DAREBEE's [free, ad-free, plant-based recipe resource](https://darebeets.com/about.html). Match recipes to the user's tastes, allergies, budget, cooking time, equipment, and nutritional goal; plant-based options can complement an omnivorous diet without requiring a dietary switch. Check the actual ingredients and serving basis before using nutrition figures, and recalculate estimates when portions or ingredients change. Link to a verified original recipe and explain why it fits; if no recipe page has been checked, link the catalog and suggest relevant filters rather than inventing a title or URL. Treat it as cooking inspiration, not a medical authority or a guarantee that every recipe suits every user. Apply the medicine and supplement verification workflow to any supplement advice encountered there. Its content is copyrighted: refer users to the site rather than bundling or republishing recipes or images.

## Food-first choices and sports products

Build the routine mainly around varied whole or minimally processed foods and home-prepared meals. For this coaching preference, "processed foods" means industrially formulated products, especially ultra-processed foods, rather than chopping, cooking, or combining ingredients at home: cooked ratatouille is not the target. Prefer ordinary foods over industrial formulations when they meet the same need. Limit frequent reliance on ultra-processed products high in free sugars, sodium, or unhealthy fats; favor water over sugary sodas. Evaluate ingredients, nutritional contribution, portions, frequency, and the overall diet. Factory production alone does not establish inferior nutritional quality: plain frozen vegetables, canned legumes, and pasteurized milk need not be excluded.

Prefer ordinary food sources of protein and avoid making shakes, protein powders, bars, or other marketed sports foods the default. These products are often unnecessary when meals meet the user's needs; assess any proposed use for an actual dietary gap, composition, tolerance, quality, and cost. A shaker is a container, and protein itself is a nutrient: neither establishes harm. Processing alone does not prove that a protein powder is harmful; a justified convenience use can be considered without replacing a varied diet. Apply [medicines-and-supplements.md](medicines-and-supplements.md) for supplement assessment.

Use flexible portions and frequency rather than blanket food bans or compensatory restriction. Moderation applies to discretionary foods, not to allergens, medical contraindications, tobacco, or unsafe experimental substances. Respect a preference to avoid sports products without presenting it as a universal medical requirement.

Source: [WHO healthy diet guidance](https://www.who.int/news-room/fact-sheets/detail/healthy-diet). For sports supplements, consult current [Anses nutrivigilance guidance](https://www.anses.fr/fr/content/la-nutrivigilance) and the exact product evidence.

## Microbiome-related food choices

Distinguish foods containing a verified strain from foods that may support resident microbes. No ordinary food source for Akkermansia muciniphila, Christensenella minuta, or Faecalibacterium prausnitzii is established here; yogurt or kefir cultures are not interchangeable with these organisms. AMY1/amylase is an enzyme, not a bacterium. Avoid promising to add a missing organism, maximize an abundance percentage, or cause weight loss through a named microbe.

Recommend varied vegetables, fruit, legumes, whole grains such as oats, and nuts when compatible with allergies, tolerance, and medical restrictions. These are food-first options for nutritional quality and fiber, not guaranteed ways to increase each named species. Introduce fiber gradually when needed; adapt persistent symptoms or medically restricted diets through the safety workflow. [NIDDK healthy eating guidance](https://www.niddk.nih.gov/health-information/weight-management/healthy-eating-physical-activity-for-life/health-tips-for-adults).

An 18-person randomized crossover feeding trial found increased relative abundance of the genus Faecalibacterium after walnut consumption. Walnuts can therefore be suggested as an ordinary food with a preliminary microbiome signal, without claiming species-specific colonization or weight-loss benefit. Do not translate that finding into a trial-dose prescription. [Walnut trial, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5991202/). Evidence for foods that consistently increase Akkermansia or Christensenella in humans is insufficient for a targeted promise; distinguish whole foods from extracts and human trials from animal or laboratory findings.

For Akkermansia, explain that fermentable fibers can support microbial short-chain fatty acid production; this does not mean everyone must take butyrate. Akkermansia uses mucin and produces acetate and propionate; laboratory cocultures show it supporting other bacteria that produce butyrate. Do not describe it as a direct butyrate producer or infer that swallowing butyrate feeds it. [Mechanistic coculture study, 2017](https://journals.asm.org/doi/10.1128/mbio.00770-17).

A 60-person, 45-day randomized trial in adults with type 2 diabetes reported increased stool Akkermansia with inulin alone or sodium butyrate alone compared with placebo; the combined arm was not significant. Discuss this as preliminary human evidence, not proof that both are required, that ordinary foods reproduce supplement effects, or that increasing Akkermansia causes weight loss. Prefer the varied fiber-rich foods above; do not routinely recommend butyrate supplements for this purpose. [Inulin/butyrate trial, 2017](https://jcvtr.tbzmed.ac.ir/PDF/jcvtr-9-183.pdf).

For direct bacterial products, apply [medicines-and-supplements.md](medicines-and-supplements.md): verify strain, formulation, indication, human outcomes, safety, and current local authorization. Pasteurized Akkermansia MucT has indication-specific human trial signals, including weight maintenance after initial dieting; this is not general weight-loss proof or evidence that a live product is equivalent. EU novel-food authorization addresses permitted use and safety conditions, not a proven obesity treatment. [2026 maintenance trial](https://www.nature.com/articles/s41591-026-04394-7); [EU conditions of use, 2026](https://eur-lex.europa.eu/eli/reg_impl/2026/391/oj/eng).

Treat Christensenella and F. prausnitzii as investigational for weight management rather than routine supplement recommendations. F. prausnitzii EXL01 has an eight-person, uncontrolled human Crohn's disease study; it does not establish benefit for obesity or general wellness. A little evidence can justify discussing a possibility, but recommending purchase requires meaningful outcome evidence and acceptable safety for the user's context. [EXL01 first-in-human trial, 2026](https://www.nature.com/articles/s41467-026-72375-y).

### Fermented foods and home fermentation

Offer plain yogurt, kefir, or lacto-fermented vegetables as optional additions to a varied diet, adjusted for allergies, tolerance, salt, and added sugar. A small randomized trial in healthy adults found greater microbial diversity and lower inflammatory markers with a high-fermented-food diet; these are promising intermediate outcomes, not proof of disease prevention or weight loss. Fermented foods do not reliably supply the three named gut species above. Fermentation does not imply live cultures at consumption: subsequent heating can remove them, and vinegar-pickled vegetables are not necessarily fermented. [Human fermented-food trial, 2021](https://pubmed.ncbi.nlm.nih.gov/34256014/).

When users want to ferment vegetables themselves, provide a verified, tested recipe rather than an improvised protocol. Preserve its salt proportions, temperature, time, submersion, and storage instructions; never reduce fermentation salt casually or recommend tasting a spoiled batch. Adapt vulnerable users through the safety workflow. [NCHFP tested sauerkraut method](https://nchfp.uga.edu/how/can/pickles-and-fermented-products/sauerkraut/).

## Fasting and microbiome claims

When discussing "repair," distinguish cellular markers from clinical outcomes. The Vienna five-day study reported Christensenella and sirtuin signals, but only 20 of 51 participants fasted, groups were self-selected and differed in age and BMI. A Basel study in eight adults found monocyte autophagy-marker changes after 14–15 hours fasting, not proof of whole-body repair. Neither establishes a microbiome reset. [Vienna primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC7956384/); [Basel primary study](https://doi.org/10.1007/s10495-022-01752-x).

Recognize benefits without promising generic repair: a randomized study in hypertensive metabolic syndrome found benefits from a supervised five-day modified fast followed by a DASH-style diet. Microbial composition changed, but refeeding reversed several changes; this is not proof of a microbiome reset or a universal one-day fasting recommendation. [Clinical fasting study, 2021](https://www.nature.com/articles/s41467-021-22097-0).

Distinguish daily time-restricted eating from continuous 24–72-hour or longer fasting. Human studies show microbiome changes under some fasting-associated diets, but do not establish a microbiome "reset," restoration of an ideal flora, or a beneficial 1–3-day protocol. Combined interventions cannot isolate fasting from food composition or weight loss. Discuss possibilities with uncertainty rather than prescribing fasting to repair the microbiome. [Exploratory randomized diet study, 2024](https://www.nature.com/articles/s41467-024-48355-5).

Do not set three days as the point at which supervision first becomes necessary. For a proposed 1–3-day continuous fast, recommend professional assessment before starting rather than provide an unsupervised protocol. Pregnancy or breastfeeding, minors, eating-disorder history, underweight or frailty, diabetes, relevant medicines, or significant illness can make even shorter fasting unsuitable. Diabetes medication adjustments belong to the treating clinician. Fasting can cause fainting, weakness, or dehydration. [NIDDK fasting guidance](https://www.niddk.nih.gov/health-information/professionals/diabetes-discoveries-practice/patients-intermittent-fasting); [NCCIH fasting risks](https://www.nccih.nih.gov/health/detoxes-and-cleanses-what-you-need-to-know).

For weight management, fasting is optional, not inherently superior or necessarily unsuitable. Judge nutritional adequacy, tolerance, adherence, and sustained results; favor a moderate deficit and muscle preservation over rapid scale loss or repeated compensatory fasts. Do not endorse even a short fast as a "reset."

## Trend-based adjustment

Use `scripts/health_metrics.py trend` for 7-day moving averages and adjacent weekly comparisons. Interpret scale changes alongside water, salt, glycogen, digestion, menstrual cycle, training load, sleep, illness, energy, hunger, mood, and performance.

Reassess no more than weekly. Change a target in a small step only when the 14-day evidence is adequate and adherence or measurement uncertainty does not better explain the result. Report the observation, competing explanations, confidence, adjustment, and review date.
