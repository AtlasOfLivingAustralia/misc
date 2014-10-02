#!/bin/bash

# TODO: run a requirements check? check for wget, curl, travis client, etc?
# travis client is /usr/bin/travis2.0 on my openSUSE13.1 laptop, while the mac os x uses /usr/bin/travis
TRAVIS_CLIENT=/usr/bin/travis2.0



# WARNING: github is case insensitive, the travis/tavis client *IS* case sensitive
#          i found out when: 'travis encrypt -r atlasoflivingaustralia/reponame ...' FAILED, while
#          'travis encrypt -r AtlasOfLivingAustralia/reponame ...' works OK
#
GITHUB_USER_ORG="AtlasOfLivingAustralia"

if [ -z "$1" ] || [ -z "$2" ] || [ ! -e "$2" ] ; then
    echo "usage: ./github-add-travis.sh [github-token] [environment-variables-file]"
    exit 1;
fi

GITHUB_TOKEN=$1
VARS_TO_ENCRYPT=`cat $2`

temp=`basename $0`
TMPFILE=`mktemp /tmp/${temp}.XXXXXX` || exit 1

# single page result-s (no pagination), have no Link: section, the grep result is empty
last_page=`curl -s -I "https://api.github.com/users/$GITHUB_USER_ORG/repos" -H "Authorization: token $GITHUB_TOKEN" | grep '^Link:'`

# does this result use pagination?
if [ -z "$last_page" ]; then
    # no - this result has only one page
    curl -s -i "https://api.github.com/users/$GITHUB_USER_ORG/repos" -H "Authorization: token $GITHUB_TOKEN" | grep '"name":' >> $TMPFILE;

else
    # yes - this result is on multiple pages; extract the last_page number
    last_page=`echo $last_page | sed -e 's/^Link:.*page=//g' -e 's/>.*$//g'`

    p=1
    while [ "$p" -le "$last_page" ]; do
	curl -s -i "https://api.github.com/users/$GITHUB_USER_ORG/repos?page=$p" -H "Authorization: token $GITHUB_TOKEN" | grep '"name":' >> $TMPFILE
	p=$(($p + 1))
    done
fi

# TODO: remember PWD
TMP_DIR=$PWD/github-add-travis
rm -rf $TMP_DIR
mkdir -p $TMP_DIR

# TODO: check logins at the start, do not bother if they failed
$TRAVIS_CLIENT login --github-token $GITHUB_TOKEN

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
	# download/copy in the grails project .travis template, TODO: add support for a custom .travis.yml template/boilerplate later
	wget -q -O .travis.yml https://raw.githubusercontent.com/AtlasOfLivingAustralia/travis-build-configuration/master/doc/travis-grails_template.yml
    fi

    if [ -e "pom.xml" ]
    then
	wget -q -O .travis.yml https://raw.githubusercontent.com/AtlasOfLivingAustralia/travis-build-configuration/master/doc/travis-java_template.yml
    fi

    # TODO: add support for more project types (android/gradle, etc.)

    # encrypt and add env variables to .travis.yml
    for v in $VARS_TO_ENCRYPT
    do
	# encrypt env variables, for example: TRAVIS_DEPLOY_USERNAME, TRAVIS_DEPLOY_PASSWORD, etc.
	$TRAVIS_CLIENT encrypt -a -p -r $GITHUB_USER_ORG/$repo "$v"
    done

    git add .travis.yml

    # if README.md does NOT exist (yet) create one
    if [ ! -e "README.md" ]
    then
	touch README.md
    fi

    # does the README.md file already contain travis-i.org build status badge?
    grep "\[\!\[Build Status\](https://travis-ci.org/$GITHUB_USER_ORG/$repo\.svg)\]" ./README.md
    if [ "$?" = "1" ]
    then
	# NOTE: given this is not a fully automated process, we do not handle bracnhes, etc. the README.md needs to be adjusted manually
	echo "### $repo   [![Build Status](https://travis-ci.org/$GITHUB_USER_ORG/$repo.svg?branch=master)](https://travis-ci.org/$GITHUB_USER_ORG/$repo)" >> ./HEADER.md
	cat README.md >> HEADER.md
	mv HEADER.md README.md
	git add README.md
    fi

    git commit -m "GENERATED: adding travis-ci.org support"

    # push/publish all the changes we made
    git push

done
