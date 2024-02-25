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
        while True:
            old_value = distributed_map.get(key)
            new_value = old_value + 1
            if distributed_map.replace_if_same(key, old_value, new_value):
                break
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