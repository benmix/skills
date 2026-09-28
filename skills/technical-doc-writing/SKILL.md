---
name: technical-doc-writing
description: Draft, edit, or review developer documentation such as how-to guides, tutorials, conceptual docs, API references, and CLI instructions. Use the locally saved Google developer documentation style guide as an editorial reference, while respecting project-specific style and the user's language.
---

# Technical document writing

Help a developer understand a system or complete a task. This skill distills the Google developer documentation style guide into a writing workflow. The downloaded guide is Google's house style, not a universal standard: follow the user's requirements and the project's established terminology and style first. Its US English rules apply to English prose; adapt clarity and accessibility principles to other languages without copying English grammar rules.

## Find the relevant guidance

Read [references/google-style-map.md](references/google-style-map.md) to select the few chapters needed for the task. Every chapter link in that map points to a local Markdown file under `references/google-style-guide/`. The [complete chapter index](references/google-style-guide/README.md) lists all 70 chapters and their official source URLs. Consult the online source only when a current detail is needed.

To refresh the downloaded chapters, run `python3 scripts/update_google_style.py` from this skill directory (or pass its path from elsewhere). Use `--check` to report drift without writing files.

## Write or revise

1. Establish the reader, their goal, the document type, and the knowledge required before they start. Use available code, product behavior, and authoritative sources to verify technical facts. Flag facts that remain unknown rather than inventing them.
2. Organize around the reader's task or question. Give each page a clear purpose and descriptive headings. For a how-to, put prerequisites before actions, recommend a workable path for the common case, and explain alternatives only when a choice matters. For a reference, cover the public contract systematically.
3. Write directly: address the reader, use concrete verbs and active voice, put conditions before the instructions they qualify, and keep terminology consistent. Distinguish required actions, recommendations, options, expected results, and possible results.
4. Make examples usable. Introduce what each example shows; format code, commands, filenames, identifiers, and UI labels consistently. Explain placeholders and where their values come from. Test executable examples when practical, and do not present incomplete syntax as a copyable command.
5. Make the page easy to scan and use: one main idea per paragraph, numbered steps for sequences, bullets for unordered items, tables for comparable multi-field data, descriptive link text, semantic structure, and text alternatives for images.

## Check the result

Read as a first-time user. Confirm that the reader can find the right section, meet the prerequisites, perform the steps, replace example values, and recognize success. Check names and commands against the source, then check links, terminology, accessibility, and any project-specific style. Preserve the requested format and level of detail.
