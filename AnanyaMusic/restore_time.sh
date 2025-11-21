#!/bin/bash
echo "♻️  Restoring original timestamps..."
while read -r line; do
    ts=$(echo "$line" | cut -d' ' -f1)
    file=$(echo "$line" | cut -d' ' -f2-)
    if [ -f "$file" ]; then
        touch -d "@$ts" "$file"
    fi
done < .timestamps_backup.txt
echo "✅ All timestamps restored to original values."
