import requests
import json
import csv 
import time

# Insert your github token to make Github API calls
ghtoken = ""
# If you have your github token stored in a file, read it in from the file.
with open("gh.token", "r") as f:
	reader = f.readlines()
	ghtoken = reader[0]

def main(ghtoken):
	"""
	Main function for the scraper. Read package list, query Github, write results.

	"""
	# Read packages list from CSV file
	packList = read_pkg_csv("Py_packages_toScrape.csv")
	# Query Github with the package list
	results = send_query(packList, ghtoken)
	# Write out the results to a csv file
	write_csv(results)
	return


def read_pkg_csv(filename):
	"""
	Open the CSV file and read in the package list. 

	"""
	packList = []
	with open(filename) as csvfile:
		# Csv reader
	    reader = csv.reader(csvfile, delimiter=",")
	    for row in reader:
	    	package = row[0]
	    	# Ignore the header row
	    	if package != "package":
	    		# Append individual package name
	    		packList.append(package)

	return packList


def write_csv(results):
	"""
	Write out the results to a CSV file

	"""

	# The headers we want to write out
	_headers = ["package", "crossover_package", "crossover_file"]

	# List to be written out
	_writeout = []

	# Organize results into a csv-friendly writeable list
	for line in results:
		_tmp = []
		for header in _headers:
			try:
				_tmp.append(line[header])
			except KeyError:
				_tmp.append(" ")
		_writeout.append(_tmp)

	# Write new (or overwrite) csv file with organized results
	with open("scrapeGitResults.csv", "w") as csvfile:
		writer = csv.writer(csvfile, delimiter=",")
		writer.writerow(_headers)
		for row in _writeout:
			writer.writerow(row)
	return


def send_query(packList, ghtoken):

	"""
	Make a github query for each package in the package list.

	"""

	results = []

	# Loop for each package
	for pkg in packList:
		print("Querying Github: {}".format(pkg))
		try:
			# Make the github request. Look for 'import <package_name>' in code in python files
			r = requests.get('https://api.github.com/search/code?q="import {}"+in:file+language:"python"+extension:"py"'.format(pkg), 
				headers={"Authorization":"token {}".format(ghtoken), "Accept": "application/vnd.github.v3+json"})

			# Did the query come back successful?
			if r.status_code == 200:
				try:
					# Load the response json as a Python dictionary
					r_text = json.loads(r.text)
					# Loop through each query result
					for result in r_text["items"]:
						try:
							# We don't need all the data from the results. Save the few pieces of info that we're interested in.
							results.append({"package": pkg, "crossover_file": result["html_url"], "crossover_package": result["repository"]["name"]})
						except KeyError:
							# This result was missing a piece of data that we need.
							print("Error parsing a result for: {}".format(pkg))
				except Exception as e:
					# There was a problem trying to parse the json response, or 'items' key is not in the response results
					print("Missing data from Github response object for package: {}".format(pkg))
			else:
				# There was a bad HTTP response from Github. If the error is 403, then we likely hit the rate limiter and need to increase the sleep time between requests.
				print("Received error from Github API: Status Code: {}".format(r.status_code))

			# Don't query github too fast or you'll hit the limiter and get a bad response. Give it some time. 
			time.sleep(10)

		except Exception as e:
			# Did your interenet connection go out? Something is wrong with sending out the request
			print("Unable to make Github request. Connection issues.")

	return results


main(ghtoken)


# def write_multi_connection_csv():
# 	"""
# 	Open the CSV file and read in the package list. 

# 	"""
# 	packList = []
# 	multi = {}
# 	output = []
# 	_headers = ["package", "connections"]

# 	with open("scrapeGitResults.csv") as csvfile:
# 		# Csv reader
# 	    reader = csv.DictReader(csvfile, delimiter=",")
# 	    for row in reader:
#     		# Append individual package name
#     		packList.append(row)

# 	for entry in packList:
# 		if entry["package"] not in multi:
# 			multi[entry["package"]] = []
# 		if entry["crossover_package"] not in multi[entry["package"]]:
# 			multi[entry["package"]].append(entry["crossover_package"])

# 	for k,v in multi.items():
# 		output.append([k, v])

# 	# Write new (or overwrite) csv file with organized results
# 	with open("scrapeGitResultsMulti.csv", "w") as csvfile:
# 		writer = csv.writer(csvfile, delimiter=",")
# 		writer.writerow(_headers)
# 		for row in output:
# 			writer.writerow(row)

# 	return packList

