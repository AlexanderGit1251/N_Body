from abc import ABC, abstractmethod
import numpy as np

class Integrador(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def integrar(self):
        pass

class Euler(Integrador):
    def __init__(self):
        super().__init__()

    def integrar(self, fuerzas, h, R0, V0, masas):

        valores = fuerzas(R0, V0, masas)
        R = R0 + h*valores[0,:,:]
        V = V0 + h*valores[1,:,:]

        return  R, V


class RK4(Integrador):

    def __init__(self):
        super().__init__()

    def integrar(self, fuerzas, h, R0, V0, masas):
        
        k1 = fuerzas(R0, V0, masas)
        k2 = fuerzas(R0 + h*k1[0,:,:]/2, V0 + h*k1[1,:,:]/2, masas)
        k3 = fuerzas(R0+ h*k2[0,:,:]/2, V0 + h*k2[1,:,:]/2, masas)
        k4 = fuerzas(R0 + h*k3[0,:,:], V0 + h*k3[1,:,:], masas)
        R = R0 + (h/6)*(k1[0,:,:] + 2*k2[0,:,:] + 2*k3[0,:,:] + k4[0,:,:])
        V = V0 + (h/6)*(k1[1,:,:] + 2*k2[1,:,:] + 2*k3[1,:,:] + k4[1,:,:])

        return R, V

class Verlet(Integrador):

    def __init__(self):
        super().__init__()

    def integrar(self, fuerza, h, R0, V0, masas):
        A = fuerza(R0,V0,masas)[1,:,:]
        R = R0 + V0*h + A*(h**2)/2
        A_next = fuerza(R, V0, masas)[1,:,:]
        V = V0 + (A + A_next)*h/2

        return R, V


