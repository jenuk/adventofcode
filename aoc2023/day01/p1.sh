sed -r "s/^[^0-9]*([0-9]).*([0-9])[^0-9]*$/\1\2/" input.txt | sed -r "s/^[^0-9]*([0-9])[^0-9]*$/\1\1/" | awk '{sum += $1} END {print sum}'
