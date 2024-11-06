
from cc3d import CompuCellSetup
        

from test1Steppables import test1Steppable

CompuCellSetup.register_steppable(steppable=test1Steppable(frequency=1))


CompuCellSetup.run()
