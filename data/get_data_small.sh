#!/bin/bash
mkdir small
cd small
wget https://archive.org/download/stackexchange/math.stackexchange.com.7z
unar -D *.7z
rm -f *.7z
