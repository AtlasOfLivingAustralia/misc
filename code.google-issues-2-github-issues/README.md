###OBJECTIVE
Migrate [Atlas of Living Australia](http://www.ala.org.au) issues (issue tracker) from [https://code.google.com/p/ala/issues/list](https://code.google.com/p/ala/issues/list) to [https://github.com/AtlasOfLivingAustralia](https://github.com/AtlasOfLivingAustralia)

###PROBLEM
Google did disable the API for google code issues one year ago, so we can't simply use their API to get the issues in JSON format - we will have to roll our own, and most likely 'scrape' the information we want to migrate from the google code issues HTML pages.

###SOLUTION
#####Download your google issues (for example: [https://code.google.com/p/ala/issues](https://code.google.com/p/ala/issues)) in CSV format:
```BASH
# easy way to download "all" issues as one CSV file (we have 321 issues in total,
# the following will attempt to download up to 500 into one .csv file)
wget -O `date "+%Y-%m-%d"`-ala-google-code-issues-raw.csv https://code.google.com/p/ala/issues/csv?num=500

# or using curl:
curl -s https://code.google.com/p/ala/issues/csv?num=500 > `date "+%Y-%m-%d"`-ala-google-code-issues-raw.csv
```
#####Chop off the first line form the CSV file (it contains the keys - column names)
```BASH
# NOTE: one could modify the python script to use the first line to read the key
# names instead of having them hardcoded in the python; that would eliminate the
# need for this deletion too.
tail -n +2 2014-08-06-ala-google-code-issues-raw.csv > 2014-08-06-ala-google-code-issues.csv
```
#####Pass the CVS file to [csv2json.py](https://github.com/AtlasOfLivingAustralia/misc/blob/master/code.google-issues-2-github-issues/csv2json.py) script to scrape the issue details from code.google.com this will generate a JSON output file containing the scraped issues:
```BASH
python csv2json.py 2014-08-06-ala-google-code-issues.csv > 2014-08-06-ala-google-code-issues.csv-scrape-report.html
# creates:
#    2014-08-06-ala-google-code-issues.csv.json
#    2014-08-06-ala-google-code-issues.csv-scrape-report.html (a HTML table/report about errors/problems found) 
```
see [2014-08-06-ala-google-code-issues.csv.json](https://raw.githubusercontent.com/AtlasOfLivingAustralia/misc/cb72362cbe0577e1a88c1c04c1cfb29e6fad208c/code.google-issues-2-github-issues/data/ala-issues-all-2014-08-06.csv.json) for an example.

#####Migrate (map & upload) the issues from the JSON file to your github issues using the [github api v3](https://developer.github.com/v3)



---
OLDER info:

```BASH
# that generates
#    - ala-issues-all-2014-07-15.csv.json for migration
#    - and HTML table problem report is stored in ala-issues-all-2014-07-15.csv.html
#
python csv2json.py ala-issues-all-2014-07-15.csv > ala-issues-all-2014-07-15.csv.html
```
##### translate the .csv into json format (creates ala-issues-all-2014-07-15.csv.json
```BASH
python csv2json.py ala-issues-all-2014-07-15.csv
```
##### examine the output json file
```BASH
cat ala-issues-all-2014-07-15.csv.json | python -m json.tool
```
##### get the name-s of all available project-s extracted from [https://code.google.com/p/ala/issues/list](https://code.google.com/p/ala/issues/list); each of these has to be mapped into a destination - a github repo name where you want to migrate the issue for that project (for example all issues from our code.google.com issue tracker tagged with `"project": "FieldCapture"` will be migrated to [https://github.com/AtlasOfLivingAustralia/fieldcapture/issues](https://github.com/AtlasOfLivingAustralia/fieldcapture/issues))
```BASH
cat ala-issues-all-2014-07-17.csv.json | python -m json.tool | grep -e "\"project\"" | sort |uniq
        "project": "Alerts"
        "project": "ASBP"
        "project": "AUTH"
        "project": "AVH"
        "project": "BHL"
        "project": "BIE"
        "project": "biocache"
        "project": "Biocache"
        "project": "Browser-All"
        "project": "BVP"
        "project": "Collectory"
        "project": "Component-UI"
        "project": "Dashboard"
        "project": "f"
        "project": "FieldCapture"
        "project": "Geonetwork"
        "project": "Hubs"
        "project": "ImageService"
        "project": "LayerServices"
        "project": "ListsTool"
        "project": "ListTool"
        "project": "NameMatching"
        "project": "names"
        "project": "OzAtlasAndroid"
        "project": "Regions"
        "project": "Sandbox"
        "project": "Sighitngs"
        "project": "Sightings"
        "project": "SpatialPortal"
        "project": "WEBAPI"
```
##### get all available issue owners extracted from [https://code.google.com/p/ala/issues/list](https://code.google.com/p/ala/issues/list); each of these has to be mapped into a github user
```BASH
cat ala-issues-all-2014-07-17.csv.json | python -m json.tool|grep -e "\"Owner\":"|sort|uniq
        "Owner": "",
        "Owner": "adam.collins832",
        "Owner": "chris.flemming.ala",
        "Owner": "chris.godwin.ala",
        "Owner": "CoolDad67",
        "Owner": "david.baird.ala",
        "Owner": "drdavematthews",
        "Owner": "john.tann@austmus.gov.au",
        "Owner": "Kristen.williams@csiro.au",
        "Owner": "leebelbin",
        "Owner": "linda.riq",
        "Owner": "mark.woolston@csiro.au",
        "Owner": "milo_nicholls@hotmail.com",
        "Owner": "moyesyside",
        "Owner": "nickdos",
        "Owner": "Sathish.Sathyamoorthy",
        "Owner": "simon.bear@csiro.au",
        "Owner": "snomelf",
        "Owner": "waterandbirds",
```
##### get all available issue statuses (statii) extracted from [https://code.google.com/p/ala/issues/list](https://code.google.com/p/ala/issues/list); each of these has to be mapped into a github status
```BASH
cat ala-issues-all-2014-07-17.csv.json | python -m json.tool|grep -e "\"Status\":"|sort|uniq
        "Status": "Accepted",
        "Status": "Blocked",
        "Status": "New",
        "Status": "OnDev",
        "Status": "Started",
```
##### get all available issue types extracted from [https://code.google.com/p/ala/issues/list](https://code.google.com/p/ala/issues/list); each of these has to be mapped into a github issue type
```BASH
cat ala-issues-all-2014-07-17.csv.json | python -m json.tool|grep -e "\"Type\":"|sed -e "s/,//"|sort|uniq
        "Type": ""
        "Type": "Defect"
        "Type": "Enhancement"
        "Type": "Review"
        "Type": "Task"
```
##### get all available issue priorities extracted from [https://code.google.com/p/ala/issues/list](https://code.google.com/p/ala/issues/list); each of these has to be mapped into a github issue priority
NOTE: obviously synonyms like `high, High, HIgh` and/or `low, Low` are going to be merged into only one priority type High and Low respectively.  
```BASH
cat ala-issues-all-2014-07-17.csv.json | python -m json.tool|grep -e "\"Priority\":"|sed -e "s/,//"|sort|uniq
        "Priority": ""
        "Priority": "Critical"
        "Priority": "high"
        "Priority": "High"
        "Priority": "HIgh"
        "Priority": "low"
        "Priority": "Low"
        "Priority": "Medium"
```

---

#### using the [github api v3](https://developer.github.com/v3)
```BASH
curl --user "mbohun" https://api.github.com/users/mbohun
Enter host password for user 'mbohun':
{
  "login": "mbohun",
  "id": 1772897,
  "avatar_url": "https://avatars.githubusercontent.com/u/1772897?",
  "gravatar_id": "dcdbc4e57c547efe72932b586079d9d6",
  "url": "https://api.github.com/users/mbohun",
  "html_url": "https://github.com/mbohun",
  "followers_url": "https://api.github.com/users/mbohun/followers",
  "following_url": "https://api.github.com/users/mbohun/following{/other_user}",
  "gists_url": "https://api.github.com/users/mbohun/gists{/gist_id}",
  "starred_url": "https://api.github.com/users/mbohun/starred{/owner}{/repo}",
  "subscriptions_url": "https://api.github.com/users/mbohun/subscriptions",
  "organizations_url": "https://api.github.com/users/mbohun/orgs",
  "repos_url": "https://api.github.com/users/mbohun/repos",
  "events_url": "https://api.github.com/users/mbohun/events{/privacy}",
  "received_events_url": "https://api.github.com/users/mbohun/received_events",
  "type": "User",
  "site_admin": false,
  "name": "Martin Bohun",
  "company": null,
  "blog": "https://www.google.com/+MartinBohun",
  "location": "Canberra, ACT, Australia",
  "email": null,
  "hireable": true,
  "bio": null,
  "public_repos": 14,
  "public_gists": 54,
  "followers": 11,
  "following": 2,
  "created_at": "2012-05-24T06:28:16Z",
  "updated_at": "2014-07-21T02:03:43Z",
  "private_gists": 13,
  "total_private_repos": 0,
  "owned_private_repos": 0,
  "disk_usage": 21889,
  "collaborators": 0,
  "plan": {
    "name": "free",
    "space": 307200,
    "collaborators": 0,
    "private_repos": 0
  }
}
```
##### GET all issues for atlasoflivingaustralia biocache-hubs repo
```BASH
curl --user "mbohun" https://api.github.com/repos/atlasoflivingaustralia/biocache-hubs/issues
Enter host password for user 'mbohun':
[
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/3",
    "labels_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/3/labels{/name}",
    "comments_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/3/comments",
    "events_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/3/events",
    "html_url": "https://github.com/AtlasOfLivingAustralia/biocache-hubs/issues/3",
    "id": 38275672,
    "number": 3,
    "title": "Add links to associated records",
    "user": {
      "login": "nickdos",
      "id": 532845,
      "avatar_url": "https://avatars.githubusercontent.com/u/532845?",
      "gravatar_id": "e836c5faea5deb9e6567db9433628fc2",
      "url": "https://api.github.com/users/nickdos",
      "html_url": "https://github.com/nickdos",
      "followers_url": "https://api.github.com/users/nickdos/followers",
      "following_url": "https://api.github.com/users/nickdos/following{/other_user}",
      "gists_url": "https://api.github.com/users/nickdos/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/nickdos/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/nickdos/subscriptions",
      "organizations_url": "https://api.github.com/users/nickdos/orgs",
      "repos_url": "https://api.github.com/users/nickdos/repos",
      "events_url": "https://api.github.com/users/nickdos/events{/privacy}",
      "received_events_url": "https://api.github.com/users/nickdos/received_events",
      "type": "User",
      "site_admin": false
    },
    "labels": [
      {
        "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/enhancement",
        "name": "enhancement",
        "color": "84b6eb"
      }
    ],
    "state": "open",
    "assignee": {
      "login": "nickdos",
      "id": 532845,
      "avatar_url": "https://avatars.githubusercontent.com/u/532845?",
      "gravatar_id": "e836c5faea5deb9e6567db9433628fc2",
      "url": "https://api.github.com/users/nickdos",
      "html_url": "https://github.com/nickdos",
      "followers_url": "https://api.github.com/users/nickdos/followers",
      "following_url": "https://api.github.com/users/nickdos/following{/other_user}",
      "gists_url": "https://api.github.com/users/nickdos/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/nickdos/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/nickdos/subscriptions",
      "organizations_url": "https://api.github.com/users/nickdos/orgs",
      "repos_url": "https://api.github.com/users/nickdos/repos",
      "events_url": "https://api.github.com/users/nickdos/events{/privacy}",
      "received_events_url": "https://api.github.com/users/nickdos/received_events",
      "type": "User",
      "site_admin": false
    },
    "milestone": null,
    "comments": 2,
    "created_at": "2014-07-21T04:16:11Z",
    "updated_at": "2014-07-21T04:45:03Z",
    "closed_at": null,
    "body": "Records that have a duplication_status value do NOT currently link through to the associated records - the record page simply states there are associated records. E.g. http://biocache.ala.org.au/occurrences/34096adc-4d86-4fed-9d56-14d4603d05c4 has:\r\n\r\nAssociated Occurrence Status:\t Representative record\r\n\r\nWe need to create a link to also show a list of all the associated records."
  }
]
```
##### POST to create an issue test 
```BASH
curl --user "mbohun" --request POST --data '{ "title": "only a test issue, created using github api v3 from BASH and curl", "body": "This is the issues body, description, very deep in all important details.", "assignee": "nickdos", "labels": ["Label1", "Label2"] }' https://api.github.com/repos/atlasoflivingaustralia/biocache-hubs/issues
Enter host password for user 'mbohun':
{
  "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "labels_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/labels{/name}",
  "comments_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/comments",
  "events_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/events",
  "html_url": "https://github.com/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "id": 38279675,
  "number": 4,
  "title": "only a test issue, created using github api v3 from BASH and curl",
  "user": {
    "login": "mbohun",
    "id": 1772897,
    "avatar_url": "https://avatars.githubusercontent.com/u/1772897?",
    "gravatar_id": "dcdbc4e57c547efe72932b586079d9d6",
    "url": "https://api.github.com/users/mbohun",
    "html_url": "https://github.com/mbohun",
    "followers_url": "https://api.github.com/users/mbohun/followers",
    "following_url": "https://api.github.com/users/mbohun/following{/other_user}",
    "gists_url": "https://api.github.com/users/mbohun/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/mbohun/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/mbohun/subscriptions",
    "organizations_url": "https://api.github.com/users/mbohun/orgs",
    "repos_url": "https://api.github.com/users/mbohun/repos",
    "events_url": "https://api.github.com/users/mbohun/events{/privacy}",
    "received_events_url": "https://api.github.com/users/mbohun/received_events",
    "type": "User",
    "site_admin": false
  },
  "labels": [
    {
      "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/Label1",
      "name": "Label1",
      "color": "ededed"
    },
    {
      "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/Label2",
      "name": "Label2",
      "color": "ededed"
    }
  ],
  "state": "open",
  "assignee": {
    "login": "nickdos",
    "id": 532845,
    "avatar_url": "https://avatars.githubusercontent.com/u/532845?",
    "gravatar_id": "e836c5faea5deb9e6567db9433628fc2",
    "url": "https://api.github.com/users/nickdos",
    "html_url": "https://github.com/nickdos",
    "followers_url": "https://api.github.com/users/nickdos/followers",
    "following_url": "https://api.github.com/users/nickdos/following{/other_user}",
    "gists_url": "https://api.github.com/users/nickdos/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/nickdos/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/nickdos/subscriptions",
    "organizations_url": "https://api.github.com/users/nickdos/orgs",
    "repos_url": "https://api.github.com/users/nickdos/repos",
    "events_url": "https://api.github.com/users/nickdos/events{/privacy}",
    "received_events_url": "https://api.github.com/users/nickdos/received_events",
    "type": "User",
    "site_admin": false
  },
  "milestone": null,
  "comments": 0,
  "created_at": "2014-07-21T06:48:35Z",
  "updated_at": "2014-07-21T06:48:35Z",
  "closed_at": null,
  "body": "This is the issues body, description, very deep in all important details.",
  "closed_by": null
}
```
##### POST to edit/modify an existing issue
```BASH
curl --user "mbohun" --request POST --data '{ "title": "Only a TEST issue, created from the commandline using github api v3 from BASH and curl", "body": "see https://gist.github.com/mbohun/af110bcd6e6178b7def3 for beautiful details how this issue was created and edited.", "assignee": "djtfmartin", "labels": ["Label1", "Label2"] }' https://api.github.com/repos/atlasoflivingaustralia/biocache-hubs/issues/4
Enter host password for user 'mbohun':
{
  "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "labels_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/labels{/name}",
  "comments_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/comments",
  "events_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/events",
  "html_url": "https://github.com/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "id": 38279675,
  "number": 4,
  "title": "Only a TEST issue, created from the commandline using github api v3 from BASH and curl",
  "user": {
    "login": "mbohun",
    "id": 1772897,
    "avatar_url": "https://avatars.githubusercontent.com/u/1772897?",
    "gravatar_id": "dcdbc4e57c547efe72932b586079d9d6",
    "url": "https://api.github.com/users/mbohun",
    "html_url": "https://github.com/mbohun",
    "followers_url": "https://api.github.com/users/mbohun/followers",
    "following_url": "https://api.github.com/users/mbohun/following{/other_user}",
    "gists_url": "https://api.github.com/users/mbohun/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/mbohun/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/mbohun/subscriptions",
    "organizations_url": "https://api.github.com/users/mbohun/orgs",
    "repos_url": "https://api.github.com/users/mbohun/repos",
    "events_url": "https://api.github.com/users/mbohun/events{/privacy}",
    "received_events_url": "https://api.github.com/users/mbohun/received_events",
    "type": "User",
    "site_admin": false
  },
  "labels": [
    {
      "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/Label1",
      "name": "Label1",
      "color": "ededed"
    },
    {
      "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/Label2",
      "name": "Label2",
      "color": "ededed"
    }
  ],
  "state": "open",
  "assignee": {
    "login": "djtfmartin",
    "id": 444897,
    "avatar_url": "https://avatars.githubusercontent.com/u/444897?",
    "gravatar_id": "8fccf27675dce1089c7db391650ec09d",
    "url": "https://api.github.com/users/djtfmartin",
    "html_url": "https://github.com/djtfmartin",
    "followers_url": "https://api.github.com/users/djtfmartin/followers",
    "following_url": "https://api.github.com/users/djtfmartin/following{/other_user}",
    "gists_url": "https://api.github.com/users/djtfmartin/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/djtfmartin/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/djtfmartin/subscriptions",
    "organizations_url": "https://api.github.com/users/djtfmartin/orgs",
    "repos_url": "https://api.github.com/users/djtfmartin/repos",
    "events_url": "https://api.github.com/users/djtfmartin/events{/privacy}",
    "received_events_url": "https://api.github.com/users/djtfmartin/received_events",
    "type": "User",
    "site_admin": false
  },
  "milestone": null,
  "comments": 0,
  "created_at": "2014-07-21T06:48:35Z",
  "updated_at": "2014-07-21T07:06:08Z",
  "closed_at": null,
  "body": "see https://gist.github.com/mbohun/af110bcd6e6178b7def3 for beautiful details how this issue was created and edited.",
  "closed_by": null
}
```
##### PATCH to modify an issue
```BASH
curl --user "mbohun" --request PATCH --data '{ "title": "Changed title using HTTP PATCH (instead of HTTP POST)" }' https://api.github.com/repos/atlasoflivingaustralia/biocache-hubs/issues/4
Enter host password for user 'mbohun':
{
  "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "labels_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/labels{/name}",
  "comments_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/comments",
  "events_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/events",
  "html_url": "https://github.com/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "id": 38279675,
  "number": 4,
  "title": "Changed title using HTTP PATCH (instead of HTTP POST)",
  "user": {
    "login": "mbohun",
    "id": 1772897,
    "avatar_url": "https://avatars.githubusercontent.com/u/1772897?",
    "gravatar_id": "dcdbc4e57c547efe72932b586079d9d6",
    "url": "https://api.github.com/users/mbohun",
    "html_url": "https://github.com/mbohun",
    "followers_url": "https://api.github.com/users/mbohun/followers",
    "following_url": "https://api.github.com/users/mbohun/following{/other_user}",
    "gists_url": "https://api.github.com/users/mbohun/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/mbohun/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/mbohun/subscriptions",
    "organizations_url": "https://api.github.com/users/mbohun/orgs",
    "repos_url": "https://api.github.com/users/mbohun/repos",
    "events_url": "https://api.github.com/users/mbohun/events{/privacy}",
    "received_events_url": "https://api.github.com/users/mbohun/received_events",
    "type": "User",
    "site_admin": false
  },
  "labels": [
    {
      "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/enhancement",
      "name": "enhancement",
      "color": "84b6eb"
    }
  ],
  "state": "open",
  "assignee": {
    "login": "djtfmartin",
    "id": 444897,
    "avatar_url": "https://avatars.githubusercontent.com/u/444897?",
    "gravatar_id": "8fccf27675dce1089c7db391650ec09d",
    "url": "https://api.github.com/users/djtfmartin",
    "html_url": "https://github.com/djtfmartin",
    "followers_url": "https://api.github.com/users/djtfmartin/followers",
    "following_url": "https://api.github.com/users/djtfmartin/following{/other_user}",
    "gists_url": "https://api.github.com/users/djtfmartin/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/djtfmartin/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/djtfmartin/subscriptions",
    "organizations_url": "https://api.github.com/users/djtfmartin/orgs",
    "repos_url": "https://api.github.com/users/djtfmartin/repos",
    "events_url": "https://api.github.com/users/djtfmartin/events{/privacy}",
    "received_events_url": "https://api.github.com/users/djtfmartin/received_events",
    "type": "User",
    "site_admin": false
  },
  "milestone": null,
  "comments": 3,
  "created_at": "2014-07-21T06:48:35Z",
  "updated_at": "2014-07-22T09:04:34Z",
  "closed_at": null,
  "body": "see https://gist.github.com/mbohun/af110bcd6e6178b7def3 for beautiful details how this issue was created and edited.",
  "closed_by": null
}
```
##### POST to comment on an issue
```BASH
curl --user "mbohun" --request POST --data '{ "body": "This is the very first comment on an issue created from the commandline using the github api v3, ladies and gentlemen." }' https://api.github.com/repos/atlasoflivingaustralia/biocache-hubs/issues/4/comments
Enter host password for user 'mbohun':
{
  "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/comments/49577117",
  "html_url": "https://github.com/AtlasOfLivingAustralia/biocache-hubs/issues/4#issuecomment-49577117",
  "issue_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "id": 49577117,
  "user": {
    "login": "mbohun",
    "id": 1772897,
    "avatar_url": "https://avatars.githubusercontent.com/u/1772897?",
    "gravatar_id": "dcdbc4e57c547efe72932b586079d9d6",
    "url": "https://api.github.com/users/mbohun",
    "html_url": "https://github.com/mbohun",
    "followers_url": "https://api.github.com/users/mbohun/followers",
    "following_url": "https://api.github.com/users/mbohun/following{/other_user}",
    "gists_url": "https://api.github.com/users/mbohun/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/mbohun/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/mbohun/subscriptions",
    "organizations_url": "https://api.github.com/users/mbohun/orgs",
    "repos_url": "https://api.github.com/users/mbohun/repos",
    "events_url": "https://api.github.com/users/mbohun/events{/privacy}",
    "received_events_url": "https://api.github.com/users/mbohun/received_events",
    "type": "User",
    "site_admin": false
  },
  "created_at": "2014-07-21T07:15:11Z",
  "updated_at": "2014-07-21T07:15:11Z",
  "body": "This is the very first comment on an issue created from the commandline using the github api v3, ladies and gentlemen."
}
```
##### POST to change the label-s of an issue to (one of the predefined labels) "enhancement"
```BASH
curl --user "mbohun" --request POST --data '{ "labels": ["enhancement"] }' https://api.github.com/repos/atlasoflivingaustralia/biocache-hubs/issues/4
Enter host password for user 'mbohun':
{
  "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "labels_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/labels{/name}",
  "comments_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/comments",
  "events_url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/issues/4/events",
  "html_url": "https://github.com/AtlasOfLivingAustralia/biocache-hubs/issues/4",
  "id": 38279675,
  "number": 4,
  "title": "Only a TEST issue, created from the commandline using github api v3 from BASH and curl",
  "user": {
    "login": "mbohun",
    "id": 1772897,
    "avatar_url": "https://avatars.githubusercontent.com/u/1772897?",
    "gravatar_id": "dcdbc4e57c547efe72932b586079d9d6",
    "url": "https://api.github.com/users/mbohun",
    "html_url": "https://github.com/mbohun",
    "followers_url": "https://api.github.com/users/mbohun/followers",
    "following_url": "https://api.github.com/users/mbohun/following{/other_user}",
    "gists_url": "https://api.github.com/users/mbohun/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/mbohun/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/mbohun/subscriptions",
    "organizations_url": "https://api.github.com/users/mbohun/orgs",
    "repos_url": "https://api.github.com/users/mbohun/repos",
    "events_url": "https://api.github.com/users/mbohun/events{/privacy}",
    "received_events_url": "https://api.github.com/users/mbohun/received_events",
    "type": "User",
    "site_admin": false
  },
  "labels": [
    {
      "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/enhancement",
      "name": "enhancement",
      "color": "84b6eb"
    }
  ],
  "state": "open",
  "assignee": {
    "login": "djtfmartin",
    "id": 444897,
    "avatar_url": "https://avatars.githubusercontent.com/u/444897?",
    "gravatar_id": "8fccf27675dce1089c7db391650ec09d",
    "url": "https://api.github.com/users/djtfmartin",
    "html_url": "https://github.com/djtfmartin",
    "followers_url": "https://api.github.com/users/djtfmartin/followers",
    "following_url": "https://api.github.com/users/djtfmartin/following{/other_user}",
    "gists_url": "https://api.github.com/users/djtfmartin/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/djtfmartin/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/djtfmartin/subscriptions",
    "organizations_url": "https://api.github.com/users/djtfmartin/orgs",
    "repos_url": "https://api.github.com/users/djtfmartin/repos",
    "events_url": "https://api.github.com/users/djtfmartin/events{/privacy}",
    "received_events_url": "https://api.github.com/users/djtfmartin/received_events",
    "type": "User",
    "site_admin": false
  },
  "milestone": null,
  "comments": 1,
  "created_at": "2014-07-21T06:48:35Z",
  "updated_at": "2014-07-21T07:29:41Z",
  "closed_at": null,
  "body": "see https://gist.github.com/mbohun/af110bcd6e6178b7def3 for beautiful details how this issue was created and edited.",
  "closed_by": null
}
```
##### GET all (default) github issue labels
```BASH
curl --user "mbohun" https://api.github.com/repos/atlasoflivingaustralia/fieldcapture/labels
Enter host password for user 'mbohun':
[
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/fieldcapture/labels/bug",
    "name": "bug",
    "color": "fc2929"
  },
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/fieldcapture/labels/duplicate",
    "name": "duplicate",
    "color": "cccccc"
  },
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/fieldcapture/labels/enhancement",
    "name": "enhancement",
    "color": "84b6eb"
  },
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/fieldcapture/labels/help+wanted",
    "name": "help wanted",
    "color": "159818"
  },
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/fieldcapture/labels/invalid",
    "name": "invalid",
    "color": "e6e6e6"
  },
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/fieldcapture/labels/question",
    "name": "question",
    "color": "cc317c"
  },
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/fieldcapture/labels/wontfix",
    "name": "wontfix",
    "color": "ffffff"
  }
]
```
##### GET all labels for atlasoflivingaustralia biocache-hubs (where we previously created two custom labels `Label1` and `Label2`); are we going to use custom labels for issue priority (Priority-Low, Priority-Medium, Priority-High, Priority-Critical) and other code.google.com Label-s that do not have a github counterpart?
```BASH
curl --user "mbohun" https://api.github.com/repos/atlasoflivingaustralia/biocache-hubs/labels
Enter host password for user 'mbohun':
[
  {
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/bug",
    "name": "bug",
    "color": "fc2929"
  },
  { 
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/duplicate",
    "name": "duplicate",
    "color": "cccccc"
  },
  { 
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/enhancement",
    "name": "enhancement",
    "color": "84b6eb"
  },
  { 
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/help+wanted",
    "name": "help wanted",
    "color": "159818"
  },
  { 
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/invalid",
    "name": "invalid",
    "color": "e6e6e6"
  },
  { 
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/question",
    "name": "question",
    "color": "cc317c"
  },
  { 
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/wontfix",
    "name": "wontfix",
    "color": "ffffff"
  },
  { 
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/Label1",
    "name": "Label1",
    "color": "ededed"
  },
  { 
    "url": "https://api.github.com/repos/AtlasOfLivingAustralia/biocache-hubs/labels/Label2",
    "name": "Label2",
    "color": "ededed"
  }
]
```
