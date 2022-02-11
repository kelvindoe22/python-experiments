from threading import Thread
import random
import time


class Mutex():
    def __init__(self, value):
        self.value = value
        self.taken = False
        self.secret_pass = "could_be_anything_really"
    
    def get_secret_pass(self):
        if self.taken:
            return None
        else:
            self.taken = True
            return self.secret_pass

    def work(self, *args, **kwargs):
        pass
    
    def mutate_value(self,key, *args, **kwargs):
        a = args
        if key == self.secret_pass:
            self.work(*args)
    
    def done(self, key):
        if key == self.secret_pass:
            ls = list(self.secret_pass)
            random.shuffle(ls)
            self.secret_pass = ''.join(ls)
            self.taken = False

    





if __name__ == "__main__":
    class MyMutex(Mutex):
        def work(self, num):
            for i in range(num,100,num):
                self.value.append(i)

    mut = MyMutex([])
    
    def get_key_then_work(*args):
        global mut
        num = args[0]
        time.sleep(1/num)
        a = None
        while not a:
            a = mut.get_secret_pass()
        mut.mutate_value(a, *args)
        mut.done(a)


    thread_vec = []
    for i in range(2,5):
        t = Thread(target=get_key_then_work, args=(i,))
        t.start()
        thread_vec.append(t)
    
    for t in thread_vec:
        t.join()
    

    print(f"{mut.value}")




