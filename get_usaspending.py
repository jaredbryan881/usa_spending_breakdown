import numpy as np
import pandas as pd

import requests

from budget_structure import Budget
from budget_sankey import plot_budget_sankey

def main():
	agencies_of_interest=["Department of Energy", 
						  "Department of the Interior", 
						  "Department of Defense", 
						  "Department of Homeland Security",
						  "Department of Commerce",
						  "National Aeronautics and Space Administration", 
						  "National Science Foundation"]
	agencies_of_interest=["Department of the Interior"]

	# get list of all toptier agencies
	toptier_agencies=get_agencies()
	# filter out all but the agencies of interest
	toptier_agencies=toptier_agencies["agencies"] # no subagencies
	toptier_agencies=toptier_agencies["cfo_agencies"] # don't want "other agencies"
	toptier_agencies=[tta for tta in toptier_agencies if tta["name"] in agencies_of_interest]

	total_budget=Budget()
	for agency in toptier_agencies:
		# retrieve all subagencies, e.g. subagency=USFWS for agency=DOI
		subagencies = get_subagencies(agency["toptier_code"], fiscal_year=2022, limit=100, agency_type='awarding')

		agency_budget=Budget()
		for (i,subagency) in enumerate(subagencies.name):

			subagency_budget=Budget()
			for (j,child) in enumerate(subagencies.children[i]):
				subagency_budget.add_obligation(child["name"], child["total_obligations"])

			agency_budget.add_budget(subagency, subagency_budget)

		total_budget.add_budget(agency["name"], agency_budget)

	plot_budget_sankey(total_budget, plot_obligations=False)

def get_agencies():
	"""
	Get a list of toptier agencies.

	Returns
	-------
	:return data: Dict
		Toptier agencies with their name, toptier agency id, and toptier code
	"""
	url = "https://api.usaspending.gov"
	endpoint = "/api/v2/bulk_download/list_agencies"
	payload = {"type": "award_agencies"}

	response = requests.post(url+endpoint, json=payload)
	data = response.json()

	return data

def get_subagencies(toptier_code, fiscal_year=None, award_type_codes=None, agency_type='awarding', order='desc', sort='total_obligations', page=1, limit=10):
	"""
	Get a list of subagencies for a given toptier agency.

	Arguments
	---------
	:param toptier_code: str
		Agencies have a numeric code, and this is it.
	:param fiscal_year: int
		Year to query. Must be greater than 2008.
	:param award_type_codes: ??
	:param agency_type: str
		'awarding' or 'funding'
	:param order: str
		Sorting direction. 'asc' or 'desc'
	:param sort: str
		Criterion to sort by. 'total_obligations' for dollar value
	:param page: int
		Which page of results to query.
	:param limit: int
		Maximum number of results to query.

	Returns
	-------
	:return df: DataFrame
		Subagencies resulting from the query.
	"""
	url = "https://api.usaspending.gov"
	endpoint = "/api/v2/agency/{}/sub_agency".format(toptier_code)
	
	payload = {"toptier_code": toptier_code,
			   "agency_type": agency_type,
			   "order": order,
			   "sort": sort,
			   "page": page,
			   "limit": limit}
	if fiscal_year is not None:
		payload["fiscal_year"]=fiscal_year
	if award_type_codes is not None:
		payload["award_type_codes"]=award_type_codes

	response = requests.get(url+endpoint, params=payload)
	data = response.json()

	df = pd.DataFrame(data["results"])

	return df

if __name__=="__main__":
	main()