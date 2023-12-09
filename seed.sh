#!/bin/bash
rm -rf tunaapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations tunaapi
python3 manage.py migrate tunapid
python3 manage.py loaddata artists
python3 manage.py loaddata genres
python3 manage.py loaddata song_genres
python3 manage.py loaddata songs
