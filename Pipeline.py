import utils.TAPNBuilder as TB
import utils.TestNets as TN
import utils.DTAPNBuilder as DB
import utils.CSVMaker as CM
import utils.LtLBuilder as LTL
import utils.JsonBuilder as JB

netsynth_results_path = "/home/escanor/Apps/netsynth/ltl_results/"
dtapn_results_path = "/home/escanor/Apps/verifydtapn-strategy_output/build/bin/Results/"

csv_results_path = "/home/escanor/GMLtoTAPN/data/csv/"

### Writes a json, then xml,q,tapn and then a ltl file for a Zoo Topo
## Can be chained by increasing scale
def write_zoo(network, scale=1):
    JB.jsonbuilder("Eenet")
    TB.write_to_file("Eenet", scale=scale)
    LTL.make_ltl_zoo("Eenet", scale=scale)


def write_all_custom():
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



def write_benchmarks_csv():
    CM.make_csv("Disjoint", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Disjoint", netsynth_results_path, csv_results_path, "Netsynth")
    CM.make_csv("Shared", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Shared", netsynth_results_path, csv_results_path, "Netsynth")
    CM.make_csv("Worst", dtapn_results_path, csv_results_path, "Tapaal")
    CM.make_csv("Worst", netsynth_results_path, csv_results_path, "Netsynth")


#write_zoo("Eenet", scale=10)
#TB.write_all_to_file()
JB.build_all()