import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "chrome"

def plot_budget_sankey(budget, plot_obligations=False):
	labels, sources, targets, values = format_budget(budget, plot_obligations=plot_obligations)

	fig = go.Figure(data=[go.Sankey(
					node = dict(pad = 15,
								thickness = 20,
								line = dict(color = "black", width = 0.5),
								label = labels,
								color = "steelblue"),
					link = dict(source=sources,
								target=targets,
								value=values))])

	fig.show()

def format_budget(budget, plot_obligations):
	"""
	Format the contents of a budget object in such a way that plotly sankey can easily plot it.

	Aguments
	--------
	:param budget: Budget
		Hierarchical budget object, containing agencies, subagencies, and obligations
	"""
	# define labels array for Sankey diagram from budget object
	# list the labels such that we traverse the budget tree depth-first
	# also define the source and target amounts
	labels=[]
	sources=[]
	targets=[]
	values=[]

	running_tally=0 # keep track of how many different source-target pairs there are
	for (i,agency_budget_label) in enumerate(budget.sub_budgets.keys()):
		# define location for agency, e.g. DOI
		agency_ind=running_tally
		running_tally+=1
		agency_budget = budget.sub_budgets[agency_budget_label]

		labels.append(agency_budget_label)

		for (j,subagency_budget_label) in enumerate(agency_budget.sub_budgets.keys()):
			# define location for subagency, e.g. "USGS"
			subagency_ind=running_tally
			running_tally+=1
			subagency_budget = agency_budget.sub_budgets[subagency_budget_label]

			# add label, nodes, and link
			labels.append(subagency_budget_label)
			sources.append(agency_ind)
			targets.append(subagency_ind)
			values.append(subagency_budget.total_obligations)

			# plot each obligation or not? Can be a lot/can crash page
			if not plot_obligations:
				continue
			for (k,obligation_label) in enumerate(subagency_budget.sub_obligations.keys()):
				# define location for obligation, e.g. "Hawaii Volcano Observatory"
				obligation_ind=running_tally
				running_tally+=1
				obligation=subagency_budget.sub_obligations[obligation_label]

				# add label, nodes, and link
				labels.append(obligation_label)
				sources.append(subagency_ind)
				targets.append(obligation_ind)
				values.append(obligation)

	return labels, sources, targets, values