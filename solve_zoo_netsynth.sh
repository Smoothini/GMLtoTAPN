echo "Topology Zoo solving using Netsynth"
data_path=data/zoo_ltl
results_path=data/zoo_results
for raw in $data_path/*.ltl
do
	echo "Running $raw"
	file=${raw:13:-4}
	{ time timeout -k 5s 10m engines/./netsynth solve $data_path/$file.ltl; } 2> $results_path/${file}_netsynth.txt
	echo "Done!"
done
echo "Done running Topology Zoo with Netsynth!"
