from MasterV1 import Master

if __name__ == '__main__':
    work_queue = 'work_queue_v1'
    count_queue = 'count_queue_v1'
    master = Master(work_queue, count_queue)
    master.start_managing(10)