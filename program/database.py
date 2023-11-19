class Database:
	def __init__(self):
		self._current_score = None

	@property
	def current_score(self):
		if self._current_score is None:
			return 0
		else:
			return self._current_score
	
	@current_score.setter
	def current_score(self,value):
		self._current_score = value

database = Database()