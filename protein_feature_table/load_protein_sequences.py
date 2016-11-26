def load_protein_sequences(
            sequences_filename = "./protein_sequences/sequences.csv",
            signal_sequence_index_filename = "./protein_sequences/SPend.csv"):

    # Load all the peptide sequences. CSV file with Entry,Sequence, where
    # Entry is an Accession number, and Sequence is the peptide sequence.    
    seqs = {}
    with open(sequences_filename) as f:
        lines = f.readlines()
    for line in lines[1:]:
        accession, sequence = line.split(",")
        seqs[accession.strip()] = sequence.strip()
    
    # Load all indexes. The file is a csv with two columns:
    # Accession,SP end
    # Where "SP end" marks the index of last aminoacid in the signal sequence
    # of the peptide   
    ixs = {}
    with open(signal_sequence_index_filename) as f:
        lines = f.readlines()
    for line in lines[1:]:
        accession, ix = line.split(",")
        ixs[accession.strip()] = int(ix.strip())

    # Merge the data to produce one table that has
    # Accession, signal sequence, the rest of the sequence
    result = []
    
    for accession in seqs:
        if not accession in ixs:
            continue 
        last_signal_seq_ix = ixs[accession]
        signal_sequence = seqs[accession][:last_signal_seq_ix]
        rest_of_sequence = seqs[accession][last_signal_seq_ix:]
        result.append((accession,signal_sequence,rest_of_sequence))
    
    return result

if __name__ == "__main__":
    print load_protein_sequences()
