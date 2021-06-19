#!/usr/bin/env bash

cd /home/licsber/services || exit

export PYTHONPATH=/home/licsber/services/xinshou
/home/licsber/miniconda3/envs/xinshou/bin/gunicorn -b 10.0.8.8:30444 "xinshou:create_app()"
