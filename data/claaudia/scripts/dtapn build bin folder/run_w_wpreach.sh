echo "Batch 1: 200 to 1000 nodes"
for i in 10 20 30 40
do
	echo "Running Worst_$i.."
	let tokens=$i*20
	{ time timeout -k 1s 1m ./verifydtapn-linux64 -k $tokens -o 1 -m 0 Data/Worst/Worst_$i.xml Data/Worst/Worst_$i.q ; } 2> Results/Worst/Worst_$i.txt 
	echo "Done!"
done
echo "Done batch 1"
