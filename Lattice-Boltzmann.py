import numpy as np
from matplotlib import pyplot

plot_every = 50

def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def main():
# Constantes
    Nx = 400 # Cantidad de celdas en la extraccion en x 
    Ny = 100 # Cantidad de celdas en la extraccion en y
    tau = 0.53 # viscosidad 
    Nt = 4000 # Iteraciones

    """
    Velocidades de enrejado y pesos
    """
    NL = 9
    cxs = np.array([0,  0,  1,  1,  1,  0,  -1, -1, -1  ]) # El arreglo contiene los valores de las velocidades
    cys = np.array([0,  1,  1,  0,  -1, -1, -1, 0,  1   ])
    weigths = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])

    """
    Condiciones iniciales
        Queremos que el fluido sea mayoritariamente estatico con ciertas fluctuacions
    
    """
    F = np.ones((Ny,Nx,NL)) + .01 * np.random.randn(Ny,Nx,NL)

    F[:,:,3] = 2.3

    cylinder = np.full((Ny,Nx), False) # Obstaculo del agua (Si el valor es true, el objeto existe)
    
    # Se itera por cada punto para verificar si en ese punto es la distancia entre el cilindro para crear el cilindro y sus barreras
    for y in range(0,Ny): 
        for x in range(0,Nx):
            if(distance(Nx//4, Ny//2, x,y)< 13): # Checa la distancia entre los puntos donde esta el cilindro y los otros puntos
                cylinder[y][x] = True     # 13 es el radio del cilindro

    # Loop principal
    for it in range(Nt):
        print(it) # Se imprime por si hay bugs

        F[:,-1,[6,7,8]] = F[:,-2,[6,7,8]]
        F[:,0,[2,3,4]] = F[:,1,[2,3,4]]

        for i,cx,cy in zip(range(NL),cxs,cys):
            F[:,:,i] = np.roll(F[:,:,i],cx,axis = 1)
            F[:,:,i] = np.roll(F[:,:,i],cy,axis = 0)
        
        bndryF = F[cylinder,:]
        bndryF = bndryF[:,[0,5,6,7,8,1,2,3,4]]

        # Variables de fluidos para cuando chocan con el cilindro
        rho = np.sum(F,2)
        ux = np.sum(F*cxs,2)/rho
        uy = np.sum(F*cys,2)/rho

        F[cylinder,:] = bndryF
        ux[cylinder] = 0
        uy[cylinder] = 0

        # Choques
        Feq = np.zeros(F.shape)
        for i,cx,cy,w in zip(range(NL),cxs,cys,weigths):
            Feq[:,:,i] = rho * w * ( 1 + 3 * (cx*ux + cy*uy) + 9 * (cx*ux + cy*uy)**2 / 2 - 3 * (ux**2 + uy**2)/2 )

        F = F + -(1/tau) * (F-Feq)
        
        if(it % plot_every == 0):
            dfydx = ux[2:,1:-1] -1 - ux[0:-2,1:-1]
            dfxdy = uy[1:-1,2:] - uy[1:-1,0:-2]
            curl = dfydx - dfxdy
            
            pyplot.imshow(np.sqrt(ux**2 +uy**2))
            # pyplot.imshow(curl, cmap="bwr")

            pyplot.pause(0.01)
            pyplot.cla()
    

if __name__ == "__main__":
    main()