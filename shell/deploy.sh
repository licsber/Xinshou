#!/usr/bin/env zsh

rsync -avhv /Users/licsber/PycharmProjects/Xinshou/xinshou/ shh.licsber.site:/home/licsber/xinshou \
  --exclude "__pycache__/*" --exclude "__pycache__" --delete-after

rsync -avhv /Users/licsber/PycharmProjects/Xinshou/requirements.txt shh.licsber.site:/home/licsber/xinshou
