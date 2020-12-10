import utils.TAPNBuilder as TB
import utils.TestNets as TN
import utils.DTAPNBuilder as DB
import utils.CSVMaker as CM
import utils.LtLBuilder as LTL

netsynth_results_path = "/home/escanor/Apps/netsynth/ltl_results/"
dtapn_results_path = "/home/escanor/Apps/verifydtapn-strategy_output/build/bin/Results/"

csv_results_path = "/home/escanor/GMLtoTAPN/data/csv/"
#  Current setup:
# Switches only for nodes present in the initial and final routing with different existing outgoing routes
#


# Write all the TAPN, JSON, LTL, DTAPN
# Missing only ltl for zootopo
def write_all_custom():
    #TN.write_batch_to_file(10, 100, 10)
    #TN.write_batch_to_file(100, 1000, 100)

    for i in range(10, 110, 10):
        DB.build_composed_model(TN.generate_disjoint(i), "data/claaudia/disjoint_wpreach_dtapn")

        DB.build_composed_model(TN.generate_shared(i), "data/claaudia/shared_wpreach_dtapn")

        DB.build_composed_model(TN.generate_worst(i), "data/claaudia/worst_wpreach_dtapn")

    for i in range(100, 1100, 100):
        DB.build_composed_model(TN.generate_disjoint(i), "data/claaudia/disjoint_wpreach_dtapn")

        DB.build_composed_model(TN.generate_shared(i), "data/claaudia/shared_wpreach_dtapn")

        DB.build_composed_model(TN.generate_worst(i), "data/claaudia/worst_wpreach_dtapn")

    for i in range(2000, 6000, 1000):
        DB.build_composed_model(TN.generate_disjoint(i), "data/claaudia/disjoint_wpreach_dtapn")

def write_custom():
    #for i in range(1000,5500,500):
     #   DB.build_composed_model(TN.generate_disjoint(i), "data/claaudia/disjoint500_5000")
    #for i in range(100,430,30):
     #   DB.build_composed_model(TN.generate_shared(i), "data/claaudia/shared100_400")
    for i in range(10, 22, 2):
        DB.build_composed_model(TN.generate_worst(i), "data/claaudia/worst10_20")




def write_benchmarks_csv():
    CM.make_csv("Disjoint", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Disjoint", netsynth_results_path, csv_results_path, "Netsynth")
    CM.make_csv("Shared", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Shared", netsynth_results_path, csv_results_path, "Netsynth")
    CM.make_csv("Worst", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Worst", netsynth_results_path, csv_results_path, "Netsynth")


write_custom()
#write_benchmarks_csv()
