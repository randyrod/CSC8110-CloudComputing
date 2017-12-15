from pymongo import MongoClient
from datetime import datetime

mongoClient = MongoClient()
db = mongoClient.stats

collection = db.benchmark

previous_cpu = -1
previous_system = -1
# print '['
for obj in collection.find():
    # print obj['cpu']['usage']
    # print ','
# print ']'

    percentage = 0.0
    current_cpu = obj['cpu']['usage']['total']
    current_system = obj['cpu']['usage']['user']
    cpu_cores = len(obj['cpu']['usage']['per_cpu_usage'])
    if previous_cpu == -1 or previous_system == -1:
        previous_cpu = current_cpu
        previous_system = current_system
    else:
        cpu_delta = float(current_cpu - previous_cpu)
        system_delta = float(current_system - previous_system)

        print "CPU Delta" + " " + str(cpu_delta)
        print "System Delta" + " " + str(system_delta)
        if cpu_delta > 0.0 and system_delta > 0.0:
            percentage = (system_delta / cpu_delta) * cpu_cores * 100

        previous_cpu = current_cpu
        previous_system = current_system
    print percentage
