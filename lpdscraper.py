#!/usr/bin/python3

import httplib2
from geopy.geocoders import Nominatim
import re

# https://github.com/jcgregorio/httplib2/blob/master/README.md
URL="http://linux-presentation-day.de/orte/index.html"
h = httplib2.Http(".cache")
(resp_headers, content) = h.request(URL, "GET")
# https://github.com/jcgregorio/httplib2/wiki/Examples-Python3
str_content = content.decode('utf-8')

htmllist = str_content.split('\n')
cities = [i for i in htmllist if i.startswith("<li><p>")]

cityurl = []
for i in cities:
  # regexexample: <li><p><a href="http://www.eifeltux.de/index.php/l-p-d">Eifel</a></p></li>
  p = re.compile('<li><p><a href="(.*?)">(.*?)<')
  if p.match(i):
      url = p.match(i).group(1)
      city = p.match(i).group(2)
      cityurl.append([city, url])

geolocator = Nominatim()

with open ("umap.lpd.csv", "w") as csvfile:
    csvfile.write("name;lat;lon;description\n")

with open ("umap.lpd.csv", "a") as csvfile:
    for i in cityurl: 
        if not i[0] == "Voralpen / Weis" or i[0] == "Hanau" or i[0].strip == "":
            try:
                csvfile.write(i[0] + "; ")
                location = geolocator.geocode(i[0] + ", Germany")
                csvfile.write(str(location.latitude) + "; " +  str(location.longitude) + "; [[" + i[1] + "]]\n")
            except:
                print(i)
