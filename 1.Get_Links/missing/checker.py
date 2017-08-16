"""
checks to make sure the potential_cities are read
into either city_links or failures

more robust checks can be made and get_city_links.py
can be developed to adjust the file it reads from based
 on the content of missing.csv
"""

missing = open('missing.csv', 'w')
for line in open('../all_links/potential_cities.csv'):
	# pretty inefficient, but the file sizes here are not big enough to
	# cause a problem
	if line.strip() not in open('../processed_links/failures.csv').read() \
	and line.strip() not in open('../processed_links/city_links.csv').read():
		print line.strip()
		missing.write(line)

missing.close()