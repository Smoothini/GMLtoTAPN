./purge.sh
python3 Generate_Synthethic.py
./solve_synthethic_dtapn.sh
./solve_synthethic_netsynth.sh
python3 CSV_Synthethic.py

echo "DTapn and Netsynth Synthethic solving complete!"
