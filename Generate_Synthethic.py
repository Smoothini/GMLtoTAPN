import utils.TAPNBuilder as TB
import utils.TestNets as TN
import utils.DTAPNBuilder as DB
import utils.CSVMaker as CM
import utils.LtLBuilder as LTL
import utils.JsonBuilder as JB
import time,os



def write_all_custom():

    for i in range(100, 2200, 100):
        DB.build_composed_model(TN.generate_disjoint(i))
    for i in range(4000, 22000, 2000):
        DB.build_composed_model(TN.generate_disjoint(i))
  
    for i in range(120, 520, 20):
        DB.build_composed_model(TN.generate_shared(i))

    for i in range(4, 28, 3):
        DB.build_composed_model(TN.generate_worst(i))
    for i in range(50, 225, 25):
        DB.build_composed_model(TN.generate_worst(i))



write_all_custom()

######- I N F O -######
## This will build all the json files
#JB.build_all()
## This will build all the xml,q and tapaal files
#TB.write_all_to_file() 
## This will build all the ltl files
#LTL.make_all_zoo()

### This will chain writing a json, (xml,q,tapaal) and ltl, one after the other
# By default, scale is already 1, so it can be used also without it.
#write_zoo("Network", scale=10)
