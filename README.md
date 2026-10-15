# Wise Product Video

A reusable Codex skill for creating Wise-style product demo videos from screenshots and a written storyboard. Includes a configurable Python renderer, Wise logo, spinning loader, and success animation.

## Test with your own screens

1. Clone this private repository and open the folder as a Codex project.
2. Add your screens to `projects/my-demo/screens/` (the `projects/` directory is ignored by Git).
3. Ask Codex:

   > Use $wise-product-video to create a video with these screens. Start on the home screen, tap Upload, show scanning, load the review screen, then tap Confirm and pay and show success. Use the green background and seamless logo loop. Save the editable storyboard and MP4 in projects/my-demo.

The skill lives at `.agents/skills/wise-product-video/` so it is available within this repository. To use it in another project, copy that whole folder into the project's `.agents/skills/`, or ask Codex's skill installer to install it from this repository. Team members need access to this private repository first. If the skill does not appear, restart Codex.

Provide screenshots plus the interaction order. Optional inputs include camera footage, transparent keyboard assets, GIFs, and desired timing. Full square frames or clean phone-screen exports both work; Codex should inspect and configure the crop. New projects do not depend on the original author's files or chat history.

## Run the example without Codex

Python 3.11 or 3.12 is recommended. From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r .agents/skills/wise-product-video/scripts/requirements.txt
.venv/bin/python examples/make_example.py
.venv/bin/python .agents/skills/wise-product-video/scripts/render.py examples/generated/storyboard.json --output output/example.mp4
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.

The generated example uses deliberately simple placeholder screens to demonstrate page slides, a bottom sheet, tap feedback and the branded loop. It is a renderer smoke test, not a finished product design. The renderer exports a contact sheet and performs a full FFmpeg decode check after encoding. Inspect the contact sheet and transitions before accepting a video.

## Defaults and limits

- 1080×1080, 60 fps, silent H.264 MP4.
- Solid #9FE870, fixed phone, subtle 24 px entrance/exit, logo at both ends.
- 190 ms tap feedback; .52 s page transitions; .65/.60 s modal transitions.
- Configurable screenshots, holds, crops, PNG/GIF/video overlays and chroma key.
- Typing, animated keypads and zooms require a project-local renderer adaptation; the skill explains how to preserve the established style.

See [SKILL.md](.agents/skills/wise-product-video/SKILL.md) for the workflow and [storyboard format](.agents/skills/wise-product-video/references/storyboard.md) for the JSON schema. All paths are relative to each storyboard; bundled assets use an `@` prefix. Dependencies include a bundled FFmpeg executable through imageio-ffmpeg.

Brand assets are provided for the team's Wise work. This repository does not grant a public license to Wise branding. Keep project inputs and rendered videos out of commits unless intentionally sharing them.
