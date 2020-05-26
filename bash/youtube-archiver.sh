CWD="$PWD"
if [ ! -z "$1" ]; then
    CWD="$1"
fi
cd "$CWD"
find . -name "*.archive" |
while read file; do
    cd "$CWD"
    CURRENT=0
    TOTAL=0
    CHANNEL=$(head -n 1 "$file")
    cd "$(dirname "$file")"
    youtube-dl --ignore-errors "$CHANNEL" 2>/dev/null | while read line; do
        if CURRENT_VIDEO=$(pcregrep -o1 '(\d+)\s\w+\s(\d+)' <<< $line); then
            CURRENT=$CURRENT_VIDEO
            #only need to grab total once per loop
            if [ $TOTAL -eq "0" ]; then
                TOTAL=$(pcregrep -o2 '(\d+)\s\w+\s(\d+)' <<< $line)
            fi
            echo "processing ${CURRENT} of ${TOTAL}"
        fi
        grep -Po "has already been downloaded and merged" <<< $line >/dev/null
        if [ "$?" -eq "0" ]; then
            if [ $CURRENT -gt "1" ]; then
                echo "finished updating archive ${CHANNEL}, ${$[current + 1]} videos added"
            else
                echo "finished updating archive ${CHANNEL}, no new videos downloaded"
            fi
            break
        fi
    done
done
echo "finished scanning subdirectories for .archive files"
