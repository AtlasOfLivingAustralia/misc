### PROBLEM
Some of the code.google.com issues are referring (link) to other issue-s; for example the issue [747](https://code.google.com/p/ala/issues/detail?id=747) is referring to the issue [561](https://code.google.com/p/ala/issues/detail?id=561)

```JSON
{
    AllLabels: "FieldCapture, Priority-Low, Type-Enhancement",
    ID: "747",
    Modified: "Jul 06, 2014 08:48:05",
    ModifiedTimestamp: "1404636485",
    Owner: "CoolDad67",
    Priority: "Low",
    Status: "New",
    Summary: "New tab on project activities page - Output Reconciliation",
    Type: "Enhancement",
    comments: [
        " ",
        " "
    ],
    details: [
        {
            pre-full: "['\nInsert a new tab next to the Gantt chart view on the Activities page for a stage-based reconciliation view of output targets. Design still to be provided.\r\n\r\nThis task is dependednt on implementation of ', ' and should ideally be done in conjunction with that task.\n']"
        },
        {
            pre: {
                text: " Insert a new tab next to the Gantt chart view on the Activities page for a stage-based reconciliation view of output targets. Design still to be provided. This task is dependednt on implementation of "
            }
        },
        {
            a: {
                link: "/p/ala/issues/detail?id=561",
                text: "issue 561"
            }
        }
    ],
    project: "FieldCapture"
}
```

```JSON
{
    AllLabels: "FieldCapture, Priority-Low, Type-Enhancement",
    ID: "561",
    Modified: "Jul 06, 2014 03:39:23",
    ModifiedTimestamp: "1404617963",
    Owner: "chris.godwin.ala",
    Priority: "Low",
    Status: "New",
    Summary: "Change output targets from project level to activity level",
    Type: "Enhancement",
    comments: [
        " ",
        " "
    ],
    details: [
        {
            pre-full: "['\nDoE requirement #35\r\nRemove overall output targets and include them for each activity.\r\n\r\nComments - PB 6/2/14\r\nThere have been numerous requests for this from grantees who expected output targets to be set at the activity level. Doing this would placate those and will also enable the development of a "stage reconciliation" view which would eliminate the need for grant manager shadow systems to monitor/manage output reconciliation at the stage/periodic reporting level. This would be highly beneficial and in my opinion would significantly outweigh any potential negative fallout.\r\n\r\nIt is however a 2-edge sword in that some organisations, particularly some NRM bodies), are likely to complain that this is adding detail and complexity, which could be politically unpalatable.\r\n\r\nPriority is set low and further discussion is required, including a specific instruction in an email from DoE to proceed.\n']"
        },
        {
            pre: {
                text: " DoE requirement #35 Remove overall output targets and include them for each activity. Comments - PB 6/2/14 There have been numerous requests for this from grantees who expected output targets to be set at the activity level. Doing this would placate those and will also enable the development of a "stage reconciliation" view which would eliminate the need for grant manager shadow systems to monitor/manage output reconciliation at the stage/periodic reporting level. This would be highly beneficial and in my opinion would significantly outweigh any potential negative fallout. It is however a 2-edge sword in that some organisations, particularly some NRM bodies), are likely to complain that this is adding detail and complexity, which could be politically unpalatable. Priority is set low and further discussion is required, including a specific instruction in an email from DoE to proceed. "
            }
        }
    ],
    project: "FieldCapture"
}
```

Simple grep search for `"/p/ala/issues/detail?id="`
```BASH
bash-3.2$ cat ala-issues-all-2014-07-17.csv.json | python -m json.tool | grep -n "/p/ala/issues/detail?id="
89:                    "link": "/p/ala/issues/detail?id=62",
416:                    "link": "/p/ala/issues/detail?id=538",
422:                    "link": "/p/ala/issues/detail?id=538",
428:                    "link": "/p/ala/issues/detail?id=538",
929:                    "link": "/p/ala/issues/detail?id=489",
4988:                    "link": "/p/ala/issues/detail?id=650",
5479:                    "link": "/p/ala/issues/detail?id=333",
5508:                    "link": "/p/ala/issues/detail?id=333",
7825:                    "link": "/p/ala/issues/detail?id=124",
7880:                    "link": "/p/ala/issues/detail?id=561",
8039:                    "link": "/p/ala/issues/detail?id=543",

bash-3.2$ cat ala-issues-all-2014-07-17.csv.json | python -m json.tool | grep -n "/p/ala/issues/detail?id=" | wc -l
      11
```

Unfortunately 73 (84 - 11 = 73) issues are referring to "disabled" issue tracker-s:
```BASH
bash-3.2$ cat ala-issues-all-2014-07-17.csv.json | python -m json.tool | grep "/issues/detail?id=" | grep '"link":' | grep 'https://' | sed -e 's/^.*"link": "//g' -e 's/\/detail\?id.*$//g' | sort | uniq
https://code.google.com/p/ala-bie/issues
https://code.google.com/p/ala-collectory/issues
https://code.google.com/p/ala-hubs/issues
https://code.google.com/p/ala-portal/issues
https://code.google.com/p/ala-sightings/issues
https://code.google.com/p/ala-volunteer/issues
https://code.google.com/p/alageospatialportal/issues
```

```BASH
bash-3.2$ cat ala-issues-all-2014-07-17.csv.json | python -m json.tool | grep "/issues/detail?id=" | grep '"link":' | sort
                    "link": "/p/ala/issues/detail?id=124",
                    "link": "/p/ala/issues/detail?id=333",
                    "link": "/p/ala/issues/detail?id=333",
                    "link": "/p/ala/issues/detail?id=489",
                    "link": "/p/ala/issues/detail?id=538",
                    "link": "/p/ala/issues/detail?id=538",
                    "link": "/p/ala/issues/detail?id=538",
                    "link": "/p/ala/issues/detail?id=543",
                    "link": "/p/ala/issues/detail?id=561",
                    "link": "/p/ala/issues/detail?id=62",
                    "link": "/p/ala/issues/detail?id=650",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=333",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=333#c13",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=347",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=353",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=355",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=358",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=374",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=380",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=384",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=386",
                    "link": "https://code.google.com/p/ala-bie/issues/detail?id=389",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=14",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=23",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=25",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=26",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=3",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=30",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=36",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=45",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=5",
                    "link": "https://code.google.com/p/ala-collectory/issues/detail?id=6",
                    "link": "https://code.google.com/p/ala-hubs/issues/detail?id=12",
                    "link": "https://code.google.com/p/ala-hubs/issues/detail?id=21",
                    "link": "https://code.google.com/p/ala-hubs/issues/detail?id=84",
                    "link": "https://code.google.com/p/ala-hubs/issues/detail?id=88",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=129",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=142",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=161",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=168",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=171",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=185",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=191",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=194",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=208",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=220",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=229",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=247",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=251",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=254",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=285",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=298",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=299",
                    "link": "https://code.google.com/p/ala-portal/issues/detail?id=300",
                    "link": "https://code.google.com/p/ala-sightings/issues/detail?id=3",
                    "link": "https://code.google.com/p/ala-volunteer/issues/detail?id=26",
                    "link": "https://code.google.com/p/ala-volunteer/issues/detail?id=32",
                    "link": "https://code.google.com/p/ala-volunteer/issues/detail?id=37",
                    "link": "https://code.google.com/p/ala-volunteer/issues/detail?id=56",
                    "link": "https://code.google.com/p/ala-volunteer/issues/detail?id=58",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=1022",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=1069",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=1070",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=1071",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=1075",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=304",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=428",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=442",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=538",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=565",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=575",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=632",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=717",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=737",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=767",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=811",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=898",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=914",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=922",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=952",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=953",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=972",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=991",
                    "link": "https://code.google.com/p/alageospatialportal/issues/detail?id=994",
bash-3.2$ cat ala-issues-all-2014-07-17.csv.json | python -m json.tool | grep "/issues/detail?id=" | grep '"link":' | sort | wc -l
      84
```
