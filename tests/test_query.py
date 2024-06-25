from meteoblue_dataset_sdk import ApiError, Client

import asyncio
import logging
import os
import unittest


class TestQuery(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_invalid_query(self):
        client = Client("invalid_api_key")
        with self.assertRaises(ApiError):
            result = asyncio.run(client.query({"invalid": "query"}))
            self.assertEqual(
                result, "API returned error message: Value required for key 'geometry'."
            )

    def test_simple_query(self):
        query = {
            "units": {
                "temperature": "C",
                "velocity": "km/h",
                "length": "metric",
                "energy": "watts",
            },
            "geometry": {
                "type": "MultiPoint",
                "coordinates": [[7.57327, 47.558399, 279]],
                "locationNames": ["Basel"],
            },
            "format": "json",
            "timeIntervals": ["2019-01-01T+00:00/2019-01-01T+00:00"],
            "timeIntervalsAlignment": "none",
            "runOnJobQueue": True,
            "queries": [
                {
                    "domain": "NEMSGLOBAL",
                    "gapFillDomain": None,
                    "timeResolution": "hourly",
                    "codes": [{"code": 11, "level": "2 m above gnd"}],
                }
            ],
        }

        client = Client(os.environ["APIKEY"])
        result = asyncio.run(client.query(query))
        geo = result.geometries[0]
        timeInterval = result.geometries[0].timeIntervals[0]
        variable = geo.codes[0]
        data = variable.timeIntervals[0].data

        self.assertEqual(geo.domain, "NEMSGLOBAL")
        self.assertEqual(geo.lats, [47.66651916503906])
        self.assertEqual(geo.lons, [7.5])
        self.assertEqual(geo.asls, [499.7736511230469])
        self.assertEqual(geo.locationNames, ["Basel"])
        self.assertEqual(geo.nx, 1)
        self.assertEqual(geo.ny, 1)
        self.assertEqual(geo.timeResolution, "hourly")

        self.assertEqual(variable.code, 11)
        self.assertEqual(variable.level, "2 m above gnd")
        self.assertEqual(variable.unit, "°C")
        self.assertEqual(variable.aggregation, "none")

        self.assertEqual(timeInterval.start, 1546300800)
        self.assertEqual(timeInterval.end, 1546383600 + 3600)
        self.assertEqual(timeInterval.stride, 3600)

        self.assertEqual(
            data,
            [
                2.890000104904175,
                2.690000057220459,
                2.549999952316284,
                2.380000114440918,
                2.2699999809265137,
                2.119999885559082,
                1.9900000095367432,
                1.8300000429153442,
                1.8200000524520874,
                2.0999999046325684,
                2.430000066757202,
                2.9200000762939453,
                3.7200000286102295,
                3.930000066757202,
                3.9100000858306885,
                3.5299999713897705,
                3.130000114440918,
                2.880000114440918,
                2.6500000953674316,
                2.4600000381469727,
                2.2799999713897705,
                2.0299999713897705,
                1.690000057220459,
                1.3799999952316284,
            ],
        )

    def test_complex_query(self):
        # This query is read half of Europe and 2 years of data
        # The API will refuse to run it directly
        query_complex = {
            "units": {
                "temperature": "C",
                "velocity": "km/h",
                "length": "metric",
                "energy": "watts",
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [2.96894, 46.041886],
                        [2.96894, 48.216537],
                        [10.989692, 48.216537],
                        [10.989692, 46.041886],
                        [2.96894, 46.041886],
                    ]
                ],
            },
            "format": "json",
            "timeIntervals": ["2017-01-01T+00:00/2019-01-31T+00:00"],
            "timeIntervalsAlignment": "none",
            "queries": [
                {
                    "domain": "NEMSGLOBAL",
                    "gapFillDomain": None,
                    "timeResolution": "hourly",
                    "codes": [{"code": 11, "level": "2 m above gnd"}],
                    "transformations": [
                        {"type": "aggregateTimeInterval", "aggregation": "mean"},
                        {"type": "spatialTotalAggregate", "aggregation": "mean"},
                    ],
                }
            ],
        }

        client = Client(os.environ["APIKEY"])
        result = asyncio.run(client.query(query_complex))
        geo = result.geometries[0]
        timestamps = geo.timeIntervals[0].timestrings
        variable = geo.codes[0]
        data = variable.timeIntervals[0].data

        self.assertEqual(geo.domain, "NEMSGLOBAL")
        self.assertEqual(len(geo.lats), 1)
        self.assertEqual(len(geo.lons), 1)
        self.assertAlmostEqual(geo.lats[0], 47.12916946411133, 3)
        self.assertAlmostEqual(geo.lons[0], 6.97930908203125, 3)
        self.assertEqual(geo.nx, 1)
        self.assertEqual(geo.ny, 1)
        self.assertEqual(geo.timeResolution, "total")

        self.assertEqual(variable.code, 11)
        self.assertEqual(variable.level, "2 m above gnd")
        self.assertEqual(variable.unit, "°C")
        self.assertEqual(variable.aggregation, "mean")

        self.assertEqual(timestamps, ["20170101T0000-20190131T235959"])
        self.assertEqual(len(data), 1)
        self.assertAlmostEqual(data[0], 8.519842147827148, 3)
