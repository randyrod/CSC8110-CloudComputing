import docker

client = docker.from_env()

image = client.images.pull("google/cadvisor:latest")

contain = client.containers.run(image.id,
                                detach=True,
                                ports={"8080/tcp": 6060},
                                volumes={"/": {"bind": "/rootfs", "mode": "ro"},
                                         "/var/run": {"bind": "/var/run", "mode": "rw"},
                                         "/sys": {"bind": "/sys", "mode": "ro"},
                                         "/var/lib/docker/": {"bind": "/var/lib/docker", "mode": "ro"}})

print contain.id
