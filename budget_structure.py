class Budget:
	"""
	A place to structure the hierarchical obligations of a the US budget.
	"""
	def __init__(self):
		self.total_obligations=0 # total money in this budget
		self.sub_obligations={}  # division of money in each sub budget
		self.sub_budgets={} # sub budgets

	def add_obligation(self, name, obligation):
		"""
		Add an obligation to the budget. Should not contain any substructures

		Arguments
		---------
		:param name: str
			Name of the obligation, e.g. "Pacific Northwest Field Office"
		:param obligation: float
			Dollar amount of obligation, e.g. 100 is $100
		"""
		self.total_obligations+=obligation
		self.sub_obligations[name]=obligation

	def add_budget(self, name, sub_budget):
		"""
		Add a sub budget to this budget, allowing for hierarchical storage of budget data.

		Arguments
		---------
		:param name: str
			Name of the obligation, e.g. "Pacific Northwest Field Office"
		:param sub_budget: Budget
			Sub-budget, of class Budget
		"""
		self.sub_budgets[name]=sub_budget
		self.total_obligations+=sub_budget.total_obligations