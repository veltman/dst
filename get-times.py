import requests
import json
from bs4 import BeautifulSoup

cities = open("cities.txt").read().split("\n")

for city in cities:

	place = city.split(",")[0].strip()
	st = city.split(",")[1].strip()

	payload = {
		"FFX": "1",
		"xxy": "2013",
		"type": "0",
		"st": st,
		"place": place,
		"ZZZ": "END"
	}

	headers = {
		"Referer": "http://aa.usno.navy.mil/data/docs/RS_OneYear.php"
	}

	url = "http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl"

	table = requests.post(url,data=payload, headers=headers)

	soup = BeautifulSoup(table.text)

	pre = soup.find("pre").text

	lines = pre.split("\n")[2:]

	location = lines[0].split("  ")[0]

	latlng = location.replace("Location: ","").strip().split(", ")

	lng = latlng[0].replace(" ",".").replace("W","-").replace("E","")
	lat = latlng[1].replace(" ",".").replace("S","-").replace("N","")

	lng = float(lng)
	lat = float(lat)

	tz = lines[2].strip().replace(" Standard "," ")

	lines = lines[8:39]

	times = []

	for m in range(12):
		times.append([])

	for line in lines:
		line  = line[4:]

		i = 0
		while i < 12:
			pair = line[i*11:(i*11)+9]
			
			if len(pair.strip()) > 0:
				pair = pair.split(" ")
				pair[0] = pair[0][:2]+":"+pair[0][2:]
				pair[1] = pair[1][:2]+":"+pair[1][2:]
				times[i].append(pair)

			i = i+1

	output = {
		"lat": lat,
		"lng": lng,
		"city": place,
		"state": st,
		"timezone": tz,
		"sun": []
	}

	for month in times:
		for day in month:
			output["sun"].append(day)

	open("cities/"+place.replace(" ","_")+".json","w").write(json.dumps(output,indent=2, separators=(',', ': ')))