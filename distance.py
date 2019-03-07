import numpy as np

#Scores
gap_score=2
substitution_score=1
match_score=0

"""To calculate the similarity score between two Strings"""
def similarity(A,B):
    score=np.zeros([len(A)+1,len(B)+1])
    for i in range(len(A)+1):
        for j in range(len(B)+1):
            if (i==0 or j==0):
                score[i][j]=i*gap_score+j*gap_score
            else:
                scoreDiag=""
                if A[i-1]==B[j-1]:
                    scoreDiag=score[i-1][j-1]+match_score
                else:
                    scoreDiag=score[i-1][j-1]+substitution_score
                scoreLeft=score[i][j-1]+gap_score
                scoreUp=score[i-1][j]+gap_score
                score[i][j]=min(scoreLeft,scoreUp,scoreDiag)
    return score[len(A)][len(B)]
