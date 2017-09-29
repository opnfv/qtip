#!/usr/bin/env bash

mongoimport --db test_results_collection --collection pods --drop --file pod.json
mongoimport --db test_results_collection --collection projects --drop --file project.json
mongoimport --db test_results_collection --collection cases --drop --file cases.json --jsonArray
