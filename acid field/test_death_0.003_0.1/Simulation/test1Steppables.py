from cc3d.core.PySteppables import *
import numpy as np
import random

#adding acid_mean,xml,size modification,field initial value,getfield,acid-dependent
P1=0.9
P2=0.9
D1=0.003
D2=0.005
T=20000
n_cells=np.zeros((2,T))
acid_mean=1000

class test1Steppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        for cell in self.cell_list:
            cell.targetVolume = 100
            cell.lambdaVolume = 2.0
            
        self.field.ACID[0:200,0:200,0]=acid_mean
        self.field.ACID[200:400,0:200,0]=0

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        print(mcs)
        for cell in self.cell_list:
            if cell.type==1:
                n_cells[0,mcs]+=1
            else:
                n_cells[1,mcs]+=1
            if random.random()<0.01:
                if cell.type==1 and random.random()<D1*100:
                    #print(cell.targetVolume)
                    #self.delete_cell(cell)
                    cell.targetVolume = 0 #Starts apoptosis
                    cell.lambdaVolume = 200 #Optional: make the shrinkage happen very fast
                elif cell.type==2 and random.random()<(D1+(D2-D1)*self.field.ACID[cell.xCOM, cell.yCOM, cell.zCOM]/acid_mean*2)*100:
                    cell.targetVolume = 0 #Starts apoptosis
                    cell.lambdaVolume = 200 #Optional: make the shrinkage happen very fast

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """
        np.savetxt(r"C:\Users\admin\CC3DWorkspace\output\n_cells.txt",n_cells)
        print(n_cells)

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
        np.savetxt(r"C:\Users\admin\CC3DWorkspace\output\n_cells.txt",n_cells)
        print(n_cells)

class proliferationSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)
    
    def step(self, mcs):
        
        cells_to_divide=[]
        for cell in self.cell_list:
            if cell.volume>100:
                if cell.type==1 and random.random()<P1: 
                    cells_to_divide.append(cell)
                elif cell.type==2 and random.random()<P2:
                    cells_to_divide.append(cell)

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        if self.parent_cell.type==1:
            self.child_cell.type=1
        else:
            self.child_cell.type=2

class DeathSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        cells_to_delete = []
        for cell in self.cell_list:
            if cell.volume < 2: #Replace '2' with any arbitrary small number
                cells_to_delete.append(cell)

        for cell in cells_to_delete:
            self.delete_cell(cell)       
            
class growSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        '''
        constructor
        '''
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        '''
        called every MCS or every "frequency" MCS (depending how it was instantiated in the main Python file)
        '''
        # PLACE YOUR CODE BELOW THIS LINE
        for cell in self.cell_list:
            if cell.targetVolume<100 and cell.targetVolume>0:
                cell.targetVolume += 1 
