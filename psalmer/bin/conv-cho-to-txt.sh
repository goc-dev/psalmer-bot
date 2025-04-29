#!/bin/bash

# Goal: convert cho-file into txt

source ./env.sh
HYMNAL_DIR=$1
HYMN_FILE_NAME=$2
CHORDPRO_OPT=$3

HYMN_CHO=$HYMNAL_LIB_HOME_DIR/cho/$HYMNAL_DIR/$HYMN_FILE_NAME.cho
HYMN_TXT=$HYMNAL_LIB_HOME_DIR/txt/$HYMNAL_DIR/$HYMN_FILE_NAME.txt

echo "Hymnal: $HYMNAL_DIR"
echo "Source: $HYMN_CHO"
echo "Target: $HYMN_TXT"

chordpro $HYMN_CHO -o $HYMN_TXT $CHORDPRO_OPT

cat $HYMN_TXT