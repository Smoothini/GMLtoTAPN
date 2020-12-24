import os,csv

results_path = "data/synthethic_results"



def btfy_time(u_time):
    times = u_time.split("m")
    b_time = int(times[0]) * 60 + float(times[1])
    return b_time

def filebatch(ntype, path):
    content = {}
    for fname in os.listdir(path + ntype):
        size = int(fname[(len(ntype)+1):-4])
        with open(f"{path}{ntype}/{fname}") as f:
            cnt = f.readlines()
            fine_time = -1
            if cnt[1][0:4] == "real":
                raw_time = (cnt[1][5:-2])
                fine_time = btfy_time(raw_time)
        if ntype == "Disjoint":
            size +=4
        if ntype == "Shared":
            s1 = (int((size-1)/3)) * 3 + 1
            size = (int((s1-1)/3)) *2*2
        if ntype == "Worst":
            s1 = (int((size-1)/3)) * 3 + 1
            size = (s1-1) * 2
        content[size] = fine_time
    return sorted(content.items())

    
def make_csv(files, input_path, output_path, verifier):
    fb = filebatch(files, input_path)
    with open(f"{output_path}results_{files}_{verifier}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["(Init+Final", f"{verifier} {files})"])
        for i in range(len(fb)):
            nodes, time = fb[i]
            writer.writerow([f"({nodes}", f"{time})"])
        file.close()
    print(f"CSV file out of {verifier} on {files} networks results made!")

def write_benchmarks_csv():
    #make_csv("Disjoint", dtapn_satisfied, csv_path, "DTapn")
    #make_csv("Disjoint", netsynth_satisfied, csv_path, "Netsynth")
    #make_csv("Shared", dtapn_satisfied, csv_path, "DTapn")
    #make_csv("Shared", netsynth_satisfied, csv_path, "Netsynth")
    #make_csv("Worst", dtapn_satisfied, csv_path, "DTapn")
    make_csv("Worst", netsynth_satisfied, csv_path, "Netsynth")

    #make_csv("Disjoint", dtapn_nonsatisfied, csv_path, "Tapaal")
    #make_csv("Disjoint", netsynth_nonsatisfied, csv_path, "Netsynth")
    #make_csv("Shared", dtapn_nonsatisfied, csv_path, "Tapaal")
    #make_csv("Shared", netsynth_nonsatisfied, csv_path, "Netsynth")
    #make_csv("Worst", dtapn_nonsatisfied, csv_path, "Tapaal")
    #make_csv("Worst", netsynth_satisfied, csv_path, "Netsynth")



write_benchmarks_csv()
