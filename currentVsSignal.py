import pandas as pd
from progressbar import ProgressBar


corrD = []
pbar = ProgressBar()

class currentVsSignal():
    def __init__(self, d = pd.DataFrame):
        print("in currentVsSignal class")
        # Y = 0
        t = 0
        V = -0.4
        s = 10
        D = []
        T = []
        global corrD

        # Extract the current value @ V and put it in D
        for i in pbar(range(0, (len(d) - 1))):
            j = i + 1
            k = i + 2
            A = d[i:j];
            xA = float(A[0]);
            yA = float(A[1])
            B = d[j:k];
            xB = float(B[0]);
            yB = float(B[1])
            if V > xA and V < xB:
                a = (yB - yA) / (xB - xA)
                b = yA - a * xA
                Y = a * V + b
                D.append(Y)
                t = t + 28
                T.append(t)

        # Correct from baseline using the cycle number where methane starts
        if s != 0:
            m = []
            for k in range(0, s):
                m.append(D[k])
            base = sum(m) / s
            corrD = [x - base for x in D]
        elif s == 0:
            corrD = [D]

    @staticmethod
    def getCorrData():
        global corrD
        print('getData works...')
        return [corrD]
