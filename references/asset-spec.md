# Asset Specification

## Character assets

Create one 3:4 portrait character sheet for every recurring character. Use a clean four-panel layout with the same identity, costume, proportions, lighting, and background across panels:

- Top-left: close-up, straight-on face.
- Top-right: close-up, three-quarter or half-side face.
- Bottom-left: full-body front view, cropped above the face or with the face intentionally excluded.
- Bottom-right: full-body back view, cropped above the face or with the face intentionally excluded.

Record the character name, stable subject ID, costume, age/type, expression range, panel layout, source/reference images, and final file path.

## Character audio

Each speaking character needs one stable voice asset. Ask the user to choose one of three paths:

1. User-uploaded character audio.
2. Voice API generated reference audio.
3. First-segment audio from upload or voice API, then reuse the latest valid character audio from the preceding segment.

Record language, voice ID or speaker ID, sample rate, duration, clean/noise-free status, source, and reuse policy. Do not copy a complete preceding dialogue into a later segment when only voice continuity was requested.

## Scene assets

Create one clean image per unique scene. A scene image should establish the environment, camera orientation, lighting, time of day, and persistent set dressing. Keep characters out unless the user explicitly requests a populated keyframe.

## Prop assets

Create one image per key prop, not one collage per scene. Record the prop name, owning scene(s), appearance, scale, interaction, reference source, and final file path. Use transparent background only when it improves compositing or H3 reference fidelity.

## Optional assets to ask about

Ask only for assets that materially affect the requested video: motion references, first/last keyframes, alternate costumes, action studies, animal behavior references, logos or physical signage, music, sound effects, special effects, and pronunciation/voice references.
