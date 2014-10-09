#!/bin/bash

# we need at least one arg: gihub user/organization
if [ -z "$1" ]; then
    echo "usage: $0 [github user/organization] repo0 repo1 repo2 ... repoN"
    exit 1;
fi

GITHUB_USER_ORG=$1

# args 2, 3, 4 ... N are repo names, so skip arg1 required/positional args to adjust $@
shift 1
GITHUB_REPOS="$@"
echo $GITHUB_REPOS

TMP_DIR=/tmp/$0
rm -rf $TMP_DIR
mkdir -p $TMP_DIR

SUMMARY=$TMP_DIR/summary.md
rm -rf $SUMMARY

# create .md table header
echo "|repo|travis build status|" >> $SUMMARY
echo "|:---|:------------------|" >> $SUMMARY

for repo in $GITHUB_REPOS
do
    cd $TMP_DIR
    rm -rf $repo

    git clone git@github.com:$GITHUB_USER_ORG/$repo.git

    cd $repo
    if [ ! -e ".travis.yml" ]
    then
	echo "|$repo|N/A|" >> $SUMMARY

    else
	echo "|[$repo](https://github.com/$GITHUB_USER_ORG/$repo)|[![Build Status](https://travis-ci.org/$GITHUB_USER_ORG/$repo.svg?branch=master)](https://travis-ci.org/$GITHUB_USER_ORG/$repo)|" >> $SUMMARY

    fi

    # cleanup
    cd $TMP_DIR
    rm -rf $repo
done

cat $SUMMARY
