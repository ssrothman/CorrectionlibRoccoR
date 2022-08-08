import correctionlib
import numpy as np

cset = correctionlib.CorrectionSet.from_file("test.json")

for pt in [0, 1, 2, 10, 11, 20, 25, 40, 50, 60, 100, 600, 999999]:
    print(pt, cset['test'].evaluate("2017_UL", float(pt)))