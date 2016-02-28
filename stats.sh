for i in `seq 1 10`
do
	echo $i
	python evaluator_code.py 2 | tail -3  >> statfile
done
