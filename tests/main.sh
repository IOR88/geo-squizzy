#!/usr/bin/env bash

# Run all geosquizzy tests (unittests, integrationtests)
# it search for all python files which have 'test' in its name and execute them as main
TESTS=( $(find -type f -name "*test*.py") )

for test_file in "${TESTS[@]}"
    do
        echo -e "\e[32mTEST execution for: $test_file\e[0m \n"
        python "$test_file"
    done