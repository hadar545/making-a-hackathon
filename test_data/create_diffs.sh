#!/bin/bash

while read git_repo_path <&3 && read sha_line <&4; do
	git clone $git_repo_path
	dir_name=$(basename $git_repo_path | cut -f 1 -d".")
	cd $dir_name
	jul_sha=$(echo $sha_line|awk '{print $1}')
	jun_sha=$(echo $sha_line|awk '{print $2}')
	git diff -U0 $jul_sha $jun_sha > ../"${dir_name}_diff.txt"
	cd ..
done 3<URLs.txt 4<sha.txt

