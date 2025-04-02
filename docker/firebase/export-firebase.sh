#!/bin/sh

WORKSPACE=/opt/firebase
EXPORT_TO=${WORKSPACE}/exports/data


cd ${WORKSPACE}

firebase emulators:export ./exports/data -f

#echo "$0 trried to export at $(date)" >>./exports/log
