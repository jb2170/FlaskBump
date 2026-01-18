#!/usr/bin/env -S bash -eu

source ./venv/bin/activate

exec gunicorn \
-b unix:/public${HOME}/sockets/bump-area51-jb2170-com-server \
--log-file - \
FlaskBump:app
