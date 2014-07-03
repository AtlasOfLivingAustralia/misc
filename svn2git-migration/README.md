
1. in the web browser go to your github page and create a new repository, in this case: `ala-hub` `git@github.com:AtlasOfLivingAustralia/ala-hub.git`
2. `cd ~/src`
3. `git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/ala-hub --tags=tags --authors-file=./authors-file.out -s ala-hub.git`
4. `cd ~/src/ala-hub.git`
5. `git for-each-ref refs/remotes/tags | cut -d / -f 4- | grep -v @ | while read tagname; do git tag "$tagname" "tags/$tagname"; git branch -r -d "tags/$tagname"; done`
6. `git for-each-ref refs/remotes | cut -d / -f 3- | grep -v @ | while read branchname; do git branch "$branchname" "refs/remotes/$branchname"; git branch -r -d "$branchname"; done`
7. `git remote add origin git@github.com:AtlasOfLivingAustralia/ala-hub.git`
8. `git push origin --all`
9. `git push origin --tags`
10. ... and test git clone from your github repo:

* `cd ~/src`
* `git clone git@github.com:AtlasOfLivingAustralia/ala-hub.git`
* `cd ala-hub`
* `git remote show origin`
* etc.

---

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
```
