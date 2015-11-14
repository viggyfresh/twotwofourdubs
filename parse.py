import numpy as np
import xml.etree.ElementTree as ET

def parse_links(link_filename, out_filename):
    tree = ET.parse(link_filename)
    root = tree.getroot()
    with open(out_filename, "wb") as outfile:
        for child in root:
            attrs = child.attrib
            outfile.write("%s;%s\n" % (attrs["PostId"], attrs["RelatedPostId"]))

parse_links("data/small/PostLinks.xml", "links.csv")
