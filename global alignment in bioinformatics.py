import numpy as np
class Solution:
    def global_alignment(self, sequence_A: str, sequence_B: str, substitution: dict, gap: int) -> [tuple]:
        sequence_A = sequence_A.upper()
        sequence_B = sequence_B.upper()
        # Initialize matrix
        rows, cols = len(sequence_A) + 1, len(sequence_B) + 1
        D = [[0 for j in range(cols)] for i in range(rows)]
        
        # Initialize first row and column
        for i in range(1, rows):
            D[i][0] = D[i-1][0] + gap
        for j in range(1, cols):
            D[0][j] = D[0][j-1] + gap
            
        # Fill matrix according to recurrence relation
        for i in range(1, rows):
            for j in range(1, cols):
                match_score = substitution[sequence_A[i-1]][sequence_B[j-1]]
                diagonal = D[i-1][j-1] + match_score
                horizontal = D[i][j-1] + gap
                vertical = D[i-1][j] + gap
                D[i][j] = max(diagonal, horizontal, vertical)
        
        # Traverse matrix to determine all possible alignments
        aligned_sequences = []
        stack = [(rows-1, cols-1, "", "")]
        while stack:
            i, j, aligned_A, aligned_B = stack.pop()
            if i == 0 and j == 0:
                aligned_sequences.append((aligned_A, aligned_B))
            else:
                if i > 0 and j > 0 and D[i][j] == D[i-1][j-1] + substitution[sequence_A[i-1]][sequence_B[j-1]]:
                    stack.append((i-1, j-1, sequence_A[i-1] + aligned_A, sequence_B[j-1] + aligned_B))
                if j > 0 and D[i][j] == D[i][j-1] + gap:
                    stack.append((i, j-1, "-" + aligned_A, sequence_B[j-1] + aligned_B))
                if i > 0 and D[i][j] == D[i-1][j] + gap:
                    stack.append((i-1, j, sequence_A[i-1] + aligned_A, "-" + aligned_B))
        
        # Print matrix
        matrix = []
        for i in range(rows):
            row = [D[i][j] for j in range(cols)]
            matrix.append(row)
        
        # Print matrix as a list of lists
        
        output_str = '[' + "\n ".join([str(row) for row in matrix]) + ']'
        print(output_str)

        if len(aligned_sequences) == 1:
            return [aligned_sequences[0]]
        else:
            return aligned_sequences


solver = Solution()
seq_A = input("Enter sequence A: ")
seq_B = input("Enter sequence B: ")
gap= int(input("Enter gap penalty: "))
substitution = {
    'A': {'A':1,'T':-1,'C':-1,'G':-1},
    'T': {'A':-1,'T':1,'C':-1,'G':-1},
    'C': {'A':-1,'T':-1,'C':1,'G':-1},
    'G': {'A':-1,'T':-1,'C':-1,'G':1}
}

aligned_sequences = solver.global_alignment(seq_A, seq_B, substitution, gap)
print(aligned_sequences)
