
sensitivity_table = {}
Gcalc_table = {}
KD_table = {}
WW_table = {}

def load_sensitivity_table():
    with open("./sensitivity_labels/sensitivity_with_scales.csv") as f:
        lines = f.readlines()
    for line in lines[1:]:
        accession, sensitivity, Gcalc, KD, WW = line.split(",")
        sensitivity_table[accession.strip()] = sensitivity.strip()
        Gcalc_table[accession.strip()] = Gcalc.strip()
        KD_table[accession.strip()] = KD.strip()
        WW_table[accession.strip()] = WW.strip()
        
    return sensitivity_table

# Note the file is 0-active. Meaning "0" means the sequence is sensitive,
# "1" - not sensitive. Weird
def get_sensitivity_label(accession):
    if not sensitivity_table:
        load_sensitivity_table()
    if accession not in sensitivity_table:
        return "not sensitive"
    if sensitivity_table[accession] == "0":
        return "sensitive"
    return "not sensitive"

def get_min_Gcalc(accession):
    if not Gcalc_table:
        load_sensitivity_table()
    if accession not in Gcalc_table:
        return 0.0
    return Gcalc_table[accession]

def get_min_KD(accession):
    if not KD_table:
        load_sensitivity_table()
    if accession not in KD_table:
        return 0.0
    return KD_table[accession]

def get_min_WW(accession):
    if not WW_table:
        load_sensitivity_table()
    if accession not in KD_table:
        return 0.0
    return WW_table[accession]
