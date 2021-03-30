#!/bin/bash

set -xe

usage(){
  echo "Usage: $0 {major|minor|patch} [--tag]"
  exit 1
}

if ! [ -x "$(command -v bumpversion)" ]; then
  if git branch --contains $(git rev-parse --verify HEAD) | grep -E 'master'; then
    bumpversion --tag --commit $1
  else
    echo "Only master tags can be tagged"
    exit 1
  fi
else
  bumpversion $1
fi
