#!/bin/bash

GEOSITE="./sing-geosite"
GEOIP="./sing-geoip"
CORE="./sing-box"

for i in $GEOSITE/*.srs
do
  $CORE rule-set decompile ${i%.*}.srs -o ${i%.*}.json
done
for i in $GEOIP/*.srs
do
  $CORE rule-set decompile ${i%.*}.srs -o ${i%.*}.json
done
exit
