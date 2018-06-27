# Throughput Cross-Resource Workflow Scraper

One component of the broader [Throughput](http://throughput-ec.github.io) project is the ability to link to resources on the web that indicate ways in which individuals have linked records, data resources or objects to provide scientific insight.

To help establish a baseline of data integration this project uses Python to search for code on GitHub (with other implementations to come) that invoke commands such as `import packageName` (Python) or `library(packageName)` (R), and adds these to a graph database [described elsewhere](http://throughput-ec.github.io/throughputdb/populate/case_study.html) using the W3C annotation model.

## Contributions

*   Chris Heiser - University of Northern Arizona
*   Nick McKay - University of Northern Arizona
*   Simon Goring - University of Wisconsin -- Madison

We welcome contributions from all individuals, but expect contributors to follow the [Code of Conduct](http://contributor-covenant.org/version/1/3/0/) for this repository.

## Current Packages of Interest

The list of packages to be searched includes packages from the [ROpenSci registry](https://raw.githubusercontent.com/ropensci/roregistry/master/registry.json), as well as Python packages, including [lipd](https://github.com/nickmckay/LiPD-utilities) and packages in the [SciTools repository](https://github.com/SciTools).

# Support

This work is funded through the National Science Foundation's [EarthCube Program](http://earthcube.org) through awards [1740699](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1740699) and [1740667](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1740667).
