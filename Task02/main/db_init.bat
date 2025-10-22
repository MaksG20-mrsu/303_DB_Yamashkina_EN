#!/bin/bash
python main.py
sqlite3 movies_rating.db < db_init.sql
