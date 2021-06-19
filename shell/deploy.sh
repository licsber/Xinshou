#!/usr/bin/env zsh

SRC="/Users/licsber/PycharmProjects/Xinshou"
DST="tx:/home/licsber/services/xinshou"

rsync -avhv $SRC/xinshou/ $DST \
  --exclude "__pycache__/*" \
  --exclude "__pycache__" \
  --exclude ".DS_Store" \
  --delete-after

rsync -avhv $SRC/shell/run.sh $DST
rsync -avhv $SRC/requirements.txt $DST
