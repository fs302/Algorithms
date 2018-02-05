import multiprocessing as mp 
import random
import string

random.seed(323)

def rand_string(i, length, output):
	rand_str = ''.join(random.choice(string.ascii_lowercase
									+ string.ascii_uppercase
									+ string.digits) 
						for i in range(length))
	output.put((i,str(i)+"_"+rand_str))

def rand_string2(i, length):
	rand_str = ''.join(random.choice(string.ascii_lowercase
									+ string.ascii_uppercase
									+ string.digits) 
						for i in range(length))
	return (i,str(i)+"_"+rand_str)

def test_process():
	output = mp.Queue()
	processes = [mp.Process(target=rand_string, args=(i, 5, output)) for i in range(100000)]
	for p in processes:
		p.start()
	for p in processes:
		p.join()
	results = [output.get() for p in processes]
	results.sort()
	final_results = [r[1] for r in results]
	print final_results


def test_pool():
	pool = mp.Pool(processes=4)
	results = [pool.apply(rand_string2, args=(i, 5)) for i in range(100000)]
	print results

if __name__=='__main__':
	# test_process()
	test_pool()