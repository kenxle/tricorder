#!/bin/sh
# Renders tricorder_promo.mp4 (adapted from the Quote Desk promo's render_v2.sh).
# Frames come from promo.html via capture.js, the voiceover from vo.py, the music from music.py.
# Usage: sh render.sh <frames dir outside the repo> <captures dir from capture_app.py>
# Set RERENDER=1 to redraw frames that already exist.
set -e
cd "$(dirname "$0")"
F="${1:?frames dir}"
C="${2:?captures dir}"
[ -f "$F/f1349.jpg" ] && [ -z "$RERENDER" ] || node capture.js frames "$F" "$C"
# Voice start times in ms match LINES in vo.py.
ffmpeg -y -v error -i audio/music.wav \
  -i audio/vo1.wav -i audio/vo2.wav -i audio/vo3.wav -i audio/vo4.wav -i audio/vo5.wav -i audio/vo6.wav -i audio/vo7.wav -i audio/vo8.wav -i audio/vo9.wav \
  -filter_complex "\
[1]adelay=300|300[a1];[2]adelay=5700|5700[a2];[3]adelay=10500|10500[a3];[4]adelay=16600|16600[a4];[5]adelay=19800|19800[a5];\
[6]adelay=25600|25600[a6];[7]adelay=28800|28800[a7];[8]adelay=35600|35600[a8];[9]adelay=40900|40900[a9];\
[a1][a2][a3][a4][a5][a6][a7][a8][a9]amix=inputs=9:normalize=0,aformat=channel_layouts=stereo,asplit[vo][vokey];\
[0]volume=0.40[m];[m][vokey]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=350[md];\
[vo][md]amix=inputs=2:normalize=0,volume=5dB,alimiter=limit=0.95,atrim=0:45[out]" \
  -map "[out]" -ar 48000 audio/mix.wav
ffmpeg -y -v error -framerate 30 -i "$F/f%04d.jpg" -i audio/mix.wav \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -t 45 -movflags +faststart tricorder_promo.mp4
ffprobe -v error -show_entries format=duration,size -of default=nw=1 tricorder_promo.mp4
