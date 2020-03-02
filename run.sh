#!/bin/bash
cd /usr/src
gunicorn -w 2 -b 0.0.0.0:6003 manager:app

