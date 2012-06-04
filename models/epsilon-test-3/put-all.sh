#!/bin/bash

for fname in nextgen/model*.json 
do
  curl -X POST http://localhost:5984/lab_development -H "Content-Type: application/json" -d@$fname
done
