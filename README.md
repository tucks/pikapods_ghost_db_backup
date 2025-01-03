# pikapods_ghost_db_backup
An docker container to automate backups of the Ghost database from the pikapod

Tested with AdminerEvo 4.8.4

## How to Build and Use the Docker
Building
```
cd /path/to/gitrepo
docker build -t pikapod-ghost-db-bkup .
```

Use
```
export PP_USERNAME=myusername
export PP_PASSWORD=mypassword
export PP_DATABASE=mydatabase
```

Optional:
```
export PP_BACKUPNAME=mybackupname
```

Creating a backup
```
docker run --rm -e PP_URL=$PP_URL -e PP_USERNAME=$PP_USERNAME -e PP_PASSWORD=$PP_PASSWORD -e PP_DATABASE=$PP_DATABASE -e PP_BACKUPNAME=$PP_BACKUPNAME -v /dir/to/store/backups/in:/dl pikapod-ghost-db-bkup
```

## Results
After running, the backups are available locally:
```
user@mypc:$ ls -1 /dir/to/store/backups/in/
20250103-164622_mybackupname.sql.gz
20250103-164649_p12345.sql.gz
20250103-165628_p12345.sql.gz
20250103-165649_p12345.sql.gz
```

License: Apache 2.0

NOTICE must be included with any forks/derivative works.

