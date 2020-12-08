echo "Batch 1"
for i in 10 20 30 40 50 60 70 80 90 100 200 300 400 500 600 700 800 900 1000
do
	echo "Running Worst_$i.."
	{ time timeout -k 1s 1m ./netsynth solve ltl/Worst_$i.ltl ; } 2> ltl_results/Worst/Worst_$i.txt
	echo "Done!"
done
echo "Done batch 1"
