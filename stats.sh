for i in `seq 1 5`
do
	python evaluator_test.py 1 | tail -2 | head -1 >> statfile
done
