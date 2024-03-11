# GeoSpy API Mapping forked from https://github.com/devbret/geospy-api-mapping
Query the [GeoSpy API](https://dev.geospy.ai/docs/routes#overview) for any number of images, and then visualize that JSON data on a world map.

## Basic Usage
After cloning the repo, open the app.py script in a text editor. Therein enter your API_TOKEN and IMAGE_FILES strings. Once your details are entered, open a terminal and run *python3 app.py*. This wil prompt you to select your images before querying the Geospy API and creating a folium map to view them in

Next, open the map.html file in any browser. This will feature a world map, you will be able to click on and tnteract with the markers as well as zoom and scroll as you need

## Important Points To Remember
Geospy is not 100% accurate so results may not match what you expect, due to me moving to folium i have not fully finished marker
color schemes and other little tweaks like that so bare with me.

also im a shit programmer so take that into account as well
