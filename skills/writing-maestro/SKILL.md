---
name: writing-maestro
description: Use when drafting or revising human-facing prose such as docs, essays, prompts, UI copy, reports, commit messages, PR text, or polished long-form writing. Combines anti-AI-trope editing with clear and concise style rules for stronger, more natural prose, including strict prohibited-pattern enforcement for Chinese writing.
---

# Writing Maestro

Use this skill when the task is to write, rewrite, edit, or polish prose that humans will read.

## Mission

- Make writing clear, direct, and specific.
- Remove common AI writing tells and templated cadence.
- Keep tone natural while preserving the user's intent and voice.

## Workflow

1. Set constraints: audience, format, tone, and required level of detail.
2. Draft for meaning first: prioritize factual clarity over style flourishes.
3. Run anti-trope pass with [references/ai-writing-tropes-to-avoid.md](references/ai-writing-tropes-to-avoid.md).
4. Select style reference level:
   - Default: use [references/elements-of-style-principles.md](references/elements-of-style-principles.md) for fast, token-efficient cleanup.
   - Detailed and human-facing writing: must use [references/the-elements-of-style.md](references/the-elements-of-style.md).
5. Run clarity and concision pass with the selected style reference.
6. Final read aloud check: smooth rhythm, no redundant transitions, no empty emphasis.
7. For Chinese prose, run the mandatory prohibited-pattern check below and rewrite every violation before delivery.

For Chinese prose, use the localized references instead:

- [references/ai-writing-tropes-to-avoid.zh-CN.md](references/ai-writing-tropes-to-avoid.zh-CN.md)
- [references/elements-of-style-principles.zh-CN.md](references/elements-of-style-principles.zh-CN.md)
- [references/the-elements-of-style.zh-CN.md](references/the-elements-of-style.zh-CN.md)

The Chinese versions are localized writing guides, not word-for-word translations. They preserve the original editorial intent while replacing English-only grammar rules and examples with guidance that works in modern written Chinese.

## Mandatory Chinese Prohibition

For all Chinese prose, prohibit negative-reframe constructions that negate one framing and replace it with another. Do not generate constructions with these forms:

- `不是 X，而是 Y`
- `并非 X，而是 Y`
- `不在于 X，而在于 Y`
- `不是因为 X，而是因为 Y`
- `与其说是 X，不如说是 Y`
- `并不是 X，只是/却是 Y`

Treat punctuation and omitted conjunctions as the same pattern. This includes split forms such as `不是 X。是 Y。` and compressed forms such as `非 X，而是 Y`.

State the intended point directly. If contrast matters, describe the two claims in separate positive statements and explain their relationship without a negation-to-reveal turn.

Before delivering Chinese prose, scan the complete output sentence by sentence. If any prohibited construction remains, rewrite it. This check is mandatory even when the construction would be rhetorically effective. Preserve the wording only when the user explicitly requires a verbatim quotation; keep such quoted text clearly attributed and do not reproduce the construction in surrounding prose.

## Editing Priorities

- Use active voice when actor and action are important.
- Put statements in positive form where possible.
- Use specific and concrete wording over abstract labels.
- Omit needless words and padded transitions.
- Keep related words together and avoid awkward clause distance.
- Place emphatic words near sentence endings when emphasis is intended.
- Keep one tense in summaries unless time shifts are required.
- Prefer parallel structure for coordinate ideas.

## Guardrails

- Do not add drama, fake suspense, or forced profundity.
- Do not ask rhetorical questions unless the format explicitly calls for them.
- Do not over-structure prose into listicle-like paragraphs.
- Use markdown only when it improves readability for the target format.
- Enforce the Mandatory Chinese Prohibition for every Chinese output.

## Limited Context Strategy

When context is crowded, separate drafting from polishing:

1. Produce the draft with normal task context.
2. Run an isolated copyedit pass using only the draft plus anti-trope reference and one style reference.
3. Merge only edits that improve clarity, precision, or flow.

## Reference Use

- Use [references/ai-writing-tropes-to-avoid.md](references/ai-writing-tropes-to-avoid.md) to remove AI cadence and formulaic phrasing.
- Use [references/elements-of-style-principles.md](references/elements-of-style-principles.md) as the default concise checklist when writing casually or when token budget is tight.
- Use [references/the-elements-of-style.md](references/the-elements-of-style.md) as the detailed standard when writing for human readers with high quality requirements. In this case, this detailed reference is mandatory.
