#!/bin/sh

THIS_DIR=$(dirname $(readlink -f $0))

# move secret to auth.token
echo $AUTH_TOKEN > ${THIS_DIR}/auth.token

# gunicorn -w1 -b "0.0.0.0:5050" "countit_app:app"
python countit_app.py