# Storyboard format

All paths are relative to the JSON file. An `@` prefix selects a bundled skill asset. Coordinates use pixels in the resized phone, not the full canvas. Rectangle `crop`, `patches.box`, and `taps.box` use `[left, top, right, bottom]`; `phone` and `overlays.box` use `[x, y, width, height]`.

See the runnable repository example in `examples/`. A minimal project:

```json
{
  "background": "#9FE870",
  "screens": {
    "home": {"file": "screens/home.jpg", "crop": [345,118,735,962]},
    "review": {"file": "screens/review.jpg", "crop": [345,118,735,962]}
  },
  "scenes": [
    {"screen":"home", "hold":2, "taps":[{"at":1.88,"box":[16,756,374,804]}]},
    {"screen":"review", "transition":{"type":"push","duration":0.52}, "hold":2}
  ]
}
```

## Canvas and screens

- `canvas`: `[1080,1080]`, even dimensions required; `fps`: 60.
- `phone`: `[345,118,390,844]`; `radius`: 40.
- `background`: hex color. Optional `background_image` fills the canvas and stays still.
- `logo`: `@wise-logo.png`; set null to disable. `logo_size`: `[240,230]` maximum fit.
- `intro`: .8 seconds (logo then subtle phone entrance); `outro`: 1.5 seconds (phone exit then logo hold). Set to 0 to disable. At least .8 seconds each is recommended for a clean loop.
- `screens`: map of names to `file`, optional `crop`, `flatten_radius` (42), `top_fill`, `bottom_fill`. Each is resized to phone dimensions. For clean rectangular screen exports, set `flatten_radius: 0`. For photographed rounded frames, sample-fill corners to remove the old backdrop; override colors for gradients or unusual chrome.

## Scenes and timing

Total duration = intro + sum of incoming transitions + holds + outro. First scene has no incoming transition. Scene local time begins when its incoming transition starts; all overlay and tap times use this clock. Place a press .12 seconds before the next transition begins: `at = transition.duration + hold - .12`. Holds start after transition completion.

`transition.type`:

- `cut`: instant, zero duration.
- `push`: incoming full page from right, outgoing parallax.
- `rise`: incoming full page from bottom.
- `fade`: full-page crossfade.
- `modal-in`: incoming screen's sheet rises over dimmed outgoing page.
- `modal-out`: outgoing sheet drops to reveal incoming page.

`duration` defaults to .52; explicitly use .65/.60 for modal in/out. Modal options: `top:54`, `radius:32`, `dim:0.25`. The top status-bar strip in the modal screenshot is excluded from the sheet. Use `fade` of .28 seconds to switch currency options within a modal. The current/next image includes its overlays during transitions, keeping success animation synchronized.

`taps`: list of `{ "at": seconds, "box": [l,t,r,b] }` with built-in 190 ms press feedback.

`patches`: list of `{ "box": [l,t,r,b], "fill":"#163300" }`, applied before overlays. Use to erase static icons under moving artwork only when the underlying area is a flat color.

## Media overlays

`overlays`: list, composited in order, each with:

- `file`: PNG, GIF, MP4, MOV or WebM.
- `box`: `[x,y,width,height]` inside phone. Video fills/crops to fit; PNG/GIF resize to these dimensions. Prepare the intended aspect ratio first.
- `start`: scene-local seconds (0); optional `end` removes overlay at that time.
- `loop`: true; false freezes on last frame. `speed`: 1.
- Video only: `fps`:30, `trim_start`:0, `max_duration`:10. Set success to fps60. Decode is memory-resident: crop to the small viewport and bound the duration.
- `blur`: Gaussian radius, useful for camera footage during scanning.
- Optional `chroma_key`: `[r,g,b]`, `key_threshold`:10, `key_softness`:24; removes flat-color backgrounds. Inspect edge quality against the actual target screen.

GIF frame durations and transparency are preserved. Use transparent scanner brackets and loader overlays over blurred camera footage. The generic renderer does not automatically isolate scanner artwork from a screenshot.

For the supplied success clip, sample its background pixel to configure the key rather than guessing. Patch out any static checkmark first; use `start:0` and `loop:false` to start with the page transition.

## Beyond the schema

Typing, moving keypads, zooms, individual controls and complex pre-modal dim phases require a project-local Python adaptation. Preserve supplied assets and established motion curves, then validate the new states and transition midpoints. Do not approximate these with full-screen cuts without telling the user.
