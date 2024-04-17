#!/bin/bash

set -x

s=0
e=9

for i in $(seq $s $e); do
	echidna src/StaxExploit.sol --contract StaxExploit --config local.yaml --workers 4 | tee /tmp/local-$i.txt
	echidna src/StaxExploit.sol --contract StaxExploit --config remote.yaml --workers 4 | tee /tmp/remote-$i.txt
done