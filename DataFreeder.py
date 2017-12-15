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
    for stat in elements:
        stat_date = datetime.strptime((stat['timestamp'])[:-2], timeStampFormat)

        if stat_date > timestamp:
            db.benchmark.insert_one(stat)
            print "Stat added to DB"


def main():

    last_time_stamp = datetime.min

    while True:

        for container in client.containers.list(filters={"label": "com.docker.swarm.service.name=images"}):
            stats = get_json_from_url(container.id)
            if stats != '':
                persist_stats(stats, last_time_stamp)

        last_time_stamp = datetime.now()

        sleep(60)


if __name__ == '__main__':
    main()
