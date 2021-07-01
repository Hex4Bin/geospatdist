## Description

This tiny application can filter and calculate the distance of a path provided by a kml file.
It corrects the coordinates in the original kml file.

## Install the environment

<code>pip install -r requirements.txt</code>

## Call the procedure

app.kml_parser("task_2_sensor.kml")

## Logic

- I used lxml's etree.XMLParser to parse the kml file
- In two steps I converted the coordinates to list of lists
- Then put them into a Pandas dataframe
- Filtered the empty and irrelevant rows and converted them into float numbers
- Filtered out the duplicates
- Filtered out those coordinates which are too close to each other
- Used the Ramer–Douglas–Peucker algorithm to reduce the remaining coordinates
- Converted the dataframe back to text
- Modified the kml file coordinates attribute with the filtered data
- With the Harversine method I calculated the distance between the remaining coordinates
- Saved the kml file and returned the distance in KM

## Possible Improvements

I have never worked with Spatial Geodata before so my implementation is not correct.
With the usage of <code>Geopandas</code> and <code>Kalman filter</code> the accuracy can be improved.
We could validate the kml file in the beginning and we could write unit tests as well.
Transform into OOP
