import os,csv

def rows(ntype):
    content = "Net generation overhead,JSON,DTapn,DTapnQ,LTL,Init+Final\n"
    n = 0
    for fname in sorted(os.listdir("data/time/" + ntype)):
        if n%5 == 0:
            row = ""
            fname = fname[:-4].split("_")
            print(fname)
            fdx = open(f"data/time/{ntype}/{ntype}_{fname[1]}_PREP.txt")
            dx = float(fdx.read())
            fdx.close()
            row += f"{float(dx)},"
            fdx = open(f"data/time/{ntype}/{ntype}_{fname[1]}_JSON.txt")
            dx = float(fdx.read())
            fdx.close()
            row += f"{float(dx)},"
            fdx = open(f"data/time/{ntype}/{ntype}_{fname[1]}_DXML.txt")
            dx = float(fdx.read())
            fdx.close()
            row += f"{float(dx)},"
            fdx = open(f"data/time/{ntype}/{ntype}_{fname[1]}_DQuery.txt")
            dx = float(fdx.read())
            fdx.close()
            row += f"{float(dx)},"
            fdx = open(f"data/time/{ntype}/{ntype}_{fname[1]}_LTL.txt")
            dx = float(fdx.read())
            fdx.close()
            row += f"{float(dx)},"
            
            if fname[0] == "Shared":
                fname[1] = (int((int(fname[1])-1)/3)) * 3 + 1
                fname[1] = (int((int(fname[1])-1)/3)) *2*2
            if fname[0] == "Worst":
                fname[1] = (int((int(fname[1])-1)/3)) * 3 + 1
                fname[1] = (int(fname[1])-1) *2
            if fname[0] == "Disjoint":
                fname[1] = int(fname[1]) +4
            row+= f"{fname[1]}\n"
            content += row
        n+=1
    return content



    
def make_csv(ntype):
    
    f = open(f"data/time/{ntype}_overhead.csv", "w")
    f.write(rows(ntype))
    f.close()
    print(f"CSV file out of overhead times for building {ntype} networks made!")