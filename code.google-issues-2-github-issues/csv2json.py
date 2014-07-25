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
    # try-catch for unknown element.tag
    element_handler_table[element.tag](element, result)

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

    # issue description, id="hc0"
    details_xpath_element = tree.xpath('//div[@class="cursor_off vt issuedescription"]/pre')
    details = []

    details_pre_full_text = tree.xpath('//div[@class="cursor_off vt issuedescription"]/pre/text()')
    details.append({ "pre-full" : str(details_pre_full_text)})

    for di in details_xpath_element[0].getiterator():
        handle_element(di, details)

    # issue comments, id="hc1", "hc2", "hc3" and so on
    comment_xpath_elements = tree.xpath('//div[@class="cursor_off vt issuecomment"]')
    comments = []

    for c in comment_xpath_elements:
        comments.append(c.xpath('@id'))

    issue["project"] = project[0]
    issue["details"] = details
    issue["comments"] = comments

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
