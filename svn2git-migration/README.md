### prepare
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

### migrate
1. in the web browser go to your github page and create a new repository, in this case: `ala-hub` `git@github.com:AtlasOfLivingAustralia/ala-hub.git`
2. `cd ~/src`
3. `git svn clone http://ala-hubs.googlecode.com/svn --trunk=trunk/ala-hub --tags=tags --authors-file=./authors-file.out -s ala-hub.git`
4. `cd ~/src/ala-hub.git`
5. `git for-each-ref refs/remotes/tags | cut -d / -f 4- | grep -v @ | while read tagname; do git tag "$tagname" "tags/$tagname"; git branch -r -d "tags/$tagname"; done`
6. `git for-each-ref refs/remotes | cut -d / -f 3- | grep -v @ | while read branchname; do git branch "$branchname" "refs/remotes/$branchname"; git branch -r -d "$branchname"; done`
7. `git remote add origin git@github.com:AtlasOfLivingAustralia/ala-hub.git`
8. `git push origin --all`
9. `git push origin --tags`

### test
* `cd ~/src`
* `git clone git@github.com:AtlasOfLivingAustralia/ala-hub.git`
* `cd ala-hub`
* `git remote show origin`
* etc.

### advanced

#### pre-processing/filtering the svn repo with svndumpfilter prior to importing to git/github

```BASH
# PROBLEM:
#
# bash-3.2$ git remote add origin git@github.com:AtlasOfLivingAustralia/ecodata.git
# bash-3.2$ git push origin --all
# Counting objects: 6216, done.
# Delta compression using up to 4 threads.
# Compressing objects: 100% (3094/3094), done.
# Writing objects: 100% (6216/6216), 5.01 MiB | 1.24 MiB/s, done.
# Total 6216 (delta 3011), reused 2195 (delta 907)
# remote: error: GH001: Large files detected.
# remote: error: Trace: f783125ec9eea68ed1cf360875aa0590
# remote: error: See http://git.io/iEPt8g for more information.
# remote: error: File target/stacktrace.log is 353.79 MB; this exceeds GitHub's file size limit of 100 MB
# remote: error: File target/stacktrace.log is 353.29 MB; this exceeds GitHub's file size limit of 100 MB
# To git@github.com:AtlasOfLivingAustralia/ecodata.git
# ! [remote rejected] master -> master (pre-receive hook declined)
# ! [remote rejected] trunk -> trunk (pre-receive hook declined)
# error: failed to push some refs to 'git@github.com:AtlasOfLivingAustralia/ecodata.git'
# bash-3.2$
#

# first take a dump
mbohun@firewolf:~/src> svnrdump dump http://ala-fieldcapture.googlecode.com/svn > svn_ala-fieldcapture.dump
#
# [...]
#
# * Dumped revision 1696.
# * Dumped revision 1697.
# * Dumped revision 1698.
# * Dumped revision 1699.
# mbohun@firewolf:~/src> cp svn_ala-fieldcapture.dump svn_ala-fieldcapture.dump.bak
# mbohun@firewolf:~/src> ls -lah svn_ala-fieldcapture.dump
# -rw-r--r-- 1 mbohun users 369M Jul 10 21:20 svn_ala-fieldcapture.dump

# use svndumpfilter to remove the 353.79mb stacktrace.log from the dump
mbohun@firewolf:~/src> svndumpfilter exclude --pattern "*/stacktrace.log" < svn_ala-fieldcapture.dump > svn_ala-fieldcapture-without-stacktrace_log.dump
# Excluding prefix patterns:
#    '/*/stacktrace.log'
# 
# Revision 0 committed as 0.
# Revision 1 committed as 1.
# Revision 2 committed as 2.
# Revision 3 committed as 3.
# Revision 4 committed as 4.
# Revision 5 committed as 5.
# Revision 6 committed as 6.
# [...]
#
# Revision 1696 committed as 1696.
# Revision 1697 committed as 1697.
# Revision 1698 committed as 1698.
# Revision 1699 committed as 1699.
# 
# Dropped 1 node:
#    '/trunk/ecodata/target/stacktrace.log'
# 
# mbohun@firewolf:~/src>

# a simplistic verification
mbohun@firewolf:~/src> ls -lah *.dump
# -rw-r--r-- 1 mbohun users 369M Jul 10 21:20 svn_ala-fieldcapture.dump
# -rw-r--r-- 1 mbohun users  15M Jul 11 10:29 svn_ala-fieldcapture-without-stacktrace_log.dump

# create a (tmp) svn repo to import/load our filtered version of our dump
mbohun@firewolf:~/src> svnadmin create svn_ala-fieldcapture-local

# load the filtered dump
mbohun@firewolf:~/src> svnadmin load ./svn_ala-fieldcapture-local < svn_ala-fieldcapture-without-stacktrace_log.dump

# svnserve the new repo
mbohun@firewolf:~/src> svnserve -d -r ./svn_ala-fieldcapture-local

# ...and we are ready to migrate to git/github
mbohun@firewolf:~/src> git svn clone svn://localhost --tags=tags --authors-file=./authors-file.out --trunk=trunk/ecodata -s ecodata.git

# ...resuming our interrupted migration:
mbohun@firewolf:~/src> cd ecodata.git
mbohun@firewolf:~/src/ecodata.git> git for-each-ref refs/remotes/tags | cut -d / -f 4- | grep -v @ | while read tagname; do git tag "$tagname" "tags/$tagname"; git branch -r -d "tags/$tagname"; done
mbohun@firewolf:~/src/ecodata.git> git for-each-ref refs/remotes | cut -d / -f 3- | grep -v @ | while read branchname; do git branch "$branchname" "refs/remotes/$branchname"; git branch -r -d "$branchname"; done
mbohun@firewolf:~/src/ecodata.git> git remote add origin git@github.com:AtlasOfLivingAustralia/ecodata.git
mbohun@firewolf:~/src/ecodata.git> git push origin --all
mbohun@firewolf:~/src/ecodata.git> git push origin --tags

# done :-)
```

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

