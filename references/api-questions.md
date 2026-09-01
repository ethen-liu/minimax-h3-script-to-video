# API Intake Questions

Ask these questions after Gate 1 and before any generation call. Do not ask for secrets in chat.

## Image generation

- Provider and API type (native provider, OpenAI-compatible, or custom HTTP).
- Base URL and endpoint path.
- Model name and image output format.
- Whether reference images are accepted, and the maximum number per request.
- Desired image size/quality and whether transparent PNG is supported.
- Local environment variable name containing the API key.
- Retry, timeout, and concurrency limits.

## Voice generation

- Which of the three voice paths is selected: upload, voice API, or previous-segment continuity.
- Provider, endpoint, model, and local environment variable name if voice API is selected.
- Language, voice ID, age/timbre, speaking rate, pronunciation, and emotional range per character.
- Whether the API returns a reusable voice reference or only a rendered dialogue file.
- Audio format, sample rate, channel layout, and maximum reference duration.

Record answers in project metadata. Do not place credentials in prompts, manifests, Git history, or generated assets.
