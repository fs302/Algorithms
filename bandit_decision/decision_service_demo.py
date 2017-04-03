from task import *
from decisioncenter import *
import numpy as np
from collections import defaultdict
from matplotlib import pylab as plt

def run_experiment(samples, task, decisionCenter):

    sample_count = 0
    hit_count = 0
    miss_count = 0
    precision = []
    regret = []
    for data in samples:
    	sample_count += 1
    	if len(data)<4:
    		continue
    	timestamp = int(data[0])
    	level = data[1]
    	gender = data[2]
    	real_decision = int(data[3])
    	choice,source_type = decisionCenter.decide(task,(level,gender),0)
    	decisionCenter.update_model(task,(level,gender),choice,'imp',source_type)
    	if choice == real_decision:
    		decisionCenter.update_model(task,(level,gender),real_decision,'clk',source_type)
    	hit = 1 if choice==real_decision else 0
    	hit_count += hit
    	miss_count += (1-hit)
    	precision.append(1.0*hit_count/sample_count)
    	regret.append(miss_count)
    	if sample_count % 100000 == 0:
    		print sample_count,decisionCenter.name,'precision:',precision[-1],'regret:',regret[-1]
    return precision, regret

contexts = [(1,0),(2,0),(3,0),(4,0),(5,0),(1,1),(2,1),(3,1),(4,1),(5,1)]
decision_list = [0,1] # 0-item, 1-brand
task = Task(1, "test", contexts, decision_list)

request_file = open("data/request_merge.csv","r")
samples = []
sample_limit = 1000000
sample_count = 0
for line in request_file.readlines():
	data = line.split(",")
	samples.append(data)
	sample_count += 1
	if sample_count > sample_limit:
		break
request_file.close()

config_map1 = {'num_to_explore':1000}
naiveDecisionCenter = NaiveDecisionCenter(config_map1)
naive_precision,naive_regret = run_experiment(samples, task, naiveDecisionCenter)

config_map2 = {'num_to_explore':100, 'epsilon':0.1, 'epsilon_decay': True, 'decay_step': 0.001, 'min_epsilon': 0.001}
epsilonGreedyDecisionCenter = EpsilonGreedyDecisionCenter(config_map2)
epsilon_precision, epsilon_regret = run_experiment(samples, task, epsilonGreedyDecisionCenter)

ucbNormalDecisionCenter = UCBNormalDecisionCenter(None)
ucb_precision, ucb_regret = run_experiment(samples, task, ucbNormalDecisionCenter)

thompsonSamplingDecisionCenter = ThompsonSamplingDecisionCenter(None)
tps_precision, tps_regret = run_experiment(samples, task, thompsonSamplingDecisionCenter)

x = range(len(naive_precision))
plt.loglog(x,np.array(naive_precision),\
	x,np.array(epsilon_precision),\
	x,np.array(ucb_precision),\
	x,np.array(tps_precision) )
plt.legend(('Naive','Epsilon-Greedy','UCB-Normal','ThompsonSampling'),loc='lower right')
plt.show()

