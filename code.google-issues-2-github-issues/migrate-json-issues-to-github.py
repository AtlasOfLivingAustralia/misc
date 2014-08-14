import sys
import json
import unicodedata

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

def migrate_issue(issue):
    if not extract_project_labels(issue):
        return

    # TODO: make this lookup/mapping tables external JSON file
    lookup_table_project = {
        # "Alerts":         "https://api.github.com/repos/atlasoflivingaustralia/",
        # "ASBP":           "https://api.github.com/repos/atlasoflivingaustralia/",
        # "AUTH":           "https://api.github.com/repos/atlasoflivingaustralia/",
        # "AVH":            "https://api.github.com/repos/atlasoflivingaustralia/",
        # "BHL":            "https://api.github.com/repos/atlasoflivingaustralia/",
        # "BIE":            "https://api.github.com/repos/atlasoflivingaustralia/",
        "biocache":       "https://api.github.com/repos/atlasoflivingaustralia/test-issue-migration-biocache",
        "Biocache":       "https://api.github.com/repos/atlasoflivingaustralia/test-issue-migration-biocache",
        # "Browser-All":    "https://api.github.com/repos/atlasoflivingaustralia/",
        # "BVP":            "https://api.github.com/repos/atlasoflivingaustralia/",
        # "Collectory":     "https://api.github.com/repos/atlasoflivingaustralia/",
        # "Component-UI":   "https://api.github.com/repos/atlasoflivingaustralia/",
        # "Dashboard":      "https://api.github.com/repos/atlasoflivingaustralia/",
        # "f":              "https://api.github.com/repos/atlasoflivingaustralia/",
        "FieldCapture":   "https://api.github.com/repos/atlasoflivingaustralia/test-issue-migration-fieldcapture",
        # "Geonetwork":     "https://api.github.com/repos/atlasoflivingaustralia/",
        # "Hubs":           "https://api.github.com/repos/atlasoflivingaustralia/",
        # "ImageService":   "https://api.github.com/repos/atlasoflivingaustralia/",
        # "LayerServices":  "https://api.github.com/repos/atlasoflivingaustralia/",
        # "ListsTool":      "https://api.github.com/repos/atlasoflivingaustralia/",
        # "ListTool":       "https://api.github.com/repos/atlasoflivingaustralia/",
        # "NameMatching":   "https://api.github.com/repos/atlasoflivingaustralia/",
        # "names":          "https://api.github.com/repos/atlasoflivingaustralia/",
        # "OzAtlasAndroid": "https://api.github.com/repos/atlasoflivingaustralia/",
        # "Regions":        "https://api.github.com/repos/atlasoflivingaustralia/",
        # "Sandbox":        "https://api.github.com/repos/atlasoflivingaustralia/",
        # "Sighitngs":      "https://api.github.com/repos/atlasoflivingaustralia/",
        # "Sightings":      "https://api.github.com/repos/atlasoflivingaustralia/",
        "SpatialPortal":  "https://api.github.com/repos/atlasoflivingaustralia/test-issue-migration-spatial-portal"
        # "WEBAPI":         "https://api.github.com/repos/atlasoflivingaustralia/"
    }

    github_repo_url        = lookup_mapping(issue["project"], lookup_table_project)
    if len(github_repo_url) == 0:
        err = 'NO MIGRATION DESTINATION for {}'.format(issue["project"])
        print '<tr><td>{}</td><td>{}</td><td><a href="https://code.google.com/p/ala/issues/detail?id={}">{}</a></td></tr>'.format(issue["ID"], err, issue["ID"], issue["Summary"])
        return

    github_repo_issues_url = github_repo_url + "/issues"

    # CREATE ISSUE
    # example:
    #
    # curl --user    "mbohun"
    #      --request POST
    #      --data '{
    #                  "title":    "issue title here",
    #                  "body":     "issue body here",
    #                  "assignee": "pbrenton",
    #                  "labels": [
    #                      "Priority-High",
    #                      "enhancement"
    #                  ]
    #              }'
    #
    #       https://api.github.com/repos/atlasoflivingaustralia/fieldcapture/issues

    print '<!-- migrating issue id={}\t\tto: {} -->'.format(issue["ID"], github_repo_issues_url)

def migrate_json_issues(file_name):
    f = open(file_name[0], 'r')
    data = json.load(f)
    print 'len(data):{}'.format(len(data))

    # simple report in HTML format into stdout
    print '<html>'
    print '<body>'
    print '<table border="1">'
    print '<tr><th>issue id</th><th>error description</th><th>link to issue</th></tr>'

    for issue in data:
        migrate_issue(issue)

    print '</table>'
    print '</body>'
    print '</html>'

if __name__=="__main__":
        migrate_json_issues(sys.argv[1:])
