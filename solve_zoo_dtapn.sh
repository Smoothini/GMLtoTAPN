echo "Topology Zoo solving using DTapn"
data_path=data/zoo_dtapn
results_path=data/zoo_results
for raw in $data_path/*.xml
do
	echo "Running $raw"
	file=${raw:15:-4}
	let tokens=2000
	{ time timeout -k 5s 10m engines/./verifydtapn-linux64 -k $tokens -o 1 -m 0 -z $data_path/$file.txt $data_path/$file.xml $data_path/$file.q ; } 2> $results_path/${file}_dtapn.txt
	echo "Done!"
done
echo "Done running Topology Zoo with DTapn!"

