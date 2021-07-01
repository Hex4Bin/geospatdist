from lxml import etree
import os
import pandas as pd
import math
from rdp import rdp


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points 
    specified in decimal degrees
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def kml_parser(file: str) -> float:
    """
    Parse the kml file and filter out the invalid coordinates.
    """
    ns = {"kml": "http://www.opengis.net/kml/2.2"}

    kml_path = os.path.dirname(__file__) + "/" + file

    parser = etree.XMLParser(remove_blank_text=True, strip_cdata=True)
    tree = etree.parse(kml_path, parser)

    old_coordinates = tree.xpath(
        "//kml:coordinates", namespaces=ns)[0]

    # convert the coordinates to list
    new_coordinates = list(dict.fromkeys(old_coordinates.text.split(" ")))

    # convert the string list into a list of lists
    new_coordinates = [coordinates.split(",")
                       for coordinates in new_coordinates]

    # put the data into a dataframe
    df = pd.DataFrame(new_coordinates, columns=("long", "lat", "alt"))
    df = df[~df.long.isin(["", "\n"])]
    df = df.astype(float)

    # delete the duplicate coordinates
    df.drop_duplicates(subset=None, keep="first", inplace=True)

    # logic to clean the coordinates
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            if abs(df.iloc[i]["long"] - df.iloc[j]["long"]) <= 0.001:
                df.iloc[j]["long"] = df.iloc[i]["long"]
                continue
            if abs(df.iloc[i]["lat"] - df.iloc[j]["lat"]) <= 0.001:
                df.iloc[j]["lat"] = df.iloc[i]["lat"]
                continue

    # Ramer–Douglas–Peucker algorithm to reduce the remaining coordinates
    df2 = pd.DataFrame(rdp(df, epsilon=0.0005), columns=("long", "lat", "alt"))

    text = ""
    dist = 0

    # create a string from the cleaned dataframe to be able to insert back to the kml file
    for i in range(len(df2)):
        text += f'{df2.iloc[i]["long"]},{df2.iloc[i]["lat"]},0 '
        if i != 0:
            dist += haversine(df2.iloc[i-1]["long"], df2.iloc[i-1]
                              ["lat"], df2.iloc[i]["long"], df2.iloc[i]["lat"])

    schema_element = tree.xpath("//kml:coordinates", namespaces=ns)[0]
    schema_element.text = text

    # modify the coordinates in the kml file
    with open(kml_path, 'wb') as f:
        f.write(etree.tostring(tree))

    return dist
