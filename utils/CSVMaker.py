import os,csv


def btfy_time(u_time):
    times = u_time.split("m")
    b_time = int(times[0]) * 60 + float(times[1])
    return b_time

def filebatch(ntype, path):
    content = {}
    for fname in os.listdir(path + ntype):
        size = int(fname[(len(ntype)+1):-4])
        with open(f"{path}{ntype}/{fname}") as f:
            raw_time = (f.readlines()[1][5:-2])
            fine_time = btfy_time(raw_time)
        content[size] = fine_time
    return sorted(content.items())

    
def make_csv(files, input_path, output_path, verifier):
    fb = filebatch(files, input_path)
    
    with open(f"{output_path}results_{files}_{verifier}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node Count", f"{verifier} ({files})"])
        for i in range(len(fb)):
            nodes, time = fb[i]
            writer.writerow([nodes, time])
        file.close()
    print(f"CSV file out of {verifier} on {files} networks results made!")