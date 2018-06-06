import requests
import json
import csv 


def main():
	# Read all data from CSV source
	pkg_data = read_pkg_csv("python_annotations.csv")
	# Get all names from index 0 of each entry
	pkg_names = [pkg["package"] for pkg in pkg_data]
	# GET request the text of each package's setup.py - raw github link
	pkg_data = get_gh_file(pkg_data)
	# We have all the setup.py texts, now look for crossovers
	pkg_data = get_crossovers(pkg_names, pkg_data)
	# Write out the results as csv file
	write_csv(pkg_data)
	return


def write_csv(pkg_data):
	# The headers we want to write out
	_headers = ["package", "repo", "setup", "connections", "other", "notes"]
	# List to be written out
	_writeout = []
	# Reorder in a list so it's csv-write friendly
	for pkg in pkg_data:
		_tmp = []
		for header in _headers:
			try:
				_tmp.append(pkg[header])
			except KeyError:
				_tmp.append(" ")
		_writeout.append(_tmp)
	with open("gitPyResults.csv", "w") as csvfile:
		writer = csv.writer(csvfile, delimiter=",")
		writer.writerow(_headers)
		for row in _writeout:
			writer.writerow(row)
	return


def get_crossovers(pkg_names, pkg_data):
	for pkg in pkg_data:
		pkg["connections"] = []
		for pkg_name in pkg_names:
			if pkg_name.lower() in pkg["text"].lower() and pkg_name.lower() != pkg["package"]:
				pkg["connections"].append(pkg_name.lower())
		pkg["connections"] = ", ".join(pkg["connections"])
	return pkg_data


def read_pkg_csv(filename):
	out = []
	with open(filename) as csvfile:
		# Csv reader
	    reader = csv.DictReader(csvfile, delimiter=",")
	    for row in reader:
	    	out.append(row)
	return out

def get_gh_file(pkg_data):
	for pkg in pkg_data:
		# If the setup.py requirements are stored in a separate file, get that file instead
		if pkg["other"]:
			r = requests.get(pkg["other"])
		# Normal case: Get the setup.py file
		else:
			r = requests.get(pkg["setup"])
		pkg["text"] = r.text
	return pkg_data



main()
