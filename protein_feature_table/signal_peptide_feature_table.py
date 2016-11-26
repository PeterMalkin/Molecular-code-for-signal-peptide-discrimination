from calc_scales import load_all_scale_tables, calc_scale
from load_protein_sequences import load_protein_sequences
from sensitivity_labels import get_sensitivity_label, get_min_Gcalc, get_min_KD, get_min_WW

def get_table_heading(all_scale_tables):
    result = []
    result.append("accession")
    result.append("signal sequence")
    result.append("sensitivity label")
    result.append("min _Gcalc")
    result.append("min KD")
    result.append("min WW")
    
    for scale in all_scale_tables:
        result.append("min "+scale)
        result.append("max "+scale)
    return result

def calc_min_max_scale_value(sequence,table):
    min_window_size = 9
    
    min_scale_signal_seq = 10000
    max_scale_signal_seq = -10000
    
    if (len(sequence)<=min_window_size):
        return 0,0

    for window_size in range(min_window_size, len(sequence)+1):
        for window_start in range(0,len(sequence)+1-window_size):
            window_end = window_start + window_size
            seq = sequence[window_start:window_end]
            value = calc_scale(seq, table)
            if (value > max_scale_signal_seq):
                max_scale_signal_seq = value
            if (value < min_scale_signal_seq):
                min_scale_signal_seq = value

    return min_scale_signal_seq,max_scale_signal_seq

def calculate_signal_peptide_features_table(all_scale_tables, all_sequences):
    result = []
    for item in all_sequences:
        line = []
        accession = item[0]
        signal_seq = item[1]

        line.append(accession)
        line.append(signal_seq)
        line.append(get_sensitivity_label(accession))
        line.append(get_min_Gcalc(accession))
        line.append(get_min_KD(accession))
        line.append(get_min_WW(accession))

        for scale in all_scale_tables:
            table = all_scale_tables[scale]
            min_scale_signal_seq,max_scale_signal_seq = calc_min_max_scale_value(signal_seq, table)
            line.append(min_scale_signal_seq)
            line.append(max_scale_signal_seq)
        
        result.append(line)
        del line
    return result

def save_table(table_headings, table_contents, filename = "signal_peptide_features_table.csv"):
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
