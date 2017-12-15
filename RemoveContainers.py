import docker

client = docker.from_env()

print "Services:\n"
for service in client.services.list():
    service.remove()
    print service.id

print "Containers:\n"
for container in client.containers.list():
    container.remove(force=True)
    print container.id


