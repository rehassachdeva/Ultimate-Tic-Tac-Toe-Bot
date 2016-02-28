for i in `seq 1 50`
do
	python evaluator_code.py 1 | tail -50  >> statfile
done
