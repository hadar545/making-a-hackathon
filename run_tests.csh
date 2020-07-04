#!/bin/csh -f

#SBATCH --mem=32GB
#SBATCH --time=6:00:00

chmod u+x test.py
touch acc.txt
touch names.txt
touch __init__.py
foreach f (*.zip)
	set s=$f:t:r
	echo $s >> names.txt
	mkdir $s
	cp $f $s/
	cd $s/
	unzip $f && rm -f $f
	cd ../
	virtualenv "${s}_venv" --python python3.7
	source "${s}_venv"/bin/activate.csh
	if (-d $s/task1) then
		set m=task1
		cd $s/$m/src/
	else
		set m=task2
		cd $s/$m/src/
	pip install -r requirements.txt
	pip install numpy
	pip install pandas
	set res=`python ../../../get_submission_stats.py ${m} ${s} `
	foreach user (`cut -d"," -f 1  ../../USERS.txt`)
		echo "${user},${res}" >> ../../../acc.txt
		end
	deactivate
	rm -rf "${s}_venv" $s __pycache__
	end
