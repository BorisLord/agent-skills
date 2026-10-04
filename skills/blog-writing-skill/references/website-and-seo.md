# Website and SEO research

Use this reference when developing the publication context and search orientation for an article. Scale research to the decision it must support; choose relevant available tools rather than calling every tool.

## Publication context

Start with the supplied URL and relevant existing context. Inspect the site's purpose, audience and article section, then a small representative selection of articles, especially related topics. Consider author-specific or section-specific differences rather than assuming the entire site has one voice.

Capture a compact working profile:

- Audience, assumed knowledge, language and regional conventions.
- Editorial purpose and typical treatment of the subject.
- Stable voice: register, vocabulary, sentence rhythm, narration and humour.
- Contextual tone appropriate to the proposed theme.
- Heading, citation and formatting conventions; related pages and possible internal links.

Use real examples from inspected pages to justify the proposed voice. Keep inferences distinct from the author's explicit instructions. If samples are inconsistent, prioritize the relevant section and writer; otherwise ask which voice to follow. If the site is inaccessible or has no articles, use supplied samples or propose a theme-appropriate profile for approval. Never describe an inferred profile as an observed one.

## Research tools

Discover available capabilities and reuse existing site context or research when relevant. No SEO product is required for this skill.

Follow this route, skipping steps whose evidence already exists or whose tools are unavailable:

| Decision | Tool or capability | Evidence to carry into the brief |
| --- | --- | --- |
| Understand the publication | Browser, site search or a configured scraper; inspect relevant articles and site navigation | Audience, representative samples, related pages and verified link destinations |
| Reuse existing SEO context | OpenSEO `list_projects`, then `get_project_context` for the matching existing project | Known goals, market, writing preferences and earlier research |
| Understand actual site demand, when connected | OpenSEO `get_search_console_performance`, or the equivalent authorized Search Console integration, using relevant query and page dimensions | Observed queries, pages, clicks and impressions for the selected period; possible overlap with the proposed article |
| Explore the author's theme | OpenSEO `research_keywords`, or equivalent keyword research, with a focused set of seed terms in the article's language and market | Relevant candidate queries and available demand/intent data |
| Resolve a shortlist decision | OpenSEO `get_keyword_metrics`, only for candidates whose metrics are missing or need refreshing | Comparable demand and difficulty data; retain unavailable values as unknown |
| Understand what ranks | OpenSEO `get_serp_results`, or current search results through browsing; open relevant result pages | Search intent, competing formats, coverage, source URLs and gaps worth addressing |
| Investigate a relevant site's search footprint, if needed | OpenSEO `get_ranked_keywords`, or an equivalent domain/page keyword tool | Ranking queries and URLs for that destination or competitor; distinguish estimates from first-party analytics |

OpenSEO names above are the documented capabilities, not an instruction to call nonexistent tools. Discover the actual integration and inspect its schema. Calls requiring `projectId` must use the matching project returned by `list_projects`; do not invent an ID or use another site's project to obtain private data. If no matching project exists, explain the limitation and continue with permitted browsing or another available tool. Creating a project is separate work.

Align the research language and location with the approved target audience rather than silently using a provider's default market. Reuse returned metrics before buying the same research again. Read connected analytics only when they answer a relevant editorial question. Stop expanding research once it supports the proposed angle, search orientation and links.

Respect each tool's documented inputs, cost and authorization rules. Avoid saving keywords, starting trackers or running whole-site audits merely to write an article. Current integration setup and capabilities are documented in [OpenSEO MCP](https://www.openseo.so/docs/mcp).

If a tool is absent or fails, report the limitation. Public search results can support a qualitative assessment but cannot supply missing search volumes, difficulty scores, conversion data or private analytics. Keep unknown metrics unknown.

## From idea to search orientation

Translate the author's idea into plausible reader questions. Determine language and target market from the brief and website; ask when the distinction would change the research.

Examine relevant search results and inspect useful competing pages. Identify their intent, content type, main coverage and missing or weak explanations. Rankings show visibility for a query, not proven traffic, conversions or editorial truth.

Select a primary query or topic because it fits the intended reader and authorial purpose. Suggest related terms only where they help cover the subject. Consider whether an existing site article already addresses the same intent and explain the proposed distinction or possible update to the author.

Look for a useful original contribution: the author's position, experience they actually supplied, a better explanation, a relevant example or a question others neglect. Competitors inform coverage; their argument and outline need not become the author's.

Verify internal-link destinations and fit them where they help readers. Link external factual sources near the claims they support when appropriate to the agreed research and citation style. Do not invent URLs or make an opinion appear proven through an unrelated citation.

## SEO writing decisions

Make the visible title descriptive and consistent with the article. Use a clear heading hierarchy without forcing a fixed number of sections. Include search vocabulary naturally; avoid keyword quotas, stuffing and mandatory FAQ sections.

Choose length for the topic and reader. Google explicitly states that it has no preferred word count and recommends original, useful, people-first content: [Google Search Central](https://developers.google.com/search/docs/fundamentals/creating-helpful-content).

If publication metadata is requested, propose a distinct SEO title only when it helps the destination, a page-specific meta description and a readable slug. Follow the site's real CMS constraints where known, rather than universal character limits. Google may derive title links and snippets from multiple page elements: [title links](https://developers.google.com/search/docs/appearance/title-link), [snippets](https://developers.google.com/search/docs/appearance/snippet).

SEO readiness here concerns the article and agreed metadata. Indexing, deployment, site performance and ranking outcomes require separate work; do not claim they were verified through drafting alone.
