# How branches work 

This is a repo for a better understanding of git.

## basic cmd

```bash
git clone git@gitlab:repo-link # getting the repo
git add -A # add ALL new changes
git commit -m "some comment that tells me what this is about "
git pull # pull down new changes
git push # push up you new changes from current branch and remote
git log # to see some more ingo about commits
git status # shows info about changes
git reset --hard # removes all things to the latest commit that is local
```

## [branches](https://www.youtube.com/watch?v=oPpnCh7InLY&t)

![img](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.stack.imgur.com%2Fu8C1x.png&f=1&nofb=1)

### Major branches
* master || main
* develop || dev
* feature   

```bash
git checkout branch-name # go to branch
git checkout -b new-branch-name # go to new branch
git push --set-upstream remote-name new-branch-name # push new branch
git branch -d branch-name # delete branch locally
git push origin --delete branch-name # delete branch remotely (gitlab, github)
```

## [Remotes](https://www.youtube.com/watch?v=lR_hYwCAaH4)
```bash
git remote -v # shows remotes that are available
git remote add remote-name git@gitlab:repo-link # creates a new remote, link can also be fork link
git remote remove remote-name  # removes the remote
git pull remote-name branch-name # pull down new changes from that remote

```

## [Semantic Versioning and tags](https://semver.org/)
For new versions we want to create a new tag and ensure that the new release has a version number and we want to know how big of a changes that is.
```
MAJOR.MINOR.PATCH
Ex v3.2.1
```
* MAJOR version when you make incompatible API changes,

* MINOR version when you add functionality in a backwards compatible manner, and

* PATCH version when you make backwards compatible bug fixes.
