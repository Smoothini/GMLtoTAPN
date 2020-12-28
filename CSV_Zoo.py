import os,csv

results_path = "data/zoo_results"

def btfy_time(u_time):
    times = u_time.split("m")
    b_time = int(times[0]) * 60 + float(times[1])
    return b_time

def read_files():
    dtapn = []
    netsynth = []
    for f in os.listdir(results_path):
        vals = f[:-4].split("_")
        t = open(f"{results_path}/{f}")
        time_value = ""
        data = t.readlines()
        if data[1].__contains__("real"):
            time_value += str(btfy_time(data[1][:-2].split('\t')[1]))
        else:
            time_value += "-1"
        if vals[1] == "dtapn":
            dtapn.append(time_value)
        elif vals[1] == "netsynth":
            netsynth.append(time_value)
    return sorted(dtapn), sorted(netsynth)

def write_csv():
    dt, ltl = read_files()
    with open("results_topology_zoo.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["DTapn", "Netsynth"])
        for key in range(len(dt)):
            writer.writerow([dt[key], ltl[key]])
        file.close()
        print(f"CSV file with results from {max(len(dt), len(ltl))} topolozy zoo networks written!")


write_csv()


