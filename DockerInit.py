import docker

client = docker.from_env()

image = client.images.pull("nclcloudcomputing/javabenchmarkapp")

contain = client.containers.run(image.id,
                                detach=True,
                                ports={"8080/tcp": 8080})

print contain.id
