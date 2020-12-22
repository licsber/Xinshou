#!/usr/bin/env bash

/home/licsber/miniconda3/envs/xinshou/bin/gunicorn -b 127.0.0.1:30443 "xinshou:create_app()"
