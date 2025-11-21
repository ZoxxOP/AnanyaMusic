#!/bin/bash
# ⚙️ Step 1: Save original file timestamps before orphan reset
echo "Saving timestamps..."
find . -type f -not -path "./.git/*" -printf '%T@ %p\n' > .timestamps.txt

# ⚙️ Step 2: Create orphan branch and make fresh commit
echo "Creating orphan branch..."
git checkout --orphan new-main
git add .
git commit -m "✨ Fresh start for AnanyaMusic"

# ⚙️ Step 3: Delete old main and rename new branch
echo "Switching branches..."
git branch -D main
git branch -m main

# ⚙️ Step 4: Restore file timestamps
echo "Restoring timestamps..."
while read -r line; do
    ts=$(echo "$line" | cut -d' ' -f1)
    file=$(echo "$line" | cut -d' ' -f2-)
    if [ -f "$file" ]; then
        touch -d "@$ts" "$file"
    fi
done < .timestamps.txt

# ⚙️ Step 5: Cleanup
rm .timestamps.txt
echo "✅ File timestamps restored successfully."

# ⚙️ Step 6: Push forcefully
git push origin main --force

