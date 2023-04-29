import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "chrome"

def plot_budget_sankey(budget):
	labels, sources, targets, values = format_budget(budget)

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

def format_budget(budget):
	# define labels array for Sankey diagram from budget object
	# list the labels such that we traverse the budget tree depth-first
	# also define the source and target amounts
	labels=[]
	sources=[]
	targets=[]
	values=[]
	running_tally=0
	for (i,agency_budget_label) in enumerate(budget.sub_budgets.keys()):
		agency_ind=running_tally
		running_tally+=1
		agency_budget = budget.sub_budgets[agency_budget_label]

		labels.append(agency_budget_label)

		for (j,subagency_budget_label) in enumerate(agency_budget.sub_budgets.keys()):
			subagency_ind=running_tally
			running_tally+=1
			subagency_budget = agency_budget.sub_budgets[subagency_budget_label]

			# add label, nodes, and link
			labels.append(subagency_budget_label)
			sources.append(agency_ind)
			targets.append(subagency_ind)
			values.append(subagency_budget.total_obligations)

			continue
			for (k,obligation_label) in enumerate(subagency_budget.sub_obligations.keys()):
				obligation_ind=running_tally
				running_tally+=1
				obligation=subagency_budget.sub_obligations[obligation_label]

				# add label, nodes, and link
				labels.append(obligation_label)
				sources.append(subagency_ind)
				targets.append(obligation_ind)
				values.append(obligation)

	return labels, sources, targets, values