#!/bin/bash

# WARNING: github is case insensitive, the travis/tavis client *IS* case sensitive
#          i found out when: 'travis encrypt -r atlasoflivingaustralia/reponame ...' FAILED, while
#          'travis encrypt -r AtlasOfLivingAustralia/reponame ...' works OK
#
GITHUB_USER_ORG="AtlasOfLivingAustralia"

if [ -z "$1" ]; then
    echo "usage: ./github-add-travis.sh [github-username] [github-token]"
    exit 1;
fi

GITHUB_USERNAME=$1
GITHUB_TOKEN=$2

temp=`basename $0`
TMPFILE=`mktemp /tmp/${temp}.XXXXXX` || exit 1

# single page result-s (no pagination), have no Link: section, the grep result is empty
last_page=`curl -s -I "https://api.github.com/users/$GITHUB_USER_ORG/repos" | grep '^Link:'`

# does this result use pagination?
if [ -z "$last_page" ]; then
    # no - this result has only one page
    curl -s -i "https://api.github.com/users/$GITHUB_USER_ORG/repos" | grep '"name":' >> $TMPFILE;

else
    # yes - this result is on multiple pages; extract the last_page number
    last_page=`echo $last_page | sed -e 's/^Link:.*page=//g' -e 's/>.*$//g'`

    p=1
    while [ "$p" -le "$last_page" ]; do
	curl -s -i "https://api.github.com/users/$GITHUB_USER_ORG/repos?page=$p" | grep '"name":' >> $TMPFILE
	p=$(($p + 1))
    done
fi

# TODO: remember PWD
RESULT=./result.out
echo "" > $RESULT

for repo in `cat $TMPFILE | sed -e 's/^ *"name": "//g' -e 's/",$//g' | sort`
do
    git clone git@github.com:$GITHUB_USER_ORG/$repo.git
    cd $repo
    if [ ! -e ".travis"]
    then
	echo "$repo" >> $RESULT 
    fi
done
