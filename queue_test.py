import hazelcast
import multiprocessing
import time

def producer():
    client = hazelcast.HazelcastClient(cluster_name="dev")
    queue = client.get_queue("default").blocking()

    for i in range(100):
        queue.put(i)
        print("Put:", i)
    client.shutdown()
    print("queue shutdown")

def consumer(consumer_id):
    client = hazelcast.HazelcastClient(cluster_name="dev")
    queue = client.get_queue("default").blocking()
    time.sleep(1) # wait for some values to be putted
    while not queue.is_empty():
        value = queue.take()
        print(f"Client #{consumer_id} took from queue: {value}")

    client.shutdown()
    print('client shutdown')

if __name__ == "__main__":
    processes = [
        multiprocessing.Process(target=producer),
        multiprocessing.Process(target=consumer, args=(1,)),
        multiprocessing.Process(target=consumer, args=(2,))
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
