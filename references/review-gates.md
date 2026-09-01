# Approval Gates

## Gate 1: analysis and asset plan

Show:

- Script synopsis and preserved dialogue map.
- Character and speaker table.
- Scene table and key-prop table.
- Required character-sheet and audio assets.
- Missing optional assets and concrete questions.
- Proposed image/voice API inputs and estimated generation scope.
- Provisional segment count and timing risk.

Stop with a direct approval request. A vague acknowledgement is not enough; use an explicit question such as: `请确认分析和资产清单，确认后我才开始询问并调用生图/语音 API。`

## Gate 2: generated assets

Show:

- Asset previews or contact sheets.
- Stable IDs and file paths.
- Character-sheet panel checks.
- Scene and prop-to-shot mapping.
- Voice asset source and continuity policy.
- Failed, uncertain, or regenerated assets.

Stop with a direct approval request. Only after approval may the skill segment the script, write final H3 prompts, and submit local H3 jobs.

## Revisions

When the user rejects an asset, identify the exact asset and revision request, regenerate only that asset when possible, update its manifest entry, and reopen Gate 2. Do not silently replace approved assets.
