from collections import defaultdict
import operator
import random
import numpy as np

class BaseDecisionCenter(object):

	def __init__(self, config_map):

		self.name = 'BaseDecisionCenter'
		self.timestamp = defaultdict(int) # key: taskId
		self.impCount = defaultdict(int)
		self.clkCount = defaultdict(int)

    # return format: decision, source_type
	def decide(self, task, context, default_decision):
		return default_decision,'default_decision'

	def update_model(self, task, context, decision, log_type, source_type):
		pass

class NaiveDecisionCenter(BaseDecisionCenter):

	def __init__(self, config_map):
		BaseDecisionCenter.__init__(self, config_map)
		self.name = 'NaiveDecisionCenter'
		self.num_to_explore = config_map.get('num_to_explore',100)

	def decide(self, task, context, default_decision):
		self.timestamp[task.task_id] += 1
		if self.timestamp[task.task_id] < self.num_to_explore:
			return random.choice(task.decision_list),'random'
		else:
			return self.get_best_chioce(task, context, default_decision), 'best'

	def get_best_chioce(self, task, context, default_decision):
		candidate = {}
		for choice in task.decision_list:
			k = str(task.task_id)+"_"+str(choice)
			candidate[choice] = 1.0*self.clkCount[k]/self.impCount[k] if self.impCount[k]>0 else 0
		best_choice = max(candidate.iteritems(), key=operator.itemgetter(1))[0]
		if candidate[best_choice] > 0:
			return best_choice
		else: 
			return default_decision

	def update_model(self, task, context, decision, log_type, source_type):
		update_key = str(task.task_id)+"_"+str(decision)
		if self.timestamp > self.num_to_explore:
			return
		if log_type == 'imp':
			self.impCount[update_key] += 1
		if log_type == 'clk':
			self.clkCount[update_key] += 1

class EpsilonGreedyDecisionCenter(BaseDecisionCenter):

	def __init__(self, config_map):

		BaseDecisionCenter.__init__(self, config_map)
		self.name = 'EpsilonGreedyDecisionCenter'
		self.epsilon = config_map.get('epsilon',0.01)
		self.num_to_explore = config_map.get('num_to_explore',100)
		self.epsilon_decay = config_map.get('epsilon_decay',False)
		self.decay_step = config_map.get('decay_step',0.001)
		self.min_epsilon = config_map.get('min_epsilon',0.001)

	def decide(self, task, context, default_decision):
		contextStr = '|'.join(context)
		self.timestamp[task.task_id] += 1
		if self.epsilon_decay and self.epsilon > self.min_epsilon:
			self.epsilon -= self.decay_step
		r = random.random()
		if r < self.epsilon or self.timestamp[task.task_id] < self.num_to_explore:
			# random
			return random.choice(task.decision_list),'explore'
		else:
			# max
			return self.get_best_chioce(task, contextStr, default_decision),'exploit'

	def get_best_chioce(self, task, contextStr, default_decision):
		candidate = {}
		for choice in task.decision_list:
			k = str(task.task_id)+"_"+contextStr+"_"+str(choice)
			candidate[choice] = 1.0*self.clkCount[k]/self.impCount[k] if self.impCount[k]>0 else 0
		best_choice = max(candidate.iteritems(), key=operator.itemgetter(1))[0]
		if candidate[best_choice] > 0:
			return best_choice
		else: 
			return default_decision

	def update_model(self, task, context, decision, log_type, source_type):
		if source_type != 'explore':
			return
		contextStr = '|'.join(context)
		update_key = str(task.task_id)+"_"+contextStr+"_"+str(decision)
		if log_type == 'imp':
			self.impCount[update_key] += 1
		if log_type == 'clk':
			self.clkCount[update_key] += 1


