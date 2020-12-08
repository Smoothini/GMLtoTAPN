echo "Batch 1: 200 to 1000 nodes"
for i in 10 20 30 40 50 60 70 80 90 100 200 300 400 500 600 700 800 900 1000
do
	echo "Running Disjoint_$i.."
	{ time timeout -k 5 3s ./netsynth solve ltl/Disjoint_$i.ltl ; } 2> ltl_results/Disjoint/Disjoint_$i.txt 
	echo "Done!"
done
echo "Done batch 1"
