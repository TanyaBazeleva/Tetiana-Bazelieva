import xml.etree.ElementTree as ET
import os
def load_xml(filename):
    path = os.path.join("data", filename)
    tree = ET.parse(path)
    return tree.getroot()
def get_works_by_site(site_id):
    acts = load_xml("acts.xml")
    items = load_xml("items.xml")
    works = load_xml("works.xml")
    act_ids = [a.find("Id").text for a in acts if a.find("S_id").text == site_id]
    work_ids = [i.find("W_id").text for i in items if i.find("A_id").text in act_ids]
    result = []
    for w in works:
        wid = w.find("Id").text
        name = w.find("Name").text
        if wid in work_ids:
            result.append(f"{wid} – {name}")
    return result
