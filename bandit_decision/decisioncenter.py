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
		self.reset_num = config_map.get('reset_num',None)

    # return format: decision, source_type
	def decide(self, task, context, default_decision):
		self.timestamp[task.task_id] += 1
		return default_decision,'default_decision'

	def update_model(self, task, context, decision, log_type, source_type):
		pass

class NaiveDecisionCenter(BaseDecisionCenter):

	def __init__(self, config_map):
		BaseDecisionCenter.__init__(self, config_map)
		self.name = 'NaiveDecisionCenter'
		self.num_to_explore = config_map.get('num_to_explore',100)

	def decide(self, task, context, default_decision):
		BaseDecisionCenter.decide(self, task, context, default_decision)
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
		BaseDecisionCenter.decide(self, task, context, default_decision)
		# Optimize: reset for a round
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
			a = self.impCount[k] + 1
			b = self.clkCount[k] + 1
			candidate[choice] = 1.0*b/a
		best_choice = max(candidate.iteritems(), key=operator.itemgetter(1))[0]
		#print contextStr, candidate, best_choice
		if candidate[best_choice] > 0:
			return best_choice
		else: 
			return default_decision

	def update_model(self, task, context, decision, log_type, source_type):
		if source_type != 'explore':
			return
		contextStr = '|'.join(context)
		update_key = str(task.task_id)+"_"+contextStr+"_"+str(decision)
		if self.reset_num != None and self.timestamp[task.task_id] % self.reset_num == 0:
			self.impCount = defaultdict(int)
			self.clkCount = defaultdict(int)
		if log_type == 'imp':
			self.impCount[update_key] += 1
		if log_type == 'clk':
			self.clkCount[update_key] += 1

class UCBNormalDecisionCenter(BaseDecisionCenter):

	def __init__(self, config_map):
		BaseDecisionCenter.__init__(self, config_map)
		self.name = 'UCBNormalDecisionCenter'

    # return format: decision, source_type
	def decide(self, task, context, default_decision):
		BaseDecisionCenter.decide(self, task, context, default_decision)
		candidate = {}
		contextStr = '|'.join(context)
		for choice in task.decision_list:
			k = str(task.task_id)+"_"+contextStr+"_"+str(choice)
			a = self.impCount[k] + 1
			b = self.clkCount[k] + 1
			estimated_mean = 1.0*min(b/a,1) 
			estimated_variance = estimated_mean - estimated_mean**2
			candidate[choice] = estimated_mean + 1.96*np.sqrt(estimated_variance/a)
		best_choice = max(candidate.iteritems(), key=operator.itemgetter(1))[0]
		if candidate[best_choice] > 0:
			return best_choice,'best_choice'
		else: 
			return default_decision,'default_decision'

	def update_model(self, task, context, decision, log_type, source_type):
		contextStr = '|'.join(context)
		update_key = str(task.task_id)+"_"+contextStr+"_"+str(decision)
		if self.reset_num != None and self.timestamp[task.task_id] % self.reset_num == 0:
			self.impCount = defaultdict(int)
			self.clkCount = defaultdict(int)
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
		BaseDecisionCenter.decide(self, task, context, default_decision)
		candidate = {}
		contextStr = '|'.join(context)
		clk = []
		fail = []
		choices = []
		for choice in task.decision_list:
			k = str(task.task_id)+"_"+contextStr+"_"+str(choice)
			clk.append(1.0+self.clkCount[k])
			fail.append(1.0+max(self.impCount[k]-self.clkCount[k],0))
			choices.append(choice)
		best_choice = choices[np.argmax( np.random.beta(np.array(clk), np.array(fail)) )]
		if best_choice != None:
			return best_choice,'best_choice'
		else: 
			return default_decision,'default_decision'

	def update_model(self, task, context, decision, log_type, source_type):
		contextStr = '|'.join(context)
		update_key = str(task.task_id)+"_"+contextStr+"_"+str(decision)
		if self.reset_num != None and self.timestamp[task.task_id] % self.reset_num == 0:
			self.impCount = defaultdict(int)
			self.clkCount = defaultdict(int)
		if log_type == 'imp':
			self.impCount[update_key] += 1
		if log_type == 'clk':
			self.clkCount[update_key] += 1