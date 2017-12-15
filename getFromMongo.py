from pymongo import MongoClient
from datetime import datetime

mongoClient = MongoClient()
db = mongoClient.stats

collection = db.benchmark


def convert_to_epoch(timestamp):
    return (timestamp - datetime(1970, 1, 1)).total_seconds()


def get_interval(current_date, previous_date):
    current_date_seconds = convert_to_epoch(current_date)
    previous_date_seconds = convert_to_epoch(previous_date)

    return long((current_date_seconds - previous_date_seconds)*1000000000)


timeStampFormat = "%Y-%m-%dT%H:%M:%S.%f"
previous_cpu = -1
previous_timestamp = datetime.min

for obj in collection.find():

    current_cpu = obj['cpu']['usage']['total']
    cpu_cores = len(obj['cpu']['usage']['per_cpu_usage'])
    current_timestamp = datetime.strptime((obj['timestamp'])[:-2], timeStampFormat)
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
