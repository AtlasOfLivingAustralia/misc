import sys
import csv
import json
import unicodedata
import requests
from lxml import html

#TODO: if element.attrib.has_key('href'): safer?

def handler_element_a(element, result):
    result.append({ "a" : { "text" : element.text.encode('utf8'), "link": element.get('href')}})

def handler_element_b(element, result):
    result.append({ "b" : { "text" : element.text.encode('utf8')}})

def handler_element_i(element, result):
    result.append({ "i" : { "text" : element.text.encode('utf8')}})

def handler_element_pre(element, result):
    result.append({ "pre" : { "text" : element.text.encode('utf8')}})

element_handler_table = {
    "a"        : handler_element_a,
    "b"        : handler_element_b,
    "i"        : handler_element_i,
    "pre"      : handler_element_pre
}

def handle_element(element, result):
    try:
        element_handler_table[element.tag](element, result)

    except KeyError:
        result.append({ "error" : { "text" : element.text.encode('utf8'), "error": element.tag}})

def extract_project_labels(str):
    text = unicodedata.normalize('NFKD', str).encode('ascii', 'ignore')
    labels = text.strip().split(",")

    project = []

    # remove empty and non project label-s like Type-, Priority-
    for label_text in labels:
        label = label_text.strip()
        if len(label) == 0:
            continue

        if label.find("Type") > -1:
            continue

        if label.find("Priority") > -1:
            continue

        if label.find("Milestone") > -1:
            continue

        project.append(label)

    # TODO: do it properly/cleanly
    # remove synonyms like SpatialPortal Spatial-Portal, replacing it with one label: SpatialPortal
    if "Spatial-Portal" in project:
        project.pop(project.index("Spatial-Portal"))
        if not "SpatialPortal" in project:
            project.append("SpatialPortal")

    return project

def get_issue_details(issue):

    project = extract_project_labels(issue["AllLabels"]);

    # for issues that have 0 or multiple number of projects, print them out:
    if len(project) != 1:
        #print 'id: {}, project_label({}): {}'.format(issue["ID"], len(project), project)
        if len(project) == 0:
            err = "NO PROJECT"
                
        if len(project) > 1:
            err = "MULTIPLE PROJECTS ({})".format(project);

        print '<tr><td>{}</td><td>{}</td><td><a href="https://code.google.com/p/ala/issues/detail?id={}">{}</a></td></tr>'.format(issue["ID"], err, issue["ID"], issue["Summary"])

        return

    page = requests.get("https://code.google.com/p/ala/issues/detail?id=" + issue["ID"])
    tree = html.fromstring(page.text)

    details = {}
    i = 0

    while True:
        comment_element = tree.xpath('//div[@id="hc{}"]'.format(str(i)))
        if len(comment_element) == 0: break

        result = {}

        attachments = comment_element[0].xpath('div[@class="attachments"]')
        result["has-attachments"] = len(attachments) > 0

        pre_full_text = comment_element[0].xpath('pre/text()')
        result["pre-full"] = str(pre_full_text)

        r = []
        for di in comment_element[0].xpath('pre')[0].getiterator():
            handle_element(di, r)

        result["pre"] = r

        details['hc{}'.format(str(i))] = result
        i += 1

    issue["project"] = project[0]
    issue["details"] = details

    # TODO: find out why '//*[@id="meta-float"]/table/tbody/tr[3]/td/a[@class="userlink"]/text()' does not work
    cc = tree.xpath('//td/a[@class="userlink"]/text()') #OR: tree.xpath('//td/a[@class="userlink"]/@href')
    issue["cc"] = cc

def create_json(file_name, column_names):
    csv_file = open(file_name[0], 'r')

    csv_reader = csv.DictReader(csv_file, column_names) 
    out = json.dumps( [row for row in csv_reader] )

    data = json.loads(out)
    #print "number of issues found: %d" % len(data)

    # simple report in HTML format into stdout
    print '<html>'
    print '<body>'
    print '<table border="1">'
    print '<tr><th>issue id</th><th>error description</th><th>link to issue</th></tr>'

    for issue in data:
        get_issue_details(issue)

    print '</table>'
    print '</body>'
    print '</html>'

    out = json.dumps(data, sort_keys=True)

    json_file = open(file_name[0] + ".json", 'w')
    json_file.write(out);

if __name__=="__main__":
        create_json(sys.argv[1:], ["ID","Type","Status","Priority","Owner","Summary","AllLabels","Modified","ModifiedTimestamp"])
