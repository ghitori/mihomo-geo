#!/bin/bash

DOMAIN="./out/domain"
IPCIDR="./out/ipcidr"
CORE="./mihomo"

for i in $DOMAIN/*.yaml
do
  $CORE convert-ruleset domain yaml ${i%.*}.yaml ${i%.*}.mrs
done
for i in $IPCIDR/*.yaml
do
  $CORE convert-ruleset ipcidr yaml ${i%.*}.yaml ${i%.*}.mrs
done
exit
