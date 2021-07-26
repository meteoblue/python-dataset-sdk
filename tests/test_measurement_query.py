from meteoblue_dataset_sdk.protobuf.measurements_pb2 import MeasurementApiProtobuf
import meteoblue_dataset_sdk

import asyncio
import logging
import os
import unittest


class TestMeasurementQuery(unittest.TestCase):
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

    def test_invalid_table_key(self):
        client = meteoblue_dataset_sdk.Client(os.environ["APIKEY"])
        path = "/rawdata/dwdClimateHourly/notATable/get"
        with self.assertRaises(meteoblue_dataset_sdk.ApiError):
            result = asyncio.run(client.measurement_query(path, {"invalid": "query"}))
            self.assertEqual(
                result,
                "API returned error message: Unknown table notATable for provider dwdClimateHourly"
            )

    def test_invalid_api_key(self):
        client = meteoblue_dataset_sdk.Client("invalid_api_key")
        path = "/rawdata/dwdClimateHourly/dwdClimateMeasurementHourlyAirTemperature/get"
        with self.assertRaises(meteoblue_dataset_sdk.ApiError):
            result = asyncio.run(client.measurement_query(path, {"invalid": "query"}))
            self.assertEqual(
                result,
                "API returned error message: Invalid API Key"
            )

    def test_simple_query(self):
        query = {
            "timeStart": "2020-01-01T12:00:00",
            "timeEnd": "2020-01-02T12:00:00",
            "limit": 10,
            "sort": "asc",
            "stations": ["00044"],
            "fields": [
                "id",
                "timestamp",
                "lat",
                "lon",
                "asl",
                "temperature_2mAbvGnd_atTimestamp_none_degCels"
                ]
            }
        path = "/rawdata/dwdClimate10Minute/dwdClimateMeasurement10MinuteAirTemperature/get"

        client = meteoblue_dataset_sdk.Client(os.environ["APIKEY"])
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
            result,
            "temperature_2mAbvGnd_atTimestamp_none_degCels"
        )

        self.assertEqual(rows_per_page, 10)
        self.assertEqual(current_page, 1)
        self.assertEqual(rows_count, 10)
        self.assertEqual(
            timestamps,
            [
                1577880000,
                1577880600,
                1577881200,
                1577881800,
                1577882400,
                1577883000,
                1577883600,
                1577884200,
                1577884800,
                1577885400
            ]
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
                "00044"
            ]
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
                52.93360137939453
            ]
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
                8.237000465393066
            ]
        )
        self.assertEqual(
            asls,
            [
                44.0,
                44.0,
                44.0,
                44.0,
                44.0,
                44.0,
                44.0,
                44.0,
                44.0,
                44.0
            ]
        )
        self.assertEqual(
            temperatures,
            [
                -0.8999999761581421,
                -1.2000000476837158,
                -1.100000023841858,
                -0.8999999761581421,
                -0.8999999761581421,
                -0.800000011920929,
                -0.800000011920929,
                -0.800000011920929,
                -0.8999999761581421,
                -0.8999999761581421
            ]
        )
