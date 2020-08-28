import logging
import asyncio
import meteoblue_dataset_sdk


async def main():
    # query1 = {"units": {"temperature": "C", "velocity": "km/h", "length": "metric", "energy": "watts"}, "geometry": {"type": "Polygon", "coordinates": [[[2.96894, 46.041886], [2.96894, 48.216537], [10.989692, 48.216537], [10.989692, 46.041886], [2.96894, 46.041886]]]}, "format": "json", "timeIntervals": [
    #    "2017-01-01T+00:00/2019-01-31T+00:00"], "timeIntervalsAlignment": "none", "queries": [{"domain": "NEMSGLOBAL", "gapFillDomain": None, "timeResolution": "hourly", "codes": [{"code": 11, "level": "2 m above gnd"}], "transformations": [{"type": "aggregateTimeInterval", "aggregation": "mean"}, {"type": "spatialTotalAggregate", "aggregation": "mean"}]}]}

    query2 = {"units": {"temperature": "C", "velocity": "km/h", "length": "metric", "energy": "watts"}, "geometry": {"type": "MultiPoint", "coordinates": [[7.57327, 47.558399, 279]], "locationNames": ["Basel"]}, "format": "json", "timeIntervals": [
        "2019-01-01T+00:00/2019-01-01T+00:00"], "timeIntervalsAlignment": "none", "queries": [{"domain": "NEMSGLOBAL", "gapFillDomain": None, "timeResolution": "hourly", "codes": [{"code": 11, "level": "2 m above gnd"}]}]}
    # import mbdataset
    mb = meteoblue_dataset_sdk.Client(apikey='xxxxxx')  # ask for key
    a = await mb.query(query2)
    print(a)

    timesteps = a.geometries[0].timeIntervals[0].timestamps
    logging.debug(timesteps)
    data = a.geometries[0].codes[0].timeIntervals[0].data
    logging.debug(data)
    # query1 = asyncio.create_task(mb.query_async(qparams))
    # query2 = asyncio.create_task(mb.query_async(qparams))
    # res1 = await query1
    # res2 = await query2
    # async with mb.query(query1) as response:
    #    json = await response.json()
    #    print(json)
    # print(res1)
    # print(res2)


if __name__ == "__main__":
    logging.basicConfig(
        # filename=self._config.log_file,
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    asyncio.run(main())
