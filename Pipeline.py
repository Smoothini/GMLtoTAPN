import utils.TAPNBuilder as TB
import utils.TestNets as TN
import utils.DTAPNBuilder as DB
import utils.CSVMaker as CM
import utils.LtLBuilder as LTL
import utils.JsonBuilder as JB

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

    #for i in range(100, 2200, 100):
     #   DB.build_composed_model(TN.generate_disjoint(i), "data/claaudia/disjoint")

    #for i in range(120, 580, 20):
     #   DB.build_composed_model(TN.generate_shared(i), "data/claaudia/shared")

    #for i in range(25, 225, 25):
     #   DB.build_composed_model(TN.generate_worst(i), "data/claaudia/worst")
    #for i in range(300, 1100, 100):
     #   DB.build_composed_model(TN.generate_worst(i), "data/claaudia/worst")
    #for i in range(2000, 6000, 1000):
     #   DB.build_composed_model(TN.generate_worst(i), "data/claaudia/worst")

    #for i in range(4, 51, 3):
     #   DB.build_composed_model(TN.generate_worst(i), "data/claaudia/worst", negative=True)
    scale = 50
    #TB.write_zoo_to_file("Eenet", 2)
    #TN.make_worst(16)
    #LTL.make_ltl_zoo("Aarnet")
    #LTL.make_all_zoo()
    #LTL.make_ltl_zoo_scale("Eenet", 2)
    #TB.write_all_to_file(scale)
    #LTL.make_all_zoo_scale(scale)
    #TB.write_scaled_tapn_to_file("Eenet", 2)
    #TB.write_zoo_to_file("Eenet",2)



def write_benchmarks_csv():
    CM.make_csv("Disjoint", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Disjoint", netsynth_results_path, csv_results_path, "Netsynth")
    CM.make_csv("Shared", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Shared", netsynth_results_path, csv_results_path, "Netsynth")
    CM.make_csv("Worst", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Worst", netsynth_results_path, csv_results_path, "Netsynth")


write_all_custom()
#write_benchmarks_csv()
