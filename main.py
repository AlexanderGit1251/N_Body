from fuerza import FuerzaGravitatoria
from integrador import RK4, Verlet, Euler
from sistema import Sistema
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
import os 
import json

def cargar_condiciones_iniciales(json_f):

    with open(f'condiciones_iniciales/{json_f}', 'r', encoding='utf-8') as file:

        datos = json.load(file)
        posiciones = np.array(datos["posiciones"])
        velocidades = np.array(datos["velocidades"])
        masas = np.array(datos["masas"])

    return posiciones, velocidades, masas

if __name__ == '__main__':
    

    # AJUSTES
    a = 0                                       # t inicial
    b = 60                                      # t final
    h = 0.001                                   # Paso
    FPS = 60                                    # FPS deseados para exportación
    duracion = 10                               # Duración del video/gif
    elevacion = 10                              # Elevación de la cámara
    azimutal = 30                               # Azimutal de la cámara
    guardar_vis = True                          # Guardar gif de la simulación
    guardar_condiciones = False                 # Guardar condiciones iniciales en json
    cargar_condiciones = ''                     # Dejar vacío para asignar manualmente

    posiciones = np.array([
        [0.0, 0.0, 0.0],
        [2.0, -1.0, 0.5],
        [-2.5, 1.5, -0.5],
        [1.0, 3.0, 1.0],
        [-3.0, -2.0, 0.2],
        [-1.0, -4.0, 0.7],
        [0, 4, 1]
    ])

    velocidades = np.array([
        [0.0, 0.0, 0.0],
        [0.8, 1.2, -0.6],
        [-1.0, -0.6, 0.7],
        [0.6, -0.4, 0.8],
        [-0.8, 1.3, -0.6],
        [-0.8, 1, -0.5],
        [0.5, -1.5 , 2]
    ])

    masas = np.array([
        [8e10],
        [2e10],
        [2e10],
        [3e10],
        [2e10],
        [4.5e10],
        [1e10]
    ])

    if cargar_condiciones:
        posiciones, velocidades, masas = cargar_condiciones_iniciales(cargar_condiciones)

    N = posiciones.shape[0]

    if np.max(masas) - np.min(masas) == 0:
        tamaños = masas - np.min
    else: 
        tamaños = (masas - np.min(masas))/(np.max(masas) - np.min(masas)) * 10


    sistema = Sistema(posiciones, velocidades, masas, FuerzaGravitatoria, RK4)
    

    t,R,V,K,U,T  = sistema.ejecutar(a, b, h)

    if guardar_condiciones:
        sistema.guardar_condiciones_iniciales()


    t_f,R_f,V_f,K_f,U_f,T_f  = sistema.obtener_frames(R,V,K,U,T,t,FPS, duracion)
    


    paleta = {
    0: '#00CED1',   
    1: '#FF8C00',   
    2: '#FF1493',  
    3: "#26FF00",   
    4: '#FF0000',   
    5: "#E6ADFF",  
    6: '#FFFF00',   
    7: '#0000FF', 
    8: '#32CD32',  
    9: '#FF4500',  
    10: '#FF00FF',  
    11: '#7CFC00',   
    12: '#1E90FF',  
    13: '#FFD700',   
    14: '#00FFFF',
    15: '#00FA9A',  
    16: '#BA55D3', 
    17: '#ADFF2F',   
    18: '#00FF00',  
    19: '#9400D3'   
}

    

    
    fig = plt.figure(figsize = (12,6) , facecolor="#000000")
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2, projection='3d')
    ax1.margins(10)
    pos = ax1.get_position()
    pos = [pos.x0, pos.y0 + 0.07, pos.width - 0.02, pos.height - 0.18]
    ax1.set_position(pos)

    ax2.set_facecolor("#000000")
    ax2.xaxis.pane.fill = ax2.yaxis.pane.fill = ax2.zaxis.pane.fill = False
    ax2.xaxis.pane.set_edgecolor("#DFDFDF")
    ax2.yaxis.pane.set_edgecolor("#DFDFDF")
    ax2.zaxis.pane.set_edgecolor("#DFDFDF")
    ax2.tick_params(colors="#BEBEBE", labelsize=6)
    ax2.set_xlabel("X", color="#DFDFDF", fontsize=10, labelpad=0)
    ax2.set_ylabel("Y", color="#DFDFDF", fontsize=10, labelpad=0)
    ax2.set_zlabel("Z", color="#DFDFDF", fontsize=10, labelpad=0)
    ax2.set_title(f"Simulación de {R_f.shape[1]} cuerpos", color="#DFDFDF", fontsize=10, pad=4)
    ax2.xaxis._axinfo["grid"].update({"color": "#5252526C", "linestyle": ":"}) # Ejemplo: Rojo
    ax2.yaxis._axinfo["grid"].update({"color": "#5252526C", "linestyle": ":"}) # Ejemplo: Verde
    ax2.zaxis._axinfo["grid"].update({"color": "#5252526C", "linestyle": ":"}) # Ejemplo: Azul
    ax2.view_init(elev = elevacion, azim = azimutal)

    ax1.set_facecolor("#000000")
    ax1.tick_params(colors="#DFDFDF", labelsize=6)
    ax1.set_xlabel("t (s)", color="#DFDFDF", fontsize=10, labelpad=0)
    ax1.set_ylabel("E (J)", color="#DFDFDF", fontsize=10, labelpad=0)
    ax1.grid(alpha = 0.2, ls = ":")
   
    
    

    line1, = ax1.plot([], [], label='Cinética', color='mediumturquoise', lw=2)
    line2, = ax1.plot([], [], label='Potencial', color='orangered', lw=2)
    line3, = ax1.plot([], [], label='Total', color='gold', lw=2)


    ax1.legend(facecolor = "#000000", edgecolor = "#DFDFDF", labelcolor = "#DFDFDF", prop={'size': 8, 'family': 'monospace'})
    ax1.set_title('Energía vs Tiempo', color="#DFDFDF",  fontfamily="monospace", fontsize = 10, pad = 4, y = 1.14 )
    ax1.set_xlim(np.min(t_f), np.max(t_f))
    y_max = max(np.max(K_f), np.max(U_f), np.max(T_f))
    y_min = min(np.min(K_f), np.min(U_f))

    x2_max = np.max(R_f[:,:,0])
    y2_max = np.max(R_f[:,:,1])
    z2_max = np.max(R_f[:,:,2])

    x2_min = np.min(R_f[:,:,0])
    y2_min = np.min(R_f[:,:,1])
    z2_min = np.min(R_f[:,:,2])

    ax2.set_xlim(x2_min + 0.1 * x2_min, x2_max + 0.1* x2_max)
    ax2.set_ylim(y2_min + 0.1 * y2_min, y2_max + 0.1* y2_max)
    ax2.set_zlim(z2_min + 0.1 * z2_min, z2_max + 0.1* z2_max)

    ax1.set_ylim(y_min + 0.1*y_min, y_max + 0.1*y_max)

   
    plots = []
    c = 0
    scatters = []
    brillos = []

    for i in range(N):
        
        line, = ax2.plot([],[],[], color = paleta[c], alpha = 0.3, lw = 1)
        plots.append(line)
        scatter, = ax2.plot([],[],[], marker = 'o', color = paleta[c], ms = 5 + tamaños[i])
        scatters.append(scatter)
        brillo, = ax2.plot([],[],[], marker = 'o', color = paleta[c], ms = 12 + tamaños[i], alpha = 0.15)
        brillos.append(brillo)

        c += 1

        if c == (len(paleta) - 1):
            c = 0
    
    alpha = 0.5
    d_a = 0
    def update(frame):
        
        centro = np.sum(R_f[frame,:,:]*masas, axis = 0)/np.sum(masas)
        global d_a
        d = np.sqrt(np.sum((R_f[frame,:,:] - centro)**2, axis = 1))
        
        if frame == 0:
            d = np.median(d)
        else:
            d = (1-alpha)*np.median(d) + alpha*d_a

        d_a = d
       

        ax2.set_xlim(centro[0] - d, centro[0] + d)
        ax2.set_ylim(centro[1] - d, centro[1] + d)
        ax2.set_zlim(centro[2] - d, centro[2] + d)
       
        

        line1.set_data(t_f[:frame], K_f[:frame])
        line2.set_data(t_f[:frame], U_f[:frame])
        line3.set_data(t_f[:frame], T_f[:frame])
        
        for i in range(N):
            if frame > 150:
                plots[i].set_data_3d(R_f[frame-150:frame, i, 0],R_f[frame-150:frame, i, 1],R_f[frame-150:frame, i, 2])
            else:
                plots[i].set_data_3d(R_f[:frame, i, 0],R_f[:frame, i, 1],R_f[:frame, i, 2])
            scatters[i].set_data_3d([R_f[frame, i, 0]],[R_f[frame, i, 1]],[R_f[frame, i, 2]]) 
            brillos[i].set_data_3d([R_f[frame, i, 0]],[R_f[frame, i, 1]],[R_f[frame, i, 2]])            

        return line1, line2, line3, *plots, *scatters
    
    anim = FuncAnimation(fig, update, frames = len(t_f), interval = 1, blit = False, repeat = True)
    plt.tight_layout
    
    
    n_simulacion = len(os.listdir('simulaciones_gif/'))

    if guardar_vis:
        anim.save(f'simulaciones_gif/simulacion_{n_simulacion}.gif', dpi = 300)
    
    plt.show()