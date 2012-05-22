#!/bin/bash
  set -e
  LOGFILE=/var/log/gunicorn/hello.log
  LOGDIR=$(dirname $LOGFILE)
  NUM_WORKERS=3
  # user/group to run as
  USER=hacker
  GROUP=hacker
  cd /home/hacker/django-bootstrap-gunicorn-starter/hellodjango
  . ../venv/bin/activate
  test -d $LOGDIR || mkdir -p $LOGDIR
  exec /home/hacker/django-bootstrap-gunicorn-starter/venv/bin/gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug\
--log-file=$LOGFILE 2>>$LOGFILE
