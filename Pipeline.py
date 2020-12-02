import utils.TAPNBuilder as TB
import utils.TestNets as TN
import utils.CSVMaker as CM

netsynth_results_path = "/home/escanor/Apps/netsynth/ltl_results/"
dtapn_results_path = "/home/escanor/Apps/verifydtapn-strategy_output/build/bin/Results/"

csv_results_path = "/home/escanor/GMLtoTAPN/data/csv/"
#  Current setup:
# Switches only for nodes present in the initial and final routing with different existing outgoing routes
#


# Write all the TAPN, JSON, LTL
# Missing only ltl for zootopo
def write_all_custom():
    TN.write_batch_to_file(10, 100, 10)
    TN.write_batch_to_file(100, 1000, 100)
    #TN.write_batch_to_file(10,100,6)
    #TN.write_batch_to_file(1000, 5000, 1000)

def write_benchmarks_csv():
    CM.make_csv("Disjoint", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Disjoint", netsynth_results_path, csv_results_path, "Netsynth")
    CM.make_csv("Shared", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Shared", netsynth_results_path, csv_results_path, "Netsynth")
    CM.make_csv("Worst", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Worst", netsynth_results_path, csv_results_path, "Netsynth")


#TB.write_all_to_file()
#write_all_custom()
write_benchmarks_csv()