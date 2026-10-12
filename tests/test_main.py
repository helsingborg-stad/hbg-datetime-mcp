"""Tests for the datetime conversion tools."""

import unittest
from zoneinfo import ZoneInfoNotFoundError

from main import iso_to_unix, unix_to_iso


class ConversionToolsTests(unittest.IsolatedAsyncioTestCase):
    """Verify batched datetime conversions."""

    async def test_iso_to_unix_returns_pairs_in_input_order(self):
        """Convert multiple offset-aware ISO strings without losing their offsets."""
        iso_times = ["1970-01-01T00:00:00+00:00", "1970-01-01T02:00:00+01:00"]

        result = await iso_to_unix(iso_times)

        self.assertEqual(result, [
            {"iso": iso_times[0], "unix": 0},
            {"iso": iso_times[1], "unix": 3600},
        ])

    async def test_unix_to_iso_returns_utc_pairs_in_input_order(self):
        """Convert multiple Unix timestamps to paired UTC ISO strings."""
        unix_times = [0, -1, 3600]

        result = await unix_to_iso(unix_times)

        self.assertEqual(result, [
            {"iso": "1970-01-01T00:00:00+00:00", "unix": 0},
            {"iso": "1969-12-31T23:59:59+00:00", "unix": -1},
            {"iso": "1970-01-01T01:00:00+00:00", "unix": 3600},
        ])

    async def test_unix_to_iso_uses_iana_zone_offsets_for_each_timestamp(self):
        """Use the zone's winter and summer offsets for the corresponding dates."""
        unix_times = [1704067200, 1719792000]

        result = await unix_to_iso(unix_times, zone="Europe/Stockholm")

        self.assertEqual(result, [
            {"iso": "2024-01-01T01:00:00+01:00", "unix": 1704067200},
            {"iso": "2024-07-01T02:00:00+02:00", "unix": 1719792000},
        ])

    async def test_unix_to_iso_rejects_unknown_zone(self):
        """Reject an IANA zone name that cannot be resolved."""
        unix_times = [0]

        with self.assertRaises(ZoneInfoNotFoundError):
            await unix_to_iso(unix_times, zone="Not/A_Zone")

    async def test_iso_to_unix_returns_empty_list_for_empty_input(self):
        """Return no converted values when given no ISO strings."""
        iso_times = []

        result = await iso_to_unix(iso_times)

        self.assertEqual(result, [])

    async def test_unix_to_iso_returns_empty_list_for_empty_input(self):
        """Return no converted values when given no timestamps."""
        unix_times = []

        result = await unix_to_iso(unix_times)

        self.assertEqual(result, [])

    async def test_iso_to_unix_rejects_invalid_iso_string(self):
        """Propagate a parse error for an invalid value in a batch."""
        iso_times = ["1970-01-01T00:00:00+00:00", "invalid"]

        with self.assertRaises(ValueError):
            await iso_to_unix(iso_times)


if __name__ == "__main__":
    unittest.main()
