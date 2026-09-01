# H3 Ref2VA Prompt Rules

Use the full-reference format in this exact order:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

Write visual and production descriptions in English. Preserve the user's dialogue in its original language inside `<d>` blocks, for example:

```text
<Subject 1> (S1) says in Mandarin: <d>[Chinese] 这里是 Peto 宠物电台，我们下期见！</d>
```

Give each visible recurring subject a stable `<Subject N>` label and each actual vocal source a stable `(Sx)` ID. Use `<Picture N>` for concrete image references and `<Audio N>` only when an audio asset is actually referenced. Keep labels consistent in all sections.

Every shot should identify composition, subject placement, environment, action, camera movement, dialogue timing, and diegetic sound. Begin Shot 1 without a timestamp; later cuts use increasing timestamps. A segment may contain prompted camera cuts, but it must remain one independent H3 generation job.

For this workflow, include these constraints unless the user overrides them: 9:16 portrait framing, no added subtitles, captions, UI, cards, overlays, logos, or watermarks, no unrequested text, no post-generation editing, and no video stitching. Existing physical text in a referenced scene may remain and should be named explicitly.

Keep a segment's spoken content within 15 seconds. Do not use `<cutoff>` unless the user explicitly accepts truncated speech. Do not translate, summarize, or rewrite dialogue in the prompt.
