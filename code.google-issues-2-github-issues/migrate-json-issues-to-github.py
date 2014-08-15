import sys
import json
import unicodedata
import requests
import cStringIO
import time

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

def lookup_mapping(string, table):
    try:
        return table[string]

    except KeyError:
        return ""

# NOTE: these handlers are to convert the HTML-like elements/formatting from ISSUE/details/comment to github markdown
def handler_element_a(element, out_buffer):
    out_buffer.write("[")
    out_buffer.write(element["a"]["text"].encode('utf8'))
    out_buffer.write("]")
    out_buffer.write("(")
    out_buffer.write(element["a"]["link"])
    out_buffer.write(")")

def handler_element_b(element, out_buffer):
    out_buffer.write("**")
    out_buffer.write(element["i"]["text"].encode('utf8'))
    out_buffer.write("**")

def handler_element_br(element, out_buffer):
    out_buffer.write("\n")

def handler_element_i(element, out_buffer):
    out_buffer.write("*")
    out_buffer.write(element["i"]["text"].encode('utf8'))
    out_buffer.write("*")

def handler_element_text(element, out_buffer):
    out_buffer.write(element["text"].encode('utf8'))

element_handler_table = {
    "a"         : handler_element_a,
    "b"         : handler_element_b,
    "br"        : handler_element_br,
    "i"         : handler_element_i,
    "text"      : handler_element_text
}

def handle_element(element, result):
    key = element.keys()[0] #there is EXACTLY ONE key
    try:
        element_handler_table[key](element, result)

    except KeyError:
        print 'ERROR handle_element() does NOT know: {}'.format(key)

def create_issue_body(arr_of_dict, meta_info=""):
    out_buffer = cStringIO.StringIO()

    if len(meta_info):
        out_buffer.write(meta_info)

    for a in arr_of_dict:
        handle_element(a, out_buffer)

    body = out_buffer.getvalue()
    out_buffer.close()
    return body

def migrate_issue(issue, lookup_table, github_password):
    if not extract_project_labels(issue):
        return

    github_repo_url        = lookup_mapping(issue["project"], lookup_table["project"])
    if len(github_repo_url) == 0:
        err = 'NO MIGRATION DESTINATION for {}'.format(issue["project"])
        print '<tr><td>{}</td><td>{}</td><td><a href="https://code.google.com/p/ala/issues/detail?id={}">{}</a></td></tr>'.format(issue["ID"], err, issue["ID"], issue["Summary"].encode('utf8'))
        return

    github_repo_create_issue_url = github_repo_url + "/issues"

    meta_info = '\n*migrated from:* https://code.google.com/p/ala/issues/detail?id={}\n*date:* {}\n*author:* {}\n ---\n'.format(issue["ID"], issue["details"]["hc0"]["date"], issue["details"]["hc0"]["author"])
    body = create_issue_body(issue["details"]["hc0"]["comment"], meta_info)
    data = json.dumps({ 'title': issue["Summary"], 'body': body }) # TODO: assignee, labels

    github_token = lookup_mapping(issue["details"]["hc0"]["author"], lookup_table["author"])
    if len(github_token) == 0:
        res = requests.post(github_repo_create_issue_url, data, auth=('mbohun', github_password))

    else:
        http_header = {'Authorization': 'token %s' % github_token}
        res = requests.post(github_repo_create_issue_url, data, headers=http_header)

    # TODO: we need to parse the return codes, id possible errors AND to extract important
    #       information from the github API return JSON messages, for example the newly
    #       created github issue ID
    if res.status_code != 201: # TODO: make/use proper constant for HTTP_ACCEPTED
        # TODO: log/report status_code err
        return False

    created_issue_id = res.json()["number"]
    github_repo_commenton_issue_url = github_repo_create_issue_url + "/" + str(created_issue_id) + "/comments"

    number_of_comments = len(issue["details"])  # hc0 is the issue description, hc1, hc2 ... are the comment-s on the issue

    for i in range(1, number_of_comments):
        hc = 'hc{}'.format(i)
        meta_info = '\n*date:* {}\n*author:* {}\n ---\n'.format(issue["details"][hc]["date"], issue["details"][hc]["author"])
        body = create_issue_body(issue["details"][hc]["comment"], meta_info)
        data = json.dumps({ 'body': body })

        github_token = lookup_mapping(issue["details"][hc]["author"], lookup_table["author"])
        if len(github_token) == 0:
            res = requests.post(github_repo_commenton_issue_url, data, auth=('mbohun', github_password))

        else:
            http_header = {'Authorization': 'token %s' % github_token}
            res = requests.post(github_repo_commenton_issue_url, data, headers=http_header)

    print '<!-- migrating issue id={}\t\tto: {} -->'.format(issue["ID"], github_repo_create_issue_url)
    return True

def migrate_json_issues(args):
    f = open(args[0], 'r')
    data = json.load(f)
    print 'len(data):{}'.format(len(data))

    lookup_table_file = open(args[1], 'r')
    lookup_table = json.load(lookup_table_file);

    # simple report in HTML format into stdout
    print '<html>'
    print '<body>'
    print '<table border="1">'
    print '<tr><th>issue id</th><th>error description</th><th>link to issue</th></tr>'

    counter = 0
    for issue in data:
        if migrate_issue(issue, lookup_table, args[2]): # args[2] github password is optional - for example if github token-s are used
            counter += 1
            time.sleep(20) # careful we are limited to 60 request per hour, this should allow for 120 fieldcapture issues test migration

    print '</table>'
    print '</body>'
    print '</html>'
    print '<!-- MIGRATED: {} -->'.format(counter)

if __name__=="__main__":
        migrate_json_issues(sys.argv[1:])
