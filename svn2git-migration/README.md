###prepare
1. `cd ~/src`
2. `svn co http://ala-hubs.googlecode.com/svn ala-hubs_svn`
3. `cd ala-hubs_svn`
4. `svn log ^/ --xml | grep "^<author" | sort -u | perl -pe 's/<author>(.*?)<\/author>/$1 = /' >> authors-file.out`
5. ... that should extract the svn user-s and store them in the file `authors_file.out` in the following format:
```
chris.flemming.ala@gmail.com = 
mark.woolston@csiro.au = 
moyesyside@gmail.com = 
...
```
... and you have to fill in the git/github credentials for each of them (` svn.user = github.user.name <github.user.email>`, for example:
```
chris.flemming.ala@gmail.com = cflemming <chris.flemming.github@gmail.com>
...
(no author) = no author <no.author@author.no>
```
the `authors-file.out` mapping file is used in the `git svn clone ...` step; see the step `3.` bellow. NOTE: _It is a good idea (in fact required if your svn repo contains commits from '(no author)' to set a mapping for '(no author)' as shown in the example above)._

###migrate
1. in the web browser go to your github page and create a new repository, in this case: `ala-hub` `git@github.com:AtlasOfLivingAustralia/ala-hub.git`
2. `cd ~/src`
3. `git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/ala-hub --tags=tags --authors-file=./authors-file.out -s ala-hub.git`
4. `cd ~/src/ala-hub.git`
5. `git for-each-ref refs/remotes/tags | cut -d / -f 4- | grep -v @ | while read tagname; do git tag "$tagname" "tags/$tagname"; git branch -r -d "tags/$tagname"; done`
6. `git for-each-ref refs/remotes | cut -d / -f 3- | grep -v @ | while read branchname; do git branch "$branchname" "refs/remotes/$branchname"; git branch -r -d "$branchname"; done`
7. `git remote add origin git@github.com:AtlasOfLivingAustralia/ala-hub.git`
8. `git push origin --all`
9. `git push origin --tags`

###test
* `cd ~/src`
* `git clone git@github.com:AtlasOfLivingAustralia/ala-hub.git`
* `cd ala-hub`
* `git remote show origin`
* etc.

---
so far the following svn modules/apps were migrated from googlecode.com to git/github:
```
git svn clone http://ala-collectory.googlecode.com/svn --trunk=trunk/collectory --tags=tags --authors-file=./authors-file.out -s collectory.git

git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/ala-hub       --tags=tags --authors-file=./authors-file.out -s ala-hub.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/amrin-hub     --tags=tags --authors-file=./authors-file.out -s amrin-hub.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/appd-hub      --tags=tags --authors-file=./authors-file.out -s appd-hub.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/asbp-hub      --tags=tags --authors-file=./authors-file.out -s asbp-hub.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/avh-hub       --tags=tags --authors-file=./authors-file.out -s avh-hub.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/biocache-hubs --tags=tags --authors-file=./authors-file.out -s biocache-hubs.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/generic-hub   --tags=tags --authors-file=./authors-file.out -s generic-hub.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/obis-hub      --tags=tags --authors-file=./authors-file.out -s obis-hub.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/ozcam-hub     --tags=tags --authors-file=./authors-file.out -s ozcam-hub.git
git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/tepapa-hub    --tags=tags --authors-file=./authors-file.out -s tepapa-hub.git

git svn clone http://ala-portal.googlecode.com/svn --trunk=trunk/biocache-jms     --tags=tags --authors-file=./authors-file.out -s biocache-jms.git
git svn clone http://ala-portal.googlecode.com/svn --trunk=trunk/biocache-service --tags=tags --authors-file=./authors-file.out -s biocache-service.git
git svn clone http://ala-portal.googlecode.com/svn --trunk=trunk/biocache-store   --tags=tags --authors-file=./authors-file.out -s biocache-store.git

git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/alaspatial --tags=tags --authors-file=./authors-file.out -s alaspatial.git
git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/webportal --tags=tags --authors-file=./authors-file.out -s webportal.git
git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/layer-ingestion --tags=tags --authors-file=./authors-file.out -s layer-ingestion.git
git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/layers-service --tags=tags --authors-file=./authors-file.out -s layers-service
git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/layers-store --tags=tags --authors-file=./authors-file.out -s layers-store
```
