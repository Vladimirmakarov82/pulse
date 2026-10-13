#!/usr/bin/env bash
# Автообновление сайта aiventurebuilder.xyz: раз в минуту тянет ветку site-aiventurebuilder.
set -e
D=/var/www/aiventurebuilder
B=site-aiventurebuilder
R=https://github.com/Vladimirmakarov82/pulse.git
if [ ! -d "$D/.git" ]; then git clone -q --depth 1 -b "$B" "$R" "$D"; else cd "$D" && git fetch -q --depth 1 origin "$B" && git reset -q --hard "origin/$B"; fi
