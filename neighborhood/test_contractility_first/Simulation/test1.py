
from cc3d import CompuCellSetup
        

from test1Steppables import test1Steppable
CompuCellSetup.register_steppable(steppable=test1Steppable(frequency=1))
        
from test1Steppables import proliferationSteppable
CompuCellSetup.register_steppable(steppable=proliferationSteppable(frequency=1))

from test1Steppables import DeathSteppable
CompuCellSetup.register_steppable(steppable=DeathSteppable(frequency=1))


        
from test1Steppables import growSteppable
CompuCellSetup.register_steppable(steppable=growSteppable(frequency=1))

CompuCellSetup.run()
