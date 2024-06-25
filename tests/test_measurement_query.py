from math import isnan
from meteoblue_dataset_sdk import ApiError, Client
from meteoblue_dataset_sdk.caching import FileCache
from meteoblue_dataset_sdk.protobuf.measurements_pb2 import MeasurementApiProtobuf

import asyncio
import logging
import os
import unittest


class TestMeasurementQuery(unittest.TestCase):
    def assertIsNaN(self, value: float):
        self.assertTrue(isnan(value))

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    @staticmethod
    def getColumnValues(message: MeasurementApiProtobuf, column: str):
        filtered_column = [col for col in message.columns if col.column == column]
        if filtered_column:
            col = filtered_column[0]
            col_type = col.values.WhichOneof("oneof_values")
            if col_type == "strings":
                return col.values.strings.array
            elif col_type == "floats":
                return col.values.floats.array
            elif col_type == "ints64":
                return col.values.ints64.array
            elif col_type == "ints32":
                return col.values.ints32.array
            elif col_type == "uints64":
                return col.values.uint64.array
            elif col_type == "uints32":
                return col.values.uints32.array
            elif col_type == "bools":
                return col.values.bools.array

    def test_invalid_table_key(self):
        client = Client(os.environ["APIKEY"])
        path = "/v2/dwdClimateHourly/raw/invalid/get"
        expected_error_message = (
            "API returned error message:"
            " Unknown table invalid for provider dwdClimateHourly"
        )
        with self.assertRaises(ApiError):
            result = asyncio.run(client.measurement_query(path, {"invalid": "query"}))
            self.assertEqual(
                result,
                expected_error_message,
            )

    def test_invalid_api_key(self):
        client = Client("invalid_api_key")
        provider = "dwdClimateHourly"
        table = "measurement"
        path = f"/v2/{provider}/raw/{table}/get"

        with self.assertRaises(ApiError):
            result = asyncio.run(client.measurement_query(path, {"invalid": "query"}))
            self.assertEqual(result, "Apikey was specified, but is not valid.")

    def test_simple_query(self):
        query = {
            "timeStart": "2024-05-01T12:00:00",
            "timeEnd": "2024-05-02T12:00:00",
            "limit": 10,
            "sort": "asc",
            "stations": ["00044"],
            "fields": [
                "id",
                "timestamp",
                "lat",
                "lon",
                "asl",
                "temperature_2mAbvGnd_atTimestamp_none_degCels",
            ],
        }
        provider = "dwdClimate10Minute"
        table = "measurement"
        path = f"/v2/{provider}/raw/{table}/get"

        cache = FileCache()
        client = Client(os.environ["APIKEY"], cache=cache)
        result = asyncio.run(client.measurement_query(path, query))
        rows_per_page = result.rows_per_page
        current_page = result.current_page
        rows_count = result.rows_count
        timestamps = self.getColumnValues(result, "timestamp")
        station_ids = self.getColumnValues(result, "id")
        lats = self.getColumnValues(result, "lat")
        lons = self.getColumnValues(result, "lon")
        asls = self.getColumnValues(result, "asl")
        temperatures = self.getColumnValues(
            result, "temperature_2mAbvGnd_atTimestamp_none_degCels"
        )

        self.assertEqual(rows_per_page, 10)
        self.assertEqual(current_page, 1)
        self.assertEqual(rows_count, 10)
        self.assertEqual(
            timestamps,
            [
                1714564800,
                1714565400,
                1714566000,
                1714566600,
                1714567200,
                1714567800,
                1714568400,
                1714569000,
                1714569600,
                1714570200,
            ],
        )
        self.assertEqual(
            station_ids,
            [
                "00044",
                "00044",
                "00044",
                "00044",
                "00044",
                "00044",
                "00044",
                "00044",
                "00044",
                "00044",
            ],
        )
        self.assertEqual(
            lats,
            [
                52.93360137939453,
                52.93360137939453,
                52.93360137939453,
                52.93360137939453,
                52.93360137939453,
                52.93360137939453,
                52.93360137939453,
                52.93360137939453,
                52.93360137939453,
                52.93360137939453,
            ],
        )
        self.assertEqual(
            lons,
            [
                8.237000465393066,
                8.237000465393066,
                8.237000465393066,
                8.237000465393066,
                8.237000465393066,
                8.237000465393066,
                8.237000465393066,
                8.237000465393066,
                8.237000465393066,
                8.237000465393066,
            ],
        )
        self.assertEqual(
            asls, [44.0, 44.0, 44.0, 44.0, 44.0, 44.0, 44.0, 44.0, 44.0, 44.0]
        )
        self.assertIsNaN(temperatures[0])
        self.assertAlmostEqual(temperatures[1], 25.6, 1)
        self.assertAlmostEqual(temperatures[2], 26, 1)
        self.assertIsNaN(temperatures[3])
        self.assertAlmostEqual(temperatures[4], 26.1, 1)
        self.assertAlmostEqual(temperatures[5], 26.1, 1)
        self.assertIsNaN(temperatures[6])
        self.assertAlmostEqual(temperatures[7], 26.4, 1)
        self.assertAlmostEqual(temperatures[8], 26.1, 1)
        self.assertIsNaN(temperatures[9])
