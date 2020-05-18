import numpy as np
import matplotlib.pyplot as plt

from skimage import io, data
print("Las imágenes disponibles son:\n"
      "- aerial.tiff\n"
      "- airport.tiff\n"
      "- autopista.tif\n"
      "- bridge.tiff\n"
      "- car.tiff\n"
      "- clock.tiff\n"
      "- lena.png\n"
      "- moon.tiff\n"
      "- NOIS.tif\n"
      "- truck.tiff")
ruta  = "imagenes/"
nombreImg = input("Ingrese el nombre de la imagen junto a su formato : ")
ruta = ruta + nombreImg
img, imgF = io.imread(ruta),io.imread(ruta)
lambdaCoeff = float(input("Ingrese el valor del coeficiente lambda: "))
k = int(input("Ingrese el valor de la constante K: "))
nIter = int(input("Ingrese el número de iteraciones: "))
opcion= int(input("Ingrese 1 para utilizar la variante exponencial o 2 para la variante fraccionaria: "))
parametros = "K = " + str(k) + " Lambda = " + str(lambdaCoeff) + " Iteraciones = " + str(nIter) + " Variante: " + str(opcion)
print(parametros)

def compare(original, output, method):
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    ax = axes.ravel()
    ax[0] = plt.subplot(1, 2, 1)
    ax[1] = plt.subplot(1, 2, 2)
    ax[0].imshow(original, cmap=plt.cm.gray)
    ax[0].set_title("Original ")
    ax[0].axis('off')
    ax[1].imshow(output, cmap="gray")
    ax[1].set_title(method)
    ax[1].axis('off')
    plt.show()

def reflectEdges(imagen):
    dimx, dimy = imagen.shape
    output = np.zeros((dimx +2, dimy + 2))
    for x in range(output.shape[0]):
        for y in range(output.shape[1]):
            if (x == 0 and y == 0): ## Empezamos reflejando esquinas
                output[x,y] = imagen[x+1,y+1]
            elif (x == 0 and y == output.shape[1]-1):
                output[x,y] = imagen[x+1, imagen.shape[1]-2]
            elif (x == output.shape[0]-1 and y == 0):
                output[x,y] = imagen[imagen.shape[0] -2, y+1]
            elif ( x == output.shape[0]-1 and y == output.shape[1] -1 ):
                output[x,y] = imagen[imagen.shape[0]-2,imagen.shape[1]-2 ]
            elif ( x == 0 ): # Se reflejan las orillas
                output[x,y] = imagen[x+1, y-1]
            elif (x == output.shape[0]-1):
                output[x,y] = imagen[x-3, y-1]
            elif (y == 0):
                output[x,y] = imagen[x-1, y+1]
            elif(y == output.shape[1]-1):
                output[x,y] = imagen[x-1,y-3]
            else: # Se copia el resto de la imagen
                output[x,y] = imagen[x-1,y-1]

    return output


def diffusionCoefficient1(img,k):
    output = np.exp( -(img / k)**2)
    return output



def diffusionCoefficient2(img,k):
    output = 1/(1 + (img/k)**2)
    return output


def anisotropicDiffusion(img,option,k,lambdaCoeff):
    dimx, dimy = img.shape
    extendedImage = reflectEdges(img)
    output = np.zeros((dimx,dimy))
    for x in range(extendedImage.shape[0]):
        for y in range(extendedImage.shape[1]):
            if(x != 0 and x !=extendedImage.shape[0]-1 and y != 0 and  y !=extendedImage.shape[1]-1 ):
                northDiff = extendedImage[x-1,y] - extendedImage[x,y]
                southDiff = extendedImage[x+1,y] - extendedImage[x,y]
                westDiff = extendedImage[x,y-1] - extendedImage[x,y]
                eastDiff = extendedImage[x,y+1] - extendedImage[x,y]
                if(option == 1):
                    northCoeff = diffusionCoefficient1(northDiff,k)
                    southCoeff = diffusionCoefficient1(southDiff,k)
                    westCoeff = diffusionCoefficient1(westDiff,k)
                    eastCoeff = diffusionCoefficient1(eastDiff,k)
                else:
                    northCoeff = diffusionCoefficient2(northDiff,k)
                    southCoeff = diffusionCoefficient2(southDiff,k)
                    westCoeff = diffusionCoefficient2(westDiff,k)
                    eastCoeff = diffusionCoefficient2(eastDiff,k)
                north = northCoeff*northDiff
                south = southCoeff*southDiff
                west = westCoeff*westDiff
                east = eastCoeff*eastDiff
                output[x-1,y-1] = extendedImage[x,y] + lambdaCoeff*(north + south + west + east)
    return output

for i in range(nIter):
    print("Iniciando Iteracion: ",i +1)
    print("Procesando...")
    imgF = anisotropicDiffusion(imgF,opcion,k,lambdaCoeff)


compare(img,imgF, parametros)













    
