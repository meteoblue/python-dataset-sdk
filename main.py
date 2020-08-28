import logging
import asyncio
import meteoblue_dataset_sdk


async def myFunction():
    # query1 = {"units": {"temperature": "C", "velocity": "km/h", "length": "metric", "energy": "watts"}, "geometry": {"type": "Polygon", "coordinates": [[[2.96894, 46.041886], [2.96894, 48.216537], [10.989692, 48.216537], [10.989692, 46.041886], [2.96894, 46.041886]]]}, "format": "json", "timeIntervals": [
    #    "2017-01-01T+00:00/2019-01-31T+00:00"], "timeIntervalsAlignment": "none", "queries": [{"domain": "NEMSGLOBAL", "gapFillDomain": None, "timeResolution": "hourly", "codes": [{"code": 11, "level": "2 m above gnd"}], "transformations": [{"type": "aggregateTimeInterval", "aggregation": "mean"}, {"type": "spatialTotalAggregate", "aggregation": "mean"}]}]}

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
        "queries": [
            {
                "domain": "NEMSGLOBAL",
                "gapFillDomain": None,
                "timeResolution": "hourly",
                "codes": [{"code": 11, "level": "2 m above gnd"}],
            }
        ],
    }
    client = meteoblue_dataset_sdk.Client(apikey="xxxxxx")  # ask for key
    result = await client.query(query)
    # result is a structured object containing timestamps and data

    timestamps = result.geometries[0].timeIntervals[0].timestamps
    data = result.geometries[0].codes[0].timeIntervals[0].data

    print(timestamps)
    # [1546300800, 1546304400, 1546308000, 1546311600, 1546315200, ...
    print(data)
    # [2.89, 2.69, 2.549999, 2.3800001,

    # query1 = asyncio.create_task(mb.query(qparams))
    # query2 = asyncio.create_task(mb.query(qparams))
    # res1 = await query1
    # res2 = await query2
    # async with mb.query(query1) as response:
    #    json = await response.json()
    #    print(json)
    # print(res1)
    # print(res2)


logging.basicConfig(
    # filename=self._config.log_file,
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)

asyncio.run(myFunction())
