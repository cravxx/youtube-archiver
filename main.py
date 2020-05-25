import argparse
import os
import re
import sys
from fnmatch import fnmatch
from signal import SIGTERM
from subprocess import PIPE, Popen

from PathType import PathType

parser = argparse.ArgumentParser( description = 'youtube archiver' )
parser.add_argument( '-a', '--archive', type = PathType( exists = True, type = 'dir' ),
                     help = "set the archive location containing subfolders with init files" )

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit( 0 )

_ARCHIVE = os.getcwd() if args.archive is None else args.archive

def process_channel(path, channel):
    process = Popen(["youtube-dl", "--ignore-errors", channel], stdout=PIPE, stderr=PIPE, preexec_fn=os.setsid,
                    cwd=path)

    print(f"checking channel {channel}")
    count = 0
    for line in process.stdout:
        download_count = re.search("Downloading video (\d+) of (\d+)", line.decode("unicode_escape"), re.UNICODE)
        if download_count:
            count = int(download_count.group(1))
            print(f"    processing {download_count.group(1)} of {download_count.group(2)}")

        already_downloaded = re.search("has already been downloaded and merged", line.decode("unicode_escape"),
                                       re.UNICODE)
        if already_downloaded:
            os.killpg(os.getpgid(process.pid), SIGTERM)

    if count is 1:
        print(f"finished updating archive {channel}, no new videos downloaded")
    else:
        print(f"finished updating archive {channel}, {str(count - 1)} videos downloaded")

for dirpath, dirnames, filenames in os.walk(_ARCHIVE):
    for matched_file in [f for f in filenames if fnmatch(f, "*.archive")]:
        channel = [line.rstrip('\n') for line in open(os.path.join(dirpath, matched_file), "r").readlines()]
        assert len(channel) is 1
        process_channel(dirpath, channel[0])

print("finished scanning subdirectories for .archive files")