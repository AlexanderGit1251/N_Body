from abc import ABC, abstractmethod
import numpy as np
import scipy.constants as sp

class Fuerza(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def fuerzas(self):
        pass

    @abstractmethod
    def energia_potencial(self):
        pass

class FuerzaGravitatoria(Fuerza):

    def __init__(self):
        pass

    def fuerzas(self, posiciones, velocidades, masas):
            
            R = posiciones[None, :, :] - posiciones[:, None, :]
            normas = np.linalg.norm(R, axis = 2, keepdims = True)
            np.fill_diagonal(normas[:,:,0], np.inf)     
            aceleraciones = np.sum(sp.G*(R*masas/normas**3), axis = 1)
            return np.array([velocidades, aceleraciones])
    
    def energia_potencial(self, posiciones, masas):

            R = posiciones[:,None,:] - posiciones[None, :, :]
            normas = np.linalg.norm(R, axis = 2)
            np.fill_diagonal(normas, np.inf)
            U = (- 1/2 )*np.sum((masas @ masas.T * sp.G)/normas)
            return U









        



