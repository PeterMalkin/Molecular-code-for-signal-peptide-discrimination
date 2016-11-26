
sensitivity_table = {}

def load_lable_sensitivity_table():
    with open("./sensitivity_labels/sensitivity_labels.csv") as f:
        lines = f.readlines()
    for line in lines[1:]:
        accession, sensitivity = line.split(",")
        sensitivity_table[accession.strip()] = sensitivity.strip()
    return sensitivity_table

# Note the file is 0-active. Meaning "0" means the sequence is sensitive,
# "1" - not sensitive. Weird
def get_sensitivity_label(accession):
    if not sensitivity_table:
        load_lable_sensitivity_table()
    if accession not in sensitivity_table:
        return 0
    if sensitivity_table[accession] == "0":
        return 1
    return 0
