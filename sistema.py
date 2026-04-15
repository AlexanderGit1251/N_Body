import numpy as np

class Sistema:

    def __init__(self, posiciones, velocidades, masas, fuerza, integrador):
        self.__posiciones = posiciones
        self.__velocidades = velocidades
        self.__masas = masas
        self.__fuerza = fuerza()
        self.__integrador = integrador()


    def energia_cinetica(self, velocidades):
        K = np.sum(1/2*self.__masas * np.linalg.norm(velocidades, axis = 1, keepdims = True)**2)
        return K
    

    def ejecutar(self, a, b, h):
        t = np.arange(a, b + h, h)
        pasos = len(t)

        R = np.zeros((pasos,self.__posiciones.shape[0], self.__posiciones.shape[1]))
        V = np.zeros((pasos,self.__velocidades.shape[0], self.__velocidades.shape[1]))
        K = np.zeros(pasos)
        U = np.zeros(pasos)
        T = np.zeros(pasos)
        R[0,:,:] = self.__posiciones
        V[0,:,:] = self.__velocidades
        K[0] = self.energia_cinetica(V[0,:,:])
        U[0] = self.__fuerza.energia_potencial(R[0,:,:], self.__masas)
        T[0] = K[0] + U[0]
        

        for paso in range(pasos-1):
            
            R[paso + 1, :, :], V[paso + 1, :, :] = self.__integrador.integrar(self.__fuerza.fuerzas, h, R[paso,:,:], V[paso,:,:], self.__masas)
            K[paso + 1] = self.energia_cinetica(V[paso + 1, :, :])
            U[paso + 1] = self.__fuerza.energia_potencial(R[paso + 1, :, :], self.__masas)
            T[paso + 1] = K[paso + 1] + U[paso + 1]

        return t,R,V,K,U,T
    
    def obtener_frames(self, R, V, K, U, T, t, FPS, duracion):

        N = duracion*FPS
        frames = np.linspace(0, R.shape[0] - 1, N).astype(int)
        R_frames = R[frames]
        V_frames = V[frames]
        K_frames = K[frames]
        U_frames = U[frames]
        T_frames = T[frames]
        t_frames = t[frames]

        return t_frames, R_frames, V_frames, K_frames, U_frames, T_frames, 


            



    

    
