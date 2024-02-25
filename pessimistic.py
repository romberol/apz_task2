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
    distributed_map = client.get_map("distributed-map").blocking()
    key = "key"

    for i in range(10000):
        distributed_map.lock(key)
        try:
            value = distributed_map.get(key)
            value += 1
            distributed_map.put(key, value)
        finally:
            distributed_map.unlock(key)
    client.shutdown()

if __name__ == '__main__':
    client = hazelcast.HazelcastClient(
            cluster_name="dev",
            cluster_members=["127.0.0.1:5701"],
            lifecycle_listeners=[
                lambda state: print("Lifecycle event >>>", state),
            ]
        )
    distributed_map = client.get_map("distributed-map").blocking()
    distributed_map.put("key", 0)

    processes = []
    for i in range(3):
        process = multiprocessing.Process(target=client_simulation)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    value = distributed_map.get("key")
    print("Value at the end:", value)
    client.shutdown()
