#!/bin/bash -eu

exec ${HOME}/.local/var/lib/WSGIBump/venv/bin/gunicorn \
-b unix:/public${HOME}/bump-jb2170-com-server \
--log-file - \
WSGIBump:App
