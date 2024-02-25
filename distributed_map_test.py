import hazelcast

client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
	    "127.0.0.1:5703"
    ],
    lifecycle_listeners=[
        lambda state: print("Lifecycle event >>>", state),
    ]
)

distributed_map = client.get_map("distributed-map")

for i in range(1000):
    distributed_map.set(str(i), f"value{i}").result()

print("Map size:", distributed_map.size().result())
client.shutdown()