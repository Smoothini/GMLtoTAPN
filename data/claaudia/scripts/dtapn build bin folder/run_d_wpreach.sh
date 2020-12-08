echo "Batch 1: 200 to 1000 nodes"
for i in 10 20 30 40 50 60 70 80 90 100 200 300 400 500 600 700 800 900 1000
do
	echo "Running Disjoint_$i.."
	let tokens=$i*20
	{ time timeout -k 5 5s ./verifydtapn-linux64 -k $tokens -o 1 -m 0 -z Data/Disjoint/Disjoint_$i.txt Data/Disjoint/Disjoint_$i.xml Data/Disjoint/Disjoint_$i.q ; } 2> Results/Disjoint/Disjoint_$i.txt
	echo "Done!"
done
echo "Done batch 1"