git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/alaspatial      --tags=tags --authors-file=./authors-file.out -s alaspatial.git
git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/webportal       --tags=tags --authors-file=./authors-file.out -s webportal.git
git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/layer-ingestion --tags=tags --authors-file=./authors-file.out -s layer-ingestion.git
git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/layers-service  --tags=tags --authors-file=./authors-file.out -s layers-service.git
git svn clone http://alageospatialportal.googlecode.com/svn --trunk=trunk/layers-store    --tags=tags --authors-file=./authors-file.out -s layers-store.git

git svn clone http://ala-fieldcapture.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/FieldCapture -s fieldcapture.git                
git svn clone http://ala-fieldcapture.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ecodata      -s ecodata.git                     
                                                                                                                                                                     
git svn clone http://ala-mobile.googlecode.com/svn       --tags=tags --authors-file=./authors-file.out --trunk=trunk/ozatlas             -s ozatlas.git              
git svn clone http://ala-mobile.googlecode.com/svn       --tags=tags --authors-file=./authors-file.out --trunk=trunk/ozatlas-android     -s ozatlas-android.git      
git svn clone http://ala-mobile.googlecode.com/svn       --tags=tags --authors-file=./authors-file.out --trunk=trunk/userdetails         -s userdetails.git          
git svn clone http://ala-mobile.googlecode.com/svn       --tags=tags --authors-file=./authors-file.out --trunk=trunk/fieldcapture-mobile -s fieldcapture-mobile.git  
git svn clone http://ala-mobile.googlecode.com/svn       --tags=tags --authors-file=./authors-file.out --trunk=trunk/fielddata-android   -s fielddata-android.git    
git svn clone http://ala-mobile.googlecode.com/svn       --tags=tags --authors-file=./authors-file.out --trunk=trunk/fielddata-mobile    -s fielddata-mobile.git     
git svn clone http://ala-mobile.googlecode.com/svn       --tags=tags --authors-file=./authors-file.out --trunk=trunk/fielddata-proxy     -s fielddata-proxy.git      
git svn clone http://ala-mobile.googlecode.com/svn       --tags=tags --authors-file=./authors-file.out --trunk=trunk/mobile-auth         -s ozatlas-proxy.git

git svn clone http://ala-images.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/image-loader         -s image-loader.git            
git svn clone http://ala-images.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/image-service        -s image-service.git           
git svn clone http://ala-images.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/image-tiling-agent   -s image-tiling-agent.git      
git svn clone http://ala-images.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/image-utils          -s image-utils.git             
git svn clone http://ala-images.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/images-client-plugin -s images-client-plugin.git

git svn clone http://ala-portal.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-datacheck       -s sandbox.git
git svn clone http://ala-portal.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-name-matching   -s ala-name-matching.git
git svn clone http://ala-portal.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-names-generator -s ala-names-generator.git
git svn clone http://ala-portal.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/sds-webapp2         -s sds-webapp2.git
git svn clone http://ala-portal.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/sensitive-species   -s sensitive-species.git

git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-cas            -s ala-cas.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-cas-client     -s ala-cas-client.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-downloads      -s ala-downloads.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-fieldguide     -s ala-fieldguide.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-logger         -s ala-logger.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-logger-service -s ala-logger-service.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/bie-profile        -s bie-profile.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/bie-service        -s bie-service.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/bie-webapp2        -s bie-webapp2.git
git svn clone http://ala-bie.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/specieslist-webapp -s specieslist-webapp.git

git svn clone http://bhl-au-ftindex.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/bhl-ftindex-manage -s bhl-ftindex-manage.git
git svn clone http://bhl-au-ftindex.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/demo-app           -s bhl-demo-app.git
git svn clone http://bhl-au-ftindex.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ftindexer          -s bhl-ftindexer.git
git svn clone http://bhl-au-ftindex.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/solr-plugin        -s bhl-solr-plugin.git

git svn clone http://ala-expert.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/expert      -s ala-expert.git

git svn clone http://specimen-browser.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/specimenbrowser -s specimenbrowser.git

git svn clone http://ala-volunteer.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/volunteer-portal -s volunteer-portal.git

git svn clone http://ala-dashboard.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/dashboard -s dashboard.git

git svn clone http://ala-sightings.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/fielddata -s fielddata.git
git svn clone http://ala-sightings.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/sightings/trunk -s sightings.git

git svn clone http://ala-visualexplorer.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/tviewer -s tviewer.git

git svn clone http://ala.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/ala-web-theme -s ala-web-theme.git

git svn clone http://ala-alerts.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk -s alerts.git

git svn clone http://ala-regions.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk -s regions.git

git svn clone http://ala.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/apikey -s apikey.git
git svn clone http://ala.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/webapi -s webapi.git

# NOTE: ala-soils2sat had no tags, and the trunk was nested in trunk/ala-soils2sat/trunk
git svn clone http://ala-soils2sat.googlecode.com/svn --trunk=trunk/ala-soils2sat/trunk --authors-file=./authors-file.out -s ala-soils2sat.git

git svn clone http://alageospatialportal.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/actions  -s spatial-logger.git
git svn clone http://alageospatialportal.googlecode.com/svn --tags=tags --authors-file=./authors-file.out --trunk=trunk/database -s database.git
```
