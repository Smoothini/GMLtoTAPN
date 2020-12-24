import utils.TAPNBuilder as TB
import utils.TestNets as TN
import utils.DTAPNBuilder as DB
import utils.CSVMaker as CM
import utils.LtLBuilder as LTL
import utils.JsonBuilder as JB
import time,os



### Writes a json, then xml,q,tapn and then a ltl file for a Zoo Topo
## Can be chained by increasing scale
def write_zoo(network, scale=1):
    JB.jsonbuilder(network)
    TB.write_to_file(network, scale=scale)
    LTL.make_ltl_zoo(network, scale=scale)


def write_all_custom():

    for i in range(100, 2200, 100):
        DB.build_composed_model(TN.generate_disjoint(i))
    #for i in range(4000, 22000, 2000):
        #DB.build_composed_model(TN.generate_disjoint(i))

    #for i in range(2000, 6000, 1000):
     #   DB.build_composed_model(TN.generate_worst(i))

    #for i in range(4, 51, 3):
     #   DB.build_composed_model(TN.generate_worst(i))


def write_all_to_file(scale):
    start = time.time()
    cnt = 0
    for f in os.listdir("data/zoo_json"):
        try:
            write_zoo(f[:-5], scale=scale)
            cnt += 1
        except:
            print(f"Failure! {f[:-5]} not converted..")
    print("Operation done in: {} seconds".format((str(time.time()-start))[:5]))
    print(f"Succesfully written {cnt} files.")


#write_all_custom()
write_all_to_file(1)

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
