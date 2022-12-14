import correctionlib
from correctionlib import schemav2 as schema
from coffea.lookup_tools.txt_converters import convert_rochester_file
import correctionlib._core as core
import numpy as np
from coffea.lookup_tools.rochester_lookup import rochester_lookup

dt = convert_rochester_file('RoccoR2017UL.txt')
coffeaRC = rochester_lookup(dt)

def wrap(*corrs):
    cset = schema.CorrectionSet(
        schema_version=schema.VERSION,
        corrections=list(corrs),
    )
    return core.CorrectionSet.from_string(cset.json())

Ms = dt['values']['M'][0][0][1].flatten()
As = dt['values']['A'][0][0][1].flatten()

cset = wrap(
    schema.Correction(
        name = "kScaleDT",
        version = 2,
        inputs = [
            schema.Variable(name='Q', type='real'),
            schema.Variable(name='pt', type='real'),
            schema.Variable(name='eta', type='real'),
            schema.Variable(name='phi', type='real'),
        ],
        generic_formulas=[
            schema.Formula(
                nodetype='formula',
                expression="1.0 / ([0] + x * [1] * y)",
                parser="TFormula", 
                variables=["Q","pt"]
            )
        ],
        output = schema.Variable(name = 'muon pt sf', type='real'),
        data=schema.MultiBinning(
            nodetype='multibinning',
            inputs=['eta', 'phi'],
            edges=[dt['edges']['scales'][i].tolist() for i in range(2)],
            content=
                [schema.FormulaRef(
                    nodetype='formularef',
                    index=0,
                    parameters=[Ms[i], As[i]]
                ) for i in range(len(Ms))],
            flow='error'
        )
    )
)

testQ = np.asarray([0.0, 0.0])
testPT = np.asarray([50.0, 50.0])
testETA = testQ
testPHI = testQ

print("Inputting single values at a time works:")
print(cset['kScaleDT'].evaluate(testQ[0], testPT[0], testETA[0], testPHI[0]))
print()
print("Inputting arrays of values at a time FAILS:")
print(cset['kScaleDT'].evaluate(np.array(testQ), np.array(testPT), np.array(testETA), np.array(testPHI)))
