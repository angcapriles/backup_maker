#!/usr/bin/python

# Import required python libraries

import os
import time
import datetime
import pipes
from pathlib import Path

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.

DB_HOST = 'localhost' 
DB_USER = 'root'
DB_USER_PASSWORD = '123456'
#DB_NAME = '/backup/dbnameslist.txt'
DB_NAME = 'honda'
BACKUP_PATH = '/Users/MacBook/Documents/lab/backup_maker/backups'
MAX_BACKUP_AMOUNT = 2

# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')

# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(BACKUP_PATH)
except:
    os.mkdir(BACKUP_PATH)

backup_directory_path = Path(BACKUP_PATH)

# Validate the backup directory exists and create if required
backup_directory_path.mkdir(parents=True, exist_ok=True)

# Get the amount of past backup zips in the backup directory already
existing_backups = [
    x for x in backup_directory_path.iterdir()
    if x.is_file() and x.suffix == '.sql' and x.name.startswith('db-backup-')
]

# Enforce max backups and delete oldest if there will be too many after the new backup
oldest_to_newest_backup_by_name = list(sorted(existing_backups, key=lambda f: f.name))
while len(oldest_to_newest_backup_by_name) >= MAX_BACKUP_AMOUNT:  # >= because we will have another soon
    backup_to_delete = oldest_to_newest_backup_by_name.pop(0)
    backup_to_delete.unlink()

# Starting actual database backup process.
db = DB_NAME
dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(BACKUP_PATH) + "/db-backup-" + DATETIME + ".sql"
os.system(dumpcmd)
gzipcmd = "gzip " + pipes.quote(BACKUP_PATH) + "/" + db + ".sql"
os.system(gzipcmd)

print ("")
print ("Backup script completed")
print ("Your backups have been created in '" + BACKUP_PATH + "' directory")