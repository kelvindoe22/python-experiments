from threading import Thread
import time

class Mutex():
    def __init__(self, value):
        self.value = value
        self.taken = False
        self.holder = None
    
    def lock(self, holder_id):
        if self.taken:
            return None
        else:
            self.taken = True
            self.holder = holder_id
            print(f"[*] Lock given to {holder_id}")
            return self.value
    
    def release(self, holder_id):
        if holder_id == self.holder:
            self.holder = None
            self.taken = False
            print("[*] Released lock")

class Worker:
    def __init__(self, mutex: Mutex):
        self.mutex = mutex
        self.val = None
        self.id = hash(self)

    def lock(self):
        while self.val == None:
            self.val = self.mutex.lock(self.id)

    def release(self):
        self.val = None
        self.mutex.release(self.id)
        






if __name__ == "__main__":
    mutex = Mutex([])
    

    # create workers for each thread
    class Worker1(Worker):
        def work(self, num):
            # Do your expensive computations here
            time.sleep(3)
            self.lock() # get the lock
            # do whatever you want to the value here
            for i in range(num, 500):
                self.val.append(i)
            self.release() # release the lock so others can use it

    
    class Worker2(Worker):
        def work(self):
            time.sleep(4)
            self.lock()
            if len(self.val) == 0:
                self.val.append(0)
            for i in range(1, 100):
                self.val[0] += i
            
            self.release()

    class Worker3(Worker):
        def isempty(self):
            return len(self.val) == 0
        
        def add(self):
            if self.isempty():
                return 0
            else:
                self.val[0] += 99
                return 1

        def sub(self):
            if self.isempty():
                return True
            else:
                self.val[1] -= 1000
                return False

        def sub_from_7(self):
            if len(self.val) > 7:
                for i in range(7):
                    self.val[i] - 100
                return False
            return True

        def work(self):
            control = True
            while control:
                self.lock()
                control = self.add()
                self.release()
            print("[*] Done")
            
            control = True
            
            time.sleep(2)

            while control:
                self.lock()
                control = self.sub()
                self.release()
            print("[*] Done")

            control = True
            
            time.sleep(3)

            while control:
                self.lock()
                control = self.sub_from_7()
                self.release()
             
            print("[*] Done")
            
    
    w1 = Worker1(mutex)
    w2 = Worker2(mutex)
    w3 = Worker3(mutex)

    thread_list = []

    t1 = Thread( target=w1.work, args=(200,) )
    t1.start()
    thread_list.append(t1)
    t2 = Thread( target=w2.work )
    t2.start()
    thread_list.append(t2)
    t3 = Thread( target=w3.work )
    t3.start()
    thread_list.append(t3)

    for t in thread_list:
        t.join()
    


    
    print(f"{mutex.value}")
    
