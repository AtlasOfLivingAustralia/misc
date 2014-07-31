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
```

