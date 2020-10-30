# Git Guideline of this Repository (developers only)

## Stucture
branch - main (for version control, push only v1, v2,...)

branch - dev (for daily collaborate, keep teamwork up-to-date)

branch - <developer_branch> (for individual use)

## Setup
get remote repository and connect with local
```
# clone the remote repository, you will have main, origin/main & origin/dev
git clone <SSH>
# generate local dev branch
git checkout -b dev
# connect local dev and origin/dev
git branch --set-upstream-to=origin/dev dev
```
generate your own local branch
```
git checkout -b <developer_branch>
```

## Working with Git
Everytime when start to work, keep dev up-to-date.
```
# go to local dev
git checkout dev
# update dev with origin/dev, pull = fetch + merge
git pull
```
Update your own branch
```
# go to local <developer_branch>
git checkout <developer_branch>
# update <developer_branch> with dev
git merge dev
```
After some modification, commit your work
```
# commit in <developer_branch>
git add .
git commit -m "<message>"
# go to dev branch
git checkout dev
git merge <developer_branch>
# commit to origin/dev
git add .
git commit -m "<message>"
git push
```