import time
import threading
from multiprocessing import Process, Pool

def func1(n):
	print('func1: starting')
	time.sleep(1.5)
	for i in range(n):
		pass
	print('func1: finishing')
	time.sleep(1.5)


def func2(n):
	print('func2: starting')
	time.sleep(1.5)
	for i in range(n):
		pass
	print('func2: finishing')
	time.sleep(1.5)


def run_all():
	ranges = [10, 20, 30]
	for i in ranges:
		t = threading.Thread(target=func1, args =[i])
		t.start()


if __name__=='__main__':
	run_all()
# 	p1 = Process(target=func1)
# 	p1.start()
# 	p2 = Process(target=func2)
# 	p2.start()
# 	p1.join()
# 	p2.join()



 



def printRange(lrange):
    print ("First is " + str(lrange[0]) + " and last is " + str(lrange[1]))

def runInParallel():
    ranges = [[0, 10], [10, 20], [20, 30]]
    for i in ranges:
        t = threading.Thread(target=printRange, args = [i])
        t.start()

# if __name__=='__main__':
# 	runInParallel()


