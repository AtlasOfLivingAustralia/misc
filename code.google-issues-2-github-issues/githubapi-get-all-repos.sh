#!/bin/bash

if [ -z "$1" ]; then
    echo "usage: ./githubapi-get-all-repos.sh [github username]"
    exit 1;
fi

# "For unauthenticated requests, the rate limit allows you to make up to 60 requests per hour."
# https://developer.github.com/v3/#rate-limiting
#
GITHUB_REQUEST_RATE=2

temp=`basename $0`
TMPFILE=`mktemp /tmp/${temp}.XXXXXX` || exit 1

# single page result-s (no pagination), have no Link: section, the grep result is empty
last_page=`curl -s -I "https://api.github.com/users/$1/repos" | grep '^Link:'`
sleep $GITHUB_REQUEST_RATE

# does this result use pagination?
if [ -z "$last_page" ]; then
    # no - this result has only one page
    curl -s -i "https://api.github.com/users/$1/repos" | grep '"name":' >> $TMPFILE;

else
    # yes - this result is on multiple pages; extract the last_page number
    last_page=`echo $last_page | sed -e 's/^Link:.*page=//g' | sed -e 's/>.*$//g'`

    p=1
    while [ "$p" -le "$last_page" ]; do
	curl -s -i "https://api.github.com/users/$1/repos?page=$p" | grep '"name":' >> $TMPFILE
	p=$(($p + 1))
	sleep $GITHUB_REQUEST_RATE
    done
fi

cat $TMPFILE | sed -e 's/^ *"name": "//g' | sed -e 's/",$//g' | sort
