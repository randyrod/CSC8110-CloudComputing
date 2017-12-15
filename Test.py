from datetime import datetime
import docker
import requests
import json
from pymongo import MongoClient
from time import sleep

baseUrl = 'http://localhost:6060/api/v1.3/containers/docker'
client = docker.from_env()
mongoClient = MongoClient()
db = mongoClient.stats
timeStampFormat = "%Y-%m-%dT%H:%M:%S.%f"


def convert_to_epoch(timestamp):
    return (timestamp - datetime(1970, 1, 1)).total_seconds()


def get_interval(current_date, previous_date):
    current_date_seconds = convert_to_epoch(current_date)
    previous_date_seconds = convert_to_epoch(previous_date)

    return long((current_date_seconds - previous_date_seconds)*1000000000)


def get_json_from_url(container_id):
    # type: (basestring) -> basestring
    url = baseUrl + "/" + container_id

    response = requests.get(url)

    if response.ok:
        response_content = json.loads(response.content)
        return response_content['stats']
    else:
        return ''


def persist_stats(elements, timestamp):
    previous_cpu = -1
    previous_timestamp = datetime.min
    for stat in elements:
        stat_date = datetime.strptime((stat['timestamp'])[:-2], timeStampFormat)

        if stat_date > timestamp:
            current_cpu = stat['cpu']['usage']['total']
            cpu_cores = len(stat['cpu']['usage']['per_cpu_usage'])
            current_timestamp = stat_date
            if previous_cpu == -1 or previous_timestamp == datetime.min:
                previous_cpu = current_cpu
                previous_timestamp = current_timestamp
            else:
                cpu_delta = float(current_cpu - previous_cpu)
                cpu_usage = float(cpu_delta / get_interval(current_timestamp, previous_timestamp))
                cpu_percentage = (cpu_usage / cpu_cores * 100)

                print cpu_percentage

                previous_cpu = current_cpu
                previous_timestamp = current_timestamp


def main():

    last_time_stamp = datetime.min

    while True:

        for container in client.containers.list(filters={"label": "com.docker.swarm.service.name=images"}):
            stats = get_json_from_url(container.id)
            if stats != '':
                persist_stats(stats, last_time_stamp)
            break
        last_time_stamp = datetime.now()

        sleep(30)


if __name__ == '__main__':
    main()
