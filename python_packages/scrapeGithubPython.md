---
title: "scrapeGithubPython"
author: Chris Heiser
---
### Overview
In this case a user has written a script to link a data resource, and the Python package written for that resource, to resources in GitHub.  The intention here is to survey ways in which the data resource is being used in analytic workflows.

We are looking for the statement "import <package_name>" in Python code found on Github. 



First, link your valid Github token to the script. This authorizes you to make API calls. You can generate a token using your [developer settings](https://developer.github.com/v3/guides/basics-of-authentication/) in GitHub.

```python
# Option 1: Paste your github token to make Github API calls
ghtoken = ""
# Option 2: If you have your github token stored in a file, read it in from the file.
with open("gh.token", "r") as f:
	reader = f.readlines()
	ghtoken = reader[0]
```



The "Py_packages_toScrape.csv" is a single column of python packages names. There isn't a Python equivalent to ROpenSci, so this list was manually created from popular scientific packages. 


```python
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
```



We put together the API request and send it out with the authorized token. We use information from the response to write a CSV file with the relevant results. Each line in the "scrapeGitResults.csv" file represents a single connection between two packages, and the URL to the file where the "import <package_name>" was found. 

```python
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
```


