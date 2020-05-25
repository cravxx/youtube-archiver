# youtube-archiver

I wanted to:
- have a single directory for all youtube channels I wished to archive
- nothing hardcoded, and easy to add channels to 
- hands off operation

The only thing the script needs to run is the location of the root archive directory, the rest of the information is determined by user-created subfolders and `init.archive` files containing the channel link.

My workflow is to only rely on this script to *update* the archives: I always do an initial download of channels directly with youtube-dl as to monitor it closely. This is why there is no logic to check whether the complete archive actually exists or not, it simply exits once youtube-dl reports that a file has already been downloaded.

This can be easily added as a systemd service:

```
[Unit]
Description=Runs youtube archiver
Wants=youtube-archiver.timer

[Service]
ExecStart=/usr/bin/python3.7 $clone-location/main.py -a $archive-location
WorkingDirectory=$clone-location

[Install]
WantedBy=multi-user.target
```

```
[Unit]
Description=Runs youtube archiver every 24 hours
Requires=youtube-archiver.service

[Timer]
Unit=youtube-archiver.service
OnBootSec=15min
OnUnitInactiveSec=24h

[Install]
WantedBy=timers.target
```

