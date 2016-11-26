from calc_scales import load_all_scale_tables, calc_scale
from load_protein_sequences import load_protein_sequences

def get_table_heading(all_scale_tables):
    result = []
    result.append("accession")
    result.append("signal sequence")
    result.append("rest of sequence")
    for scale in all_scale_tables:
        result.append("signal sequence "+scale)
        result.append("rest of sequence "+scale)
    return result

def calculate_signal_peptide_features_table(all_scale_tables, all_sequences):
    result = []
    for item in all_sequences:
        line = []
        accession = item[0]
        signal_seq = item[1]
        rest_seq = item[2]
         
        line.append(accession)
        line.append(signal_seq)
        line.append(rest_seq)
        
        for scale in all_scale_tables:
            table = all_scale_tables[scale]
            scale_signal_seq = calc_scale(signal_seq, table)
            scale_rest_seq = calc_scale(rest_seq, table)
            line.append(scale_signal_seq)
            line.append(scale_rest_seq)
        
        result.append(line)
        del line
    return result

def save_table(table_headings, table_contents, filename = "features_table.csv"):
    with open(filename,"w") as f:
        for item in table_headings:
            f.write(str(item)+",")
        f.write("\n")
        for items in table_contents:
            for item in items:
                f.write(str(item)+",")
            f.write("\n")

def Main():
    all_scale_tables = load_all_scale_tables()
    all_sequences = load_protein_sequences()
    table_headings = get_table_heading(all_scale_tables)
    table_contents = calculate_signal_peptide_features_table(all_scale_tables, all_sequences)
    save_table(table_headings, table_contents)

if __name__ == "__main__":
    Main()
