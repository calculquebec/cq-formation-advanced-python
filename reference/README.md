# cq-formation-advanced-python
Advanced and Parallel Python workshop reference material.

In your own branch (example: mcgill), add a subtree pointing to the gh-pages branch (only once):

~~~
git subtree add --prefix reference git@github.com:calculquebec/cq-formation-advanced-python.git gh-pages --squash
~~~

Each time you want to update the gh-pages branch, do it from your mcgill branch:

~~~
git checkout mcgill
git pull
git subtree pull --prefix reference git@github.com:calculquebec/cq-formation-advanced-python.git gh-pages

cp -r reference/<old dir> reference/<new dir>
... make your changes ...

git add reference/<new dir>
git commit
git push
git subtree push --prefix reference git@github.com:calculquebec/cq-formation-advanced-python.git gh-pages
~~~

Web site will be available at http://calculquebec.github.io/cq-formation-advanced-python/<new dir>/
