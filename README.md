# SanajahtiSolver

This repo contains solver for Sanajahti game written in Python programming language. 

## How to Use

Example run and first few lines printed on stdout:  
Point (0,0) represents top left corner and (size - 1, size - 1) bottom right corner.

```
python3 solver.py -c cknaäytiennswpii -s 4
```

Found word: KÄYNNISTIN, Word path: (0, 1) -> (1, 0) -> (1, 1) -> (2, 2) -> (2, 1) -> (3, 2) -> (2, 3) -> (1, 2) -> (1, 3) -> (0, 2)  
Found word: PINNISTYÄ, Word path: (3, 1) -> (3, 2) -> (2, 1) -> (2, 2) -> (3, 3) -> (2, 3) -> (1, 2) -> (1, 1) -> (1, 0)  
Found word: PIINTYÄ, Word path: (3, 1) -> (3, 2) -> (3, 3) -> (2, 2) -> (1, 2) -> (1, 1) -> (1, 0)  
Found word: KÄYNTI, Word path: (0, 1) -> (1, 0) -> (1, 1) -> (2, 2) -> (1, 2) -> (1, 3)  
...
