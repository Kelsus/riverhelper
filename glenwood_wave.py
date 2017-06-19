import urllib.request
import re


def getGlenwoodWaveFlow():
	river_page = urllib.request.urlopen('https://waterdata.usgs.gov/co/nwis/uv?site_no=09085100')
	river_regex = r"(Most recent instantaneous value: )(\w*)"
	search_results = re.search(river_regex, str(river_page.read()))

	return search_results.group(2)


print(getGlenwoodWaveFlow())
