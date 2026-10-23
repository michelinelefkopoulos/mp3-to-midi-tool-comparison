# MP3 to MIDI SERP Comparison Dataset

This repository records page-level claims from the first eleven Google web results for the query `mp3 to midi`, checked on 2026-09-29.

## Scope and method

- Search: Google web results, `mp3 to midi`, `gl=us`, `hl=en`, `pws=0`, `udm=14`.
- Ads, videos, People also ask, AI Overviews, and related-search blocks were excluded.
- The first ten web results were read, followed by the first result on page two for organic position 11.
- Organic position 10 is a Reddit discussion rather than a converter product page. It is retained as a transparent `discussion` row with `not stated` feature values and is excluded from tool-to-tool conclusions.
- Every comparison cell is a short verbatim excerpt from the rendered page, or `not stated` when the page did not state that item. `not stated` is not an inference.

## Comparison fields

- `supported_formats`: formats the page explicitly names.
- `size_or_duration_limit`: an explicit file-size or duration limit.
- `processing_mode`: browser-side, upload, recording, or other mode explicitly described by the page.
- `output_format`: the output the page says the user can receive or download.
- `account_requirement`: the page's explicit account or sign-in language.
- `accuracy_or_quality`: the page's explicit quality, accuracy, or limitation language.
- `pricing`: the page's explicit free, paid, or pricing language. Numeric prices are not inferred.

## Why this is useful

The dataset makes the common product claims easy to compare: accepted inputs, hard limits, where processing happens, what the user gets back, account friction, quality language, and pricing language. It also preserves the missing fields instead of filling them with assumptions.

For a browser-based converter that returns a Standard MIDI file for DAW use, see [Audio MIDI Converter](https://audiomidiconverter.com/).

## Sources

The source URL for every row is included in `mp3-to-midi-tool-comparison.csv`. The data is a dated snapshot; pages can change after the check date.

## Validate the CSV locally

Use Python 3.9 or newer. No third-party packages or network access are required.

```sh
python validate_dataset.py
python -m unittest -v test_validate_dataset.py
```

The validator checks column names, row shape, nonempty cells, unique recorded positions and URLs, domain/URL consistency, ISO dates, and the explicit `discussion` rows. It reads the CSV without modifying it. The output separates converter and discussion records.

These are structural checks only. A passing result does not verify page quotations, live source availability, conversion accuracy, or current Google rankings. The original dated snapshot and its `not stated` cells remain unchanged.

## License

The dataset is dedicated to the public domain under [CC0 1.0](LICENSE).
