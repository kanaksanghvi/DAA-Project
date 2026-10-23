# DAA-Project

## How to run

```bash
python DAA.py
```

The program asks for two lines of input (positions in metres, separated by
spaces or commas):

```
House positions:        0 400 800 1200 1600
Candidate transmitters:  0 700 1400 2000
```

and prints the result:

```
Minimum multiply-covered houses: 1
Transmitters to build at:        [0, 700, 2000]
```

If no placement can cover every house, it prints an infeasibility message.
