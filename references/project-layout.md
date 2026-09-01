# Project Layout

Use a per-production directory so assets, prompts, jobs, and outputs remain traceable:

```text
project/
|-- script/
|   `-- source.*
|-- assets/
|   |-- characters/<character-id>/sheet.png
|   |-- characters/<character-id>/voice.*
|   |-- scenes/<scene-id>.png
|   `-- props/<prop-id>.png
|-- manifests/
|   |-- script-analysis.json
|   `-- assets.json
|-- prompts/
|   `-- <segment-id>_ref2va.txt
|-- graphs/
|   `-- <segment-id>.json
|-- video/
|   `-- <segment-id>.mp4
`-- audits/
    `-- video-audit.json
```

Never overwrite the user's original reference image. Keep API request metadata and generation timestamps outside the prompt text. Store secrets only in local environment variables or the user's secret manager.
