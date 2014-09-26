#!/bin/bash

# TODO: run a requirements check? check for wget, curl, travis client, etc?

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
TMP_DIR=/tmp/github-add-travis
rm -rf $TMP_DIR
mkdir -p $TMP_DIR

# TODO: check logins at the start, do not bother if they failed
travis login --github-token $GITHUB_TOKEN

for repo in `cat $TMPFILE | sed -e 's/^ *"name": "//g' -e 's/",$//g' | sort`
do
    cd $TMP_DIR
    rm -rf $repo

    git clone git@github.com:$GITHUB_USER_ORG/$repo.git

    cd $repo
    if [ -e ".travis.yml" ]
    then
	echo "$repo alrady has .travis.yml skipping..."
	continue
    fi

    # TODO: this should be case statement case: grails or java or whatever...

    # TODO: make this check if is this a grails project safer/specific; grep for grails app?
    if [ -e "application.properties" ]
    then
	# download/copy in the grails project .travis template
	wget -q -O .travis.yml https://raw.githubusercontent.com/AtlasOfLivingAustralia/travis-build-configuration/master/doc/travis-grails_template.yml

	# TODO: make this a proper loop for each "VAR_NAME=value"
	# encrypt env variables, for example: TRAVIS_DEPLOY_USERNAME, TRAVIS_DEPLOY_PASSWORD, etc.
	travis -a -p -r $GITHUB_USER_ORG/$repo "TRAVIS_DEPLOY_USERNAME=deployment"
	travis -a -p -r $GITHUB_USER_ORG/$repo "TRAVIS_DEPLOY_PASSWORD=mavenrepo"

	git commit .travis.yml -m "added .travis.yml; encrypted env vars"
    fi

    # TODO: pom.xml
    # if [ -e "pom.xml" ]

done
