import hazelcast
import multiprocessing


def client_simulation():
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5701"],
        lifecycle_listeners=[
            lambda state: print("Lifecycle event >>>", state),
        ]
    )
    distributed_map = client.get_map("distributed-map")

    for i in range(10000):
        value = distributed_map.get("key").result()
        value += 1
        distributed_map.put("key", value)
    client.shutdown()

if __name__ == '__main__':
    client = hazelcast.HazelcastClient(
            cluster_name="dev",
            cluster_members=["127.0.0.1:5701"],
            lifecycle_listeners=[
                lambda state: print("Lifecycle event >>>", state),
            ]
        )
    distributed_map = client.get_map("distributed-map")
    distributed_map.put("key", 0).result()

    processes = []
    for i in range(3):
        process = multiprocessing.Process(target=client_simulation)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    value = distributed_map.get("key").result()
    print("Value at the end:", value)
    client.shutdown()
