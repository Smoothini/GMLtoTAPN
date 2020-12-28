./purge.sh
python3 Generate_Zoo.py
./solve_zoo_dtapn.sh
./solve_zoo_netsynth.sh
python3 CSV_Zoo.py

echo "DTapn and Netsynth Zoo Topology solving complete!"
