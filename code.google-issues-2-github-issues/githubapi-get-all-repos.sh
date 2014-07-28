#!/bin/bash

# "For unauthenticated requests, the rate limit allows you to make up to 60 requests per hour."
# https://developer.github.com/v3/#rate-limiting
#
GITHUB_REQUEST_RATE=2

temp=`basename $0`
TMPFILE=`mktemp /tmp/${temp}.XXXXXX` || exit 1

last_page=`curl -s -I "https://api.github.com/orgs/atlasoflivingaustralia/repos" | grep '^Link:' | sed -e 's/^Link:.*page=//g' | sed -e 's/>.*$//g'`
sleep $GITHUB_REQUEST_RATE

p=1
while [ "$p" -le "$last_page" ]; do
    curl -s -i "https://api.github.com/orgs/atlasoflivingaustralia/repos?page=$p" | grep '"name":' | sed -e 's/^.*name"://g' >> $TMPFILE
    p=$(($p + 1))
    sleep $GITHUB_REQUEST_RATE
done

cat $TMPFILE | sed -e 's/^ "//g' | sed -e 's/",$//g'| sort
