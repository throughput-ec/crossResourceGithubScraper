import requests
import json
import csv 
import time

# Need github token to make queries
ghtoken = ""
with open("gh.token", "r") as f:
	reader = f.readlines()
	ghtoken = reader[0]

def main():
	# Read packages from CSV file
	packList = read_pkg_csv("Py_packages_toScrape.csv")
	# Get all names from index 0 of each entry
	pkg_names = [pkg for pkg in packList]
	# GET request the text of each package's setup.py - raw github link
	results = send_query(packList)
	# Write out the results as csv file
	write_csv(results)
	return

def read_pkg_csv(filename):
	packList = []
	with open(filename) as csvfile:
		# Csv reader
	    reader = csv.reader(csvfile, delimiter=",")
	    for row in reader:
	    	package = row[0]
	    	if package != "package":
	    		packList.append(package)
	return packList


def write_csv(results):
	# The headers we want to write out
	_headers = ["package", "crossover_package", "crossover_file"]
	# List to be written out
	_writeout = []
	# Reorder in a list so it's csv-write friendly
	for line in results:
		_tmp = []
		for header in _headers:
			try:
				_tmp.append(line[header])
			except KeyError:
				_tmp.append(" ")
		_writeout.append(_tmp)
	with open("scrapeGitResults.csv", "w") as csvfile:
		writer = csv.writer(csvfile, delimiter=",")
		writer.writerow(_headers)
		for row in _writeout:
			writer.writerow(row)
	return


def send_query(packList):
	results = []

	for pkg in packList:
		print("Querying Github: {}".format(pkg))
		try:

			r = requests.get('https://api.github.com/search/code?q="import {}"+in:file+language:"python"+extension:"py"'.format(pkg), 
				headers={"Authorization":"token 73ebf3ec3fa330cabbe6b1bc6facc2a115ee5e68", "Accept": "application/vnd.github.v3+json"})

			if r.status_code == 200:
				try:
					r_text = json.loads(r.text)
					for result in r_text["items"]:
						try:
							results.append({"package": pkg, "crossover_file": result["html_url"], "crossover_package": result["repository"]["name"]})
						except KeyError:
							print("Error parsing a result for: {}".format(pkg))
				except Exception as e:
					print("Missing data from Github response object for package: {}".format(pkg))
			else:
				print("Received error from Github API: Status Code: {}".format(r.status_code))

			# Don't query github too fast. Take a break
			time.sleep(10)
		except Exception as e:
			print("Unable to make Github request. Connection issues.")


	return results


main()
