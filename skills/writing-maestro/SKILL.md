---
name: writing-maestro
description: Use when drafting or revising human-facing prose such as docs, essays, prompts, UI copy, reports, commit messages, PR text, or polished long-form writing. Combines anti-AI-trope editing with clear and concise style rules for stronger, more natural prose.
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

## Limited Context Strategy

When context is crowded, separate drafting from polishing:

1. Produce the draft with normal task context.
2. Run an isolated copyedit pass using only the draft plus anti-trope reference and one style reference.
3. Merge only edits that improve clarity, precision, or flow.

## Reference Use

- Use [references/ai-writing-tropes-to-avoid.md](references/ai-writing-tropes-to-avoid.md) to remove AI cadence and formulaic phrasing.
- Use [references/elements-of-style-principles.md](references/elements-of-style-principles.md) as the default concise checklist when writing casually or when token budget is tight.
- Use [references/the-elements-of-style.md](references/the-elements-of-style.md) as the detailed standard when writing for human readers with high quality requirements. In this case, this detailed reference is mandatory.
