#!/bin/bash
set -e

# CLIENT HOME
#CLIENT_HOME="/data/$(hostname)/$(hostid)"
#export CLIENT_HOME=$CLIENT_HOME

# Create directories to be used by Plone
mkdir -p /data/filestorage /data/blobstorage /data/cache /data/log /data

# Activate the virtual environment.
# This ensures that all Python executables (like runwsgi) are found correctly.
. "${PLONE_HOME}/.venv/bin/activate"

# MAIN ENV Vars
[ -z ${SECURITY_POLICY_IMPLEMENTATION+x} ] && export SECURITY_POLICY_IMPLEMENTATION=C
[ -z ${VERBOSE_SECURITY+x} ] && export VERBOSE_SECURITY=off
[ -z ${DEFAULT_ZPUBLISHER_ENCODING+x} ] && export DEFAULT_ZPUBLISHER_ENCODING=utf-8
[ -z ${DEBUG_MODE+x} ] && export DEBUG_MODE=off

# ZODB ENV Vars
[ -z ${ZODB_CACHE_SIZE+x} ] && export ZODB_CACHE_SIZE=50000

MSG="Using ZEO configuration"
# Check ZEO variables
[ -z ${ZEO_SHARED_BLOB_DIR+x} ] && export ZEO_SHARED_BLOB_DIR=off
[ -z ${ZEO_READ_ONLY+x} ] && export ZEO_READ_ONLY=false
[ -z ${ZEO_CLIENT_READ_ONLY_FALLBACK+x} ] && export ZEO_CLIENT_READ_ONLY_FALLBACK=false
[ -z ${ZEO_STORAGE+x} ] && export ZEO_STORAGE=1
[ -z ${ZEO_CLIENT_CACHE_SIZE+x} ] && export ZEO_CLIENT_CACHE_SIZE=128MB
[ -z ${ZEO_DROP_CACHE_RATHER_VERIFY+x} ] && export ZEO_DROP_CACHE_RATHER_VERIFY=false

# Handle CORS
${PLONE_HOME}/.venv/bin/python  /app/scripts/cors.py

if [[ "$1" == "start" ]]; then
  echo $MSG
  exec ${PLONE_HOME}/.venv/bin/runwsgi -v /app/etc/zope.ini config_file=zeo.conf
else
  exec "$@"
fi
