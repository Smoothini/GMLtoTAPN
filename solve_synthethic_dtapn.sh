echo "Batch 1: Disjoint"
data_path=data/synthethic_dtapn
results_path=data/synthethic_results
for i in 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 4000 6000 8000 10000 12000 14000 16000 18000 20000
do
	echo "Running Disjoint_$i.."
	let tokens=$i*20
	{ time timeout -k 5 15m engines/./verifydtapn-linux64 -k $tokens -o 1 -m 0 -z $data_path/Disjoint_$i.txt $data_path/Disjoint_$i.xml $data_path/Disjoint_$i.q ; } 2> $results_path/Disjoint_dtapn_$i.txt
	echo "Done!"
done
echo "Done batch 1"


echo "Batch 2: Shared"
for i in 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 460 480 500
do
	echo "Running Shared_$i.."
	let tokens=$i*20
	{ time timeout -k 5 15m engines/./verifydtapn-linux64 -k $tokens -o 1 -m 0 -z $data_path/Shared_$i.txt $data_path/Shared_$i.xml $data_path/Shared_$i.q ; } 2> $results_path/Shared_dtapn_$i.txt
	echo "Done!"
done
echo "Done batch 2"

echo "Batch 3: Worst"
for i in 4 7 10 13 16 19 22 
do
	echo "Running Worst_$i.."
	let tokens=$i*20
	{ time timeout -k 5 15m engines/./verifydtapn-linux64 -k $tokens -o 1 -m 0 -z $data_path/Worst_$i.txt $data_path/Worst_$i.xml $data_path/Worst_$i.q ; } 2> $results_path/Worst_dtapn_$i.txt
	echo "Done!"
done
echo "Done batch 3"
