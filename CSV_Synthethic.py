import os,csv

results_path = "data/synthethic_results"

def places_to_edges(ntype, value):
    if ntype == "Disjoint":
        value = (int(value) + 4)
    if ntype == "Shared":
        value = (int((int(value)-1)/3)*3+1)
        value = (int((int(value)-1)/3))*2*2
    if ntype == "Worst":
        value = (int((int(value)-1)/3)*3+1)
        value = (int(value)-1)*2
    return value

def btfy_time(u_time):
    times = u_time.split("m")
    b_time = int(times[0]) * 60 + float(times[1])
    return b_time

def read_files(ntype):
    flist = []
    values = {}
    for f in os.listdir(results_path):
        if f.__contains__(ntype):
            flist.append(f)
            values[places_to_edges(ntype, f[:-4].split("_")[2])] = {}
            values[places_to_edges(ntype, f[:-4].split("_")[2])]["dtapn"] = ""
            values[places_to_edges(ntype, f[:-4].split("_")[2])]["ltl"] = ""
    flist.sort()
    for f in flist:
        vals = f[:-4].split("_")
        time_value = ""
        if os.path.getsize(f"{results_path}/{f}") > 0:
            d = open(f"{results_path}/{f}")
            data = d.readlines()
            if data[1].__contains__("real"):
                time_value += str(btfy_time(data[1][:-2].split('\t')[1]))
            else:
                time_value += "-1"    
        values[places_to_edges(ntype, vals[2])][vals[1]] = time_value
    skeys = sorted(values.keys())
    svalues = {}
    for i in skeys:
        svalues[i] = values[i]
    return svalues

def write_csv(ntype):
    data = read_files(ntype)
    with open(f"results_synthethic_{ntype}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Init+Final", "DTapn", "Netsynth"])
        for key in data.keys():
            writer.writerow([key, data[key]["dtapn"], data[key]["ltl"]])
        file.close()
        print(f"CSV file with results from Synthethic {ntype} networks written!")




write_csv("Disjoint")
write_csv("Shared")
write_csv("Worst")


