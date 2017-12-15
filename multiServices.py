import docker
from docker import types

client = docker.from_env()

if client.swarm.leave(force=True):

    client.swarm.init()

    client.services.create("nclcloudcomputing/javabenchmarkapp",
                           name="images",
                           endpoint_spec=types.EndpointSpec(mode="vip", ports={5050: 8080}),
                           mode=types.ServiceMode(mode="replicated", replicas=2))

    client.services.create("dockersamples/visualizer",
                           name="vis",
                           endpoint_spec=types.EndpointSpec(mode="vip", ports={4000: 8080}),
                           mounts=["/var/run/docker.sock:/var/run/docker.sock"])

    client.services.create("mongo",
                           name="mongoDB",
                           endpoint_spec=types.EndpointSpec(mode="vip", ports={27017: 27017}),
                           mounts=['db:/data/db'])

