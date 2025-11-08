#!/bin/zsh

if [[ "$1" == "coverage" ]]; then
    python3 -m coverage run -m unittest discover -s test
    python3 -m coverage report -m
else
    python3 -m unittest discover -s test
fi