def multi_result_random(dist,itemSplitor,kvSplitor):
    # dist like 'a:0.1^b:0.2^c:0.7', return a/b/c
    choice_probs = dist.split(itemSplitor)
    elevation = 0.0
    choice_queue = []
    total_volumn = 1e-6 + sum([float(choice_prob.split(kvSplitor)[1]) for choice_prob in choice_probs])
    for choice_prob in choice_probs:
        kv = choice_prob.split(kvSplitor)
        if len(kv) < 2:
            continue
        choice,prob = kv[0],float(kv[1])/total_volumn
        choice_queue.append((elevation + prob,choice))
        elevation += prob
    point = random.random()
    for choice in choice_queue:
        if choice[0] >= point:
            return choice[1]
    return choice_queue[-1][1]

class SoftEpsilonGreedyDecisionCenter(EpsilonGreedyDecisionCenter):

	def __init__(self, config_map):
		EpsilonGreedyDecisionCenter.__init__(self, config_map)
		self.name = 'SoftEpsilonGreedyDecisionCenter'

	def get_best_chioce(self, task, contextStr, default_decision):
		candidate = {}
		candidateProbability = []
		for choice in task.decision_list:
			k = str(task.task_id)+"_"+contextStr+"_"+str(choice)
			candidate[choice] = 1.0*self.clkCount[k]/self.impCount[k] if self.impCount[k]>0 else 0
			candidateProbability.append(str(choice)+":"+str(candidate[choice]))
		best_choice = int(multi_result_random('^'.join(candidateProbability),'^',':'))
		if candidate[best_choice] > 0:
			return best_choice
		else: 
			return default_decision

class UCBNormalDecisionCenter(BaseDecisionCenter):

	def __init__(self, config_map):
		BaseDecisionCenter.__init__(self, config_map)
		self.name = 'UCBNormalDecisionCenter'

    # return format: decision, source_type
	def decide(self, task, context, default_decision):
		candidate = {}
		contextStr = '|'.join(context)
		for choice in task.decision_list:
			k = str(task.task_id)+"_"+contextStr+"_"+str(choice)
			estimated_mean = 1.0*self.clkCount[k]/self.impCount[k] if self.impCount[k]>0 else 0
			estimated_variance = estimated_mean - estimated_mean**2
			candidate[choice] = estimated_mean + 1.96*np.sqrt(estimated_variance/(self.impCount[k]+1e-6))
		best_choice = max(candidate.iteritems(), key=operator.itemgetter(1))[0]
		if candidate[best_choice] > 0:
			return best_choice,'best_choice'
		else: 
			return default_decision,'default_decision'

	def update_model(self, task, context, decision, log_type, source_type):
		contextStr = '|'.join(context)
		update_key = str(task.task_id)+"_"+contextStr+"_"+str(decision)
		if log_type == 'imp':
			self.impCount[update_key] += 1
		if log_type == 'clk':
			self.clkCount[update_key] += 1


class ThompsonSamplingDecisionCenter(BaseDecisionCenter):

	def __init__(self, config_map):
		BaseDecisionCenter.__init__(self, config_map)
		self.name = 'ThompsonSamplingDecisionCenter'

    # return format: decision, source_type
	def decide(self, task, context, default_decision):
		candidate = {}
		contextStr = '|'.join(context)
		clk = []
		fail = []
		choices = []
		for choice in task.decision_list:
			k = str(task.task_id)+"_"+contextStr+"_"+str(choice)
			clk.append(1.0+self.clkCount[k])
			fail.append(1.0+self.impCount[k]-self.clkCount[k])
			choices.append(choice)
		best_choice = choices[np.argmax( np.random.beta(np.array(clk), np.array(fail)) )]
		if best_choice != None:
			return best_choice,'best_choice'
		else: 
			return default_decision,'default_decision'

	def update_model(self, task, context, decision, log_type, source_type):
		contextStr = '|'.join(context)
		update_key = str(task.task_id)+"_"+contextStr+"_"+str(decision)
		if log_type == 'imp':
			self.impCount[update_key] += 1
		if log_type == 'clk':
			self.clkCount[update_key] += 1