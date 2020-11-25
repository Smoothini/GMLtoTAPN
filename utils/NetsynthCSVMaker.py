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
    with open(f"{results_path}results.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node Count", "Netsynth (D)"])
        for i in filebatch("Disjoint"):
            s,t = i
            writer.writerow([s,t])
        file.close()

    with open(f"{results_path}results.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node Count", "Netsynth (W)"])
        for i in filebatch("Worst"):
            s,t = i
            writer.writerow([s,t])
        file.close()

    with open(f"{results_path}results.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node Count", "Netsynth (S)"])
        for i in filebatch("Shared"):
            s,t = i
            writer.writerow([s,t])
        file.close()

    fd = filebatch("Disjoint")
    fw = filebatch("Worst")
    fs = filebatch("Shared")
    
    with open(f"{results_path}results_.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node Count", "Netsynth (D)","Node Count", "Netsynth (W)","Node Count", "Netsynth (S)"])
        for i in range(max(len(fd), len(fw), len(fs))):
            if len(fd) > i:
                sd,td = fd[i]
            else:
                sd,td = 0,0

            if len(fw) > i:
                sw,tw = fw[i]
            else:
                sw,tw = 0,0

            if len(fs) > i:
                ss,ts = fs[i]
            else:
                ss,ts = None,None
            writer.writerow([sd,td,sw,tw,ss,ts])
        file.close()
    print("CSV file out of netsynth results made!")

    

make_csv()