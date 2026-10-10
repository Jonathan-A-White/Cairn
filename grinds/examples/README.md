# Grind examples

Each grind in `grinds/<kind>.json` keeps one or more scenarios, BDD-style, under
`grinds/examples/<kind>/<name>.json`. A scenario is what the app sends (the request and
its photos) and what the answer must show (`expect`). `mw grist smoke cairn` sends the
request to the real grist and checks the answer against `expect`; the app's unit test
(`src/bridge/grindExamples.test.ts`) checks every scenario's shape without a network.

```json
{
  "description": "One plain sentence: the situation and what must come back.",
  "request": {
    "schemaVersion": "1.1",
    "requestType": "sweep",
    "place": { "name": "Top drawer", "path": "Kitchen -> Top drawer" }
  },
  "photos": ["blank-wall.jpg"],
  "expect": {
    "placeName": "Top drawer",
    "items": { "equals": [] },
    "note": { "present": true }
  }
}
```

- `request`: the grind's input exactly as the app sends it, `schemaVersion` included;
  valid against the input schema (`contexts/inventory/schemas/<kind>-request-<version>.schema.json`).
  Its `schemaVersion` is one of the grind's `versions`.
- `photos`: file names beside the scenario (`.jpg`, `.png` or `.webp`), as many as the
  grind's `attachments` allow. Public-safe only: no people, no personal data, a synthetic
  or staged picture, under 200 KB. Scenarios may share a photo.
- `expect`: answer path to checks. A path is dotted, with array positions as numbers
  (`containers.0.items.0.name`). A bare value is `equals`. An object holds any of these
  checks, and every one given must hold:
  - `equals`: the value is exactly this
  - `is_null`: `true` the value is null, `false` it is not
  - `one_of`: the value is one of these
  - `contains`: a string includes this text (or a list has this element)
  - `matches`: a string matches this regular expression (keep to what Go and JavaScript
    share: no `(?i)`, lookaround or back-references)
  - `present`: `true` the field is in the answer, `false` it is left out

Every `expect` path must be a field of the grind's answer schema, and every `equals` or
`one_of` value must be one the schema allows. The check names are the ones `mw grist smoke`
reads (snake_case: `is_null`, `one_of`).

A story that changes a grind's behaviour updates or adds its scenarios in the same story.
A new grind needs at least one scenario or the unit test fails.

The photos are staged pictures made for these scenarios (flat colour and lettering), not
photographs of anyone's home.
