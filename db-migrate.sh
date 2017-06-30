#!/usr/bin/env bash

pushd .
cd ./backend/skael/
python3 migrate.py db upgrade
popd
