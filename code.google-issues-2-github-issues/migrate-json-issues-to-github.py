import sys
import json

def migrate_issue(issue):
    print 'migrating issue id={}'.format(issue["ID"])

def migrate_json_issues(file_name):
    f = open(file_name[0], 'r')
    data = json.load(f)
    print 'len(data):{}'.format(len(data))

    for issue in data:
        migrate_issue(issue)

if __name__=="__main__":
        migrate_json_issues(sys.argv[1:])
