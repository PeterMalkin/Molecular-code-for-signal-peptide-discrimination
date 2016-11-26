import os

Acids = {
        "Ala": "A",
        "Arg": "R",
        "Asn": "N",
        "Asp": "D",
        "Cys": "C",
        "Gln": "Q",
        "Glu": "E",
        "Gly": "G",
        "His": "H",
        "Ile": "I",
        "Leu": "L",
        "Lys": "K",
        "Met": "M",
        "Phe": "F",
        "Pro": "P",
        "Ser": "S",
        "Thr": "T",
        "Trp": "W",
        "Tyr": "Y",
        "Val": "V"
    }

def parse_scale_file(filename):
    global Acids
    result = {}
    with open(filename) as f:
        contents = f.readlines()

    for line in contents:
        s = line.split(",")
        if (s):
            result[Acids[s[0].strip()]] = float(s[1].strip())
    return result

def load_all_scale_tables(path="./scale_tables/"):
    result = {}
    for root, unused_dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".txt"):
                result[f[:f.find(".txt")]] = parse_scale_file(os.path.join(root, f))
    return result

def calc_scale(sequence, table):
    scale = 0.0
    for acid in sequence:
        if acid not in table:
            continue
        scale += table[acid]

    avg = scale/len(sequence)
    return avg

if __name__ == "__main__":
    all_scale_tables = load_all_scale_tables()
    for scale in all_scale_tables:
        table = all_scale_tables[scale]
        print scale + ": " + str(calc_scale("AAAAAAAAAAA", table))