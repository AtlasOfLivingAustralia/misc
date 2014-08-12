import sys
import csv
import json
import unicodedata
import requests
from lxml import html

#TODO: if element.attrib.has_key('href'): safer?

def handler_element_a(element, result):
    html_link = element.get('href')
    if html_link.find("/p/ala/issues") == 0:
        html_link = "https://code.google.com" + html_link

    result.append({ "a" : { "text" : element.text.encode('utf8'), "link": html_link}})

def handler_element_b(element, result):
    result.append({ "b" : { "text" : element.text.encode('utf8')}})

def handler_element_br(element, result):
    result.append({ "br" : {}})

def handler_element_i(element, result):
    result.append({ "i" : { "text" : element.text.encode('utf8')}})

def handler_element_pre(element, result):
    result.append({ "text" : element.text.encode('utf8')})

element_handler_table = {
    "a"        : handler_element_a,
    "b"        : handler_element_b,
    "br"       : handler_element_br,
    "i"        : handler_element_i,
    "pre"      : handler_element_pre
}

def updates_handler_element_b(element, result):
    key = element.text.encode('utf8')
    # strip the ":" from "Status:", "Cc:", "Owner:", "Labels:"
    result.append(key.replace(":", ""))

def updates_handler_element_br(element, result):
    # nothing to do, <br> is only a separator in updates
    return

# NOTE: this is required for scenarios like https://code.google.com/p/ala/issues/detail?id=95,
#       that has the old/previous Summary wrapped in <span>; see the "WAS:" handling in
#       get_issue_details() bellow.
def updates_handler_element_span(element, result):
    was = 'WAS:{}'.format(element.text.encode('utf8').strip())
    result.append(was)

updates_handler_table = {
    "b"        : updates_handler_element_b,
    "br"       : updates_handler_element_br,
    "span"     : updates_handler_element_span
}

def handle_element(element, result, handler_table):
    try:
        handler_table[element.tag](element, result)

    except KeyError:
        result.append({ "error" : { "text" : element.text.encode('utf8'), "error": element.tag}})

# NOTE: the extraction/assignment of project label (for migration) does NOT have to be here in
#       SCRAPING script, it should be (and it will be) moved in to the
#       MIGRATION script
def extract_project_labels(issue):
    text = unicodedata.normalize('NFKD', issue["AllLabels"]).encode('ascii', 'ignore')
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
    # NORMALIZE - remove synonyms like SpatialPortal Spatial-Portal, replacing it with one label: SpatialPortal
    # This applies to all Labels string: project names (synonyms, typos), priority (high, High, HIgh), etc.
    if "Spatial-Portal" in project:
        project.pop(project.index("Spatial-Portal"))
        if not "SpatialPortal" in project:
            project.append("SpatialPortal")

    if len(project) == 1:
        issue["project"] = project[0]
        return True

    # for issues that have 0 or multiple number of projects, print them out:
    if len(project) == 0:
        err = "NO PROJECT"
                
    if len(project) > 1:
        err = "MULTIPLE PROJECTS ({})".format(project);

    print '<tr><td>{}</td><td>{}</td><td><a href="https://code.google.com/p/ala/issues/detail?id={}">{}</a></td></tr>'.format(issue["ID"], err, issue["ID"], issue["Summary"])
    return False

