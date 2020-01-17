#!/bin/bash

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  cd $HOME
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis"
  git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/makr3la/regression.git  gh-pages > /dev/null
  cd gh-pages
  rm -rf *
  cp -Rf $TRAVIS_BUILD_DIR/docs/build/html/* .
  git add -f .
  git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to gh-pages"
  git push -fq origin gh-pages > /dev/null
fi
