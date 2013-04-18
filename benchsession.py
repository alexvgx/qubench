
class BenchSession(object):
    
	def __init__(self):
		self.currentState = 0 # 0 - stopped, 1 - run


	def getState(self):
		return self.currentState

	
	def setState(self, state):
		self.currentState = state