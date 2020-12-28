echo "Batch 1: Disjoint"
data_path=data/synthethic_ltl
results_path=data/synthethic_results
for i in 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100
do
	echo "Running Disjoint_$i.."
	let tokens=$i*20
	{ time timeout -k 5 15m engines/./netsynth solve $data_path/Disjoint_$i.ltl ; } 2> $results_path/Disjoint_ltl_$i.txt
	echo "Done!"
done
echo "Done batch 1"

echo "Batch 2: Shared"
for i in 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460 480 500
do
	echo "Running Disjoint_$i.."
	let tokens=$i*20
	{ time timeout -k 5 15m engines/./netsynth solve $data_path/Shared_$i.ltl ; } 2> $results_path/Shared_ltl_$i.txt
	echo "Done!"
done
echo "Done batch 2"

echo "Batch 3: Worst"
for i in 4 7 10 13 16 19 22 25 50 75 100 125 150 175 200
do
	echo "Running Worst_$i.."
	let tokens=$i*20
	{ time timeout -k 5 15m engines/./netsynth solve $data_path/Worst_$i.ltl ; } 2> $results_path/Worst_ltl_$i.txt
	echo "Done!"
done
echo "Done batch 3"
