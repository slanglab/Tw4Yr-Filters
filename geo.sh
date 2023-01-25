#!/bin/sh

lz4cat $1 | jq -c 'select(.geo != null)' > $2

