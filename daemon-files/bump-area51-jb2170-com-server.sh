#!/bin/bash -eu

exec ${HOME}/.local/var/lib/FlaskBump/venv/bin/gunicorn \
-b unix:/public${HOME}/sockets/bump-area51-jb2170-com-server \
--log-file - \
FlaskBump:app
