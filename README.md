# HBG Datetime MCP server

Provides date and time functionality to AI that cannot
otherwise access it.

The `iso_to_unix` and `unix_to_iso` tools accept arrays and return one
`{"iso": ..., "unix": ...}` object per input, in the same order. For example:

```json
{"iso_times": ["1970-01-01T00:00:00+00:00", "1970-01-01T01:00:00+00:00"]}
```

`iso_to_unix` returns:

```json
[{"iso": "1970-01-01T00:00:00+00:00", "unix": 0}, {"iso": "1970-01-01T01:00:00+00:00", "unix": 3600}]
```

`unix_to_iso` takes `{"unix_times": [0, 3600]}` and returns the same pairs
with UTC ISO strings. Pass an optional IANA zone to use its local offset
instead, including daylight saving time changes:

```json
{"unix_times": [1704067200, 1719792000], "zone": "Europe/Stockholm"}
```

This returns ISO strings `2024-01-01T01:00:00+01:00` and
`2024-07-01T02:00:00+02:00` alongside the original Unix timestamps.
