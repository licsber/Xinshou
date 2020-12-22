#!/usr/bin/env zsh

SRC="/Users/licsber/PycharmProjects/Xinshou"
DST="shh.licsber.site:/home/licsber/xinshou"

rsync -avhv $SRC/xinshou/ $DST \
  --exclude "__pycache__/*" --exclude "__pycache__" --delete-after

rsync -avhv $SRC/requirements.txt $DST
chmod +x $SRC/shell/run.sh
rsync -avhv $SRC/shell/run.sh $DST/..