def get_issue_details(issue):

    if not extract_project_labels(issue):
        return

    page = requests.get("https://code.google.com/p/ala/issues/detail?id=" + issue["ID"])
    tree = html.fromstring(page.text)

    # NOTE: find out why '//*[@id="meta-float"]/table/tbody/tr[3]/td/a[@class="userlink"]/text()' does not work
    #       ANSWER: looks like lxml XPath engine does NOT like/support tbody element and tbody has to be omitted
    cc = tree.xpath('//td[@id="issuemeta"]/div[@id="meta-float"]/table/tr[3]/td/a[@class="userlink"]/text()') #OR use @href?
    issue["cc"] = cc

    details = {}
    i = 0

    while True:
        comment_element = tree.xpath('//div[@id="hc{}"]'.format(str(i)))
        if len(comment_element) == 0: break

        result = {}

        # NOTE: the * is used because:
        #       hc0 has author in a div:  'div[class="author"]/a[@class="userlink"]', while
        #       hc1, hc2, etc. in a span: 'span[class="author"]/a[@class="userlink"]'
        author = comment_element[0].xpath('*[@class="author"]/a[@class="userlink"]/text()')
        result["author"] = author[0]

        date = comment_element[0].xpath('div/span[@class="date"]/@title')
        result["date"] = date[0]

        # the <pre> element of description/comments
        pre_full_text = comment_element[0].xpath('pre/text()')
        comment = []

        # if pre_full_text is a list containing exactly ONE string that means the <pre> contains only text,
        # and has no sub-elements/children (<a>, <b>, <i>, <br>, etc.), no further processing is required
        if len(pre_full_text) == 1:
            comment.append({ "text": pre_full_text[0]})

        else:
            # this <pre> contains sub-elements/children (<a>, <b>, <i>, <br>, etc.), we need to combine
            # the info in pre_full_text and the info from its sub-elements children
            comment_elements = []
            for di in comment_element[0].xpath('pre')[0].getiterator():
                handle_element(di, comment_elements, element_handler_table)

            element_index = 1 # NOTE: skip comment_elements[0] it is the same pre_full_text[0]
            for c in pre_full_text:
                comment.append({ "text": c})
                if element_index < len(comment_elements):
                        comment.append(comment_elements[element_index])
                        element_index = element_index + 1

        result["comment"] = comment

        updates_full_text = comment_element[0].xpath('div[@class="updates"]/div[@class="box-inner"]/text()')

        # unlike the <pre> element in description/comments the updates are optional, and this is to guard against NO UPDATES case
        if len(updates_full_text):
            updates_values = []
            for u in updates_full_text:
                stripped_u = u.strip()
                if len(stripped_u):
                    updates_values.append(stripped_u)

            children = comment_element[0].xpath('div[@class="updates"]/div[@class="box-inner"]')[0].getchildren()
            updates_keys = []
            for c in children:
                handle_element(c, updates_keys, updates_handler_table)

            # this is to handle the WAS: updates
            was_index = -1
            for uk in updates_keys:
                if uk.find("WAS:") == 0:
                    was_index = updates_keys.index(uk)
                    break;

            if was_index > 0: # the index has to be 1,2,3,etc.
                value_index = was_index - 1;
                # TODO: strip the "WAS:" from updates_keys.pop(was_index) before appending it to the value
                updates_values[value_index] = updates_values[value_index] + updates_keys.pop(was_index)

            updates = {}
            for k, v in zip(updates_keys, updates_values):
                #print '{}: updates["{}"]={}'.format(issue["ID"], k, v)
                updates[k] = v

            result["updates"] = updates

        # NOTE: lxml XPath does not like/support the tbody element, that is the reason why it is omitted
        attachments_raw = comment_element[0].xpath('div[@class="attachments"]/table/tr[1]/td[2]/a/@href')
        if len(attachments_raw):
            attachments = []
            for a in attachments_raw:
                url=""

                token_index = a.find("token=")
                if token_index > -1:
                    token_index_end = a.find("&", token_index)
                    if token_index_end > -1:
                        url = a[0:token_index] + a[token_index_end+1:]
                    else:
                        url = a[0:token_index-1]

                else:
                    url = a

                # fix URLs like: "../../ala/issues/attachmentText?id=750&aid=7500001000&name=explanatoryNotes.txt"
                if url.find("../../ala/issues") == 0:
                    url = "https://code.google.com/p/" + url[6:]

                # fix URLs like: "//ala.googlecode.com/issues/attachment?aid=7500001000&name=explanatoryNotes.txt"
                if url.find("//ala.googlecode.com/issues/attachment") == 0:
                    url = "https:" + url

                attachments.append(url)

            result["attachments"] = attachments

        details['hc{}'.format(str(i))] = result
        i += 1

    issue["details"] = details

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
