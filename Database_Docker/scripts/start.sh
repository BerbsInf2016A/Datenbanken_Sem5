#!/bin/bash
echo "Giving the database some time to start..."
sleep 60

python prepare_db.py
python importdata/import_data.py
echo "Finished import"
