from MasterV1 import Master
import threading
import time
import matplotlib.pyplot as plt
import subprocess
from pathlib import Path

def do_test():
    path_worker = Path(__file__).parent/'Client.py'
    procs = []
    for i in range(60):
        time.sleep(1)
        if i == 1:
            proc = subprocess.Popen(['python', path_worker]
                                    ,stdout = subprocess.DEVNULL)
            procs.append(proc)
        elif i == 7:
            proc = subprocess.Popen(['python', path_worker]
                                    ,stdout = subprocess.DEVNULL)
            procs.append(proc)
        elif i == 11:
            proc = subprocess.Popen(['python', path_worker]
                                    ,stdout = subprocess.DEVNULL)
            procs.append(proc)
        elif i == 21:
            proc = procs.pop()
            proc.terminate()
            proc = procs.pop()
            proc.terminate()
        elif i == 31:
            proc = subprocess.Popen(['python', path_worker]
                                    ,stdout = subprocess.DEVNULL)
            procs.append(proc)
        elif i == 41:
            proc = procs.pop()
            proc.terminate()
            proc = procs.pop()
            proc.terminate()
        elif i == 51:
            proc = subprocess.Popen(['python', path_worker]
                                    ,stdout = subprocess.DEVNULL)
            procs.append(proc)
        elif i == 59:
            for proc in procs:
                proc.terminate()


if __name__ == "__main__":
    # Connect to RabbitMQ
    work_queue = 'work_queue_v1'
    count_queue = 'count_queue_v1'
    master = Master(work_queue, count_queue)
    time_test = 60

    proc = threading.Thread(target=do_test)
    proc.start()
    time.sleep(1)
    master.start_managing_test(10, time_test)

    proc.join()

    time_stamp = []
    for i in range(60):
        if i % 2 == 0: time_stamp.append(i)

    plot, aux = plt.subplots(figsize=(16, 6))

    aux.plot(time_stamp, master.result_workers, 'r-o', label='Workers')
    aux.set_ylabel('Workers', color='r')
    aux.tick_params(axis='y')

    aux2 = aux.twinx()
    aux2.plot(time_stamp, master.result_rate, 'b-o', label='Petition Rate')
    aux2.set_ylabel('Rate', color='b')
    aux2.tick_params(axis='y')

    aux.set_xlabel('Seconds')
    # plt.legend()
    # plt.grid(True)
    plt.title("Dynamic Scaling")
    plt.show()