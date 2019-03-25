from pathlib import Path
import pickle

class preprocess():
    """Class to process the data. Converts the txt file into dictionary for which key is sequnece ID and value is Amino Acid Sequence"""
    def __init__(self):
        self.pickleFiles=Path('pkl_files/seq.pkl')
        self.dataSeq=dict()
    
    def process(self):
        seq=str()
        with open('data.txt', 'rU') as f:
            for line_terminated in f:
                line = line_terminated.rstrip('\n')
                if line[0]=='>':
                    data=line
                elif line[len(line)-1]!='*':
                    seq=seq+line
                else:
                    seq=seq+line[:len(line)-1]
                    self.dataSeq[data]=seq
                    seq=""

    def export(self):
        with open(self.pickleFiles, 'wb') as file:
            pickle.dump(self.dataSeq, file)

if __name__ == "__main__":
    p=preprocess()
    p.process()
    p.export()
    print(p.dataSeq)

