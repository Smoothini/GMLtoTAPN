import os,csv

results_path = "/home/escanor/Apps/netsynth/ltl_results/"

def filebatch(ntype):
    content = {}
    for fname in os.listdir(results_path + ntype):
        size = int(fname[(len(ntype)+1):-4])
        with open(f"{results_path}{ntype}/{fname}") as f:
            chk_time = float(f.readlines()[18][11:-1])
        content[size] = chk_time
    return sorted(content.items())

    
def make_csv():
    fd = filebatch("Disjoint")
    fw = filebatch("Worst")
    #fs = filebatch("Shared")
    
    with open(f"{results_path}results_dw_after.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node Count", "Netsynth (D)",None,"Node Count", "Netsynth (W)"])
        for i in range(max(len(fd), len(fw))):
            if len(fd) > i:
                sd,td = fd[i]
            else:
                sd,td = None,None

            if len(fw) > i:
                sw,tw = fw[i]
            else:
                sw,tw = None,None

            writer.writerow([sd,td,None,sw,tw])
        file.close()
    print("CSV file out of netsynth results made!")

make_csv()