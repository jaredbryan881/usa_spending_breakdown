class Budget:
	def __init__(self):
		self.total_obligations=0 # total money in this budget
		self.sub_obligations={}  # division of money in each sub budget
		self.sub_budgets={} # sub budgets

	def add_obligation(self, name, obligation):
		self.total_obligations+=obligation
		self.sub_obligations[name]=obligation

	def add_budget(self, name, sub_budget):
		self.sub_budgets[name]=sub_budget
		self.total_obligations+=sub_budget.total_obligations