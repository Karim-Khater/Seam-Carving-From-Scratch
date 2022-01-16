import sys              # pour prendre les arguments de la ligne de commande
import numpy as np      # pour toutes les operations matricielles
from PIL import Image   # pour lire l'image en RGB
from numba import jit   # pour la parallelisation de la compilation et diminuer le temps de l'execution
import random           # pour generer des valeurs aleatoires dans tester()
from scipy.ndimage.filters import convolve # utiliser dans le energy_sobel_filter
from numba.core.errors import NumbaWarning,NumbaPerformanceWarning, NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings         # pour la supprimation des warnings
from tqdm import trange # est utilisé pour visualiser la progression
"""
je supprime seulement les warnings de :
NumbaPendingDeprecationWarning & NumbaDeprecationWarning : avertissement 
pour l'utilisation d'une ancienne version de commande

NumbaPerformanceWarning & NumbaWarning : car j'utilise nopython=false qui signifie que
la compilation ne fonctionnera pas entièrement sans l'intervention de l'interpréteur Python

"""
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPerformanceWarning)
warnings.simplefilter('ignore', category= NumbaWarning)


# fonction qui utilise le sobel filtre pour 
# représenter l'énergie de l'image
def energy_sobel_filter(img):
    Gx = np.array([[-1, 0 ,1], [-2, 0 ,2],[ -1, 0 ,1]]) 
    Gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]) 
   
    Gx = np.stack([Gx] * 3, axis=2)
    Gy = np.stack([Gy] * 3, axis=2)
    gx = convolve(img , Gx)
    gy = convolve(img , Gy)

    sobel_image = np.absolute(gx) + np.absolute(gy)
    sobel_image = sobel_image.sum(axis=2)
    sobel_image = np.sqrt(sobel_image)
    
    return sobel_image


#fonction pour calculer le seam
@jit(nopython=False,parallel = True)
def dynamic_prog(img):
    
    img = energy_sobel_filter(img)
    rows, columns = img.shape
    val_min_array = img.copy()
    cost  = np.zeros(img.shape)
    for j in range(columns):
        cost[0,j] = val_min_array[0,j]

    for i in range(1,rows):
        for j in range(columns):
            if (j==0):
                min_val = min(cost[i-1 , j],cost[i-1 , j+1])
            elif( j < columns - 2):
                min_val = min(cost[i-1 , j],cost[i-1 , j+1])
                min_val = min(min_val, cost[i-1 , j-1])
            else:
                 min_val = min(cost[i-1 , j],cost[i-1 , j-1])
            cost[i,j] = val_min_array[i,j] + min_val    
    path = [ ]
    min_j = np.argmin(cost[rows-1,0:columns])

    pos = (rows -1 , min_j)
    path.append(pos)

    while pos[0] !=0 :
        pix_val = cost[pos] - val_min_array[pos]
        i,j = pos
        if j == 0 :
            if pix_val == cost[i-1 , j+1]:
                pos = (i-1 , j+1)
            else:
                pos = (i-1 , j)
        elif j < columns - 2:
            if pix_val == cost[i-1,j+1]:
                pos = (i-1,j+1) 
            elif pix_val == cost[i-1,j]:
                pos = (i-1,j)
            else:
                pos = (i-1,j-1)
        else:
            if pix_val == cost[i-1,j]:
                pos = (i-1,j)
            else:
                pos = (i-1,j-1) 
		
        path.append(pos)
    return path

# fonction pour afficher un colonne rouge qui représente le seam
def redline(img,path):
    rows , columns, _ = img.shape
    path_set = set(path)
    for i in range(rows):
        for j in range(columns):
            if (i,j) in path_set:
                img[i,j] = (255,0,0) 
                
    return img		

# fonction pour supprimer un colonne
# elle est aussi utilisé dans la supprimation
# de ligne en faisant une rotation de 90% de la matrice d'image
def remove_column(img,path):
    rows , columns, _ = img.shape
    output = np.zeros((rows,columns-1,3))
    path_set = set(path)
    seen_set = set()
    for i in range(rows):
        for j in range(columns):
            if (i,j) not in path_set and i not in seen_set:
                output[i,j] = img[i,j]
            elif (i,j) in path_set:
                seen_set.add(i)
            else:
                output[i,j-1] = img[i,j]
                
    return output

# fonction pour supprimer des colonnes pour obtenir le nouveau scale
def remove_columns_scale(img,scale):
    rows , columns,_ = img.shape
    diff = columns - int(columns * scale) 
    output = img
    for x in trange(diff):
        path = dynamic_prog(output)
        output = remove_column(output,path)
    return output

# fonction pour supprimer un ligne pour obtenir le nouveau scale
def remove_rows_scale(img,scale):
    rows , columns,_ = img.shape
    diff = rows - int(rows * scale)
    output = np.rot90(img,1,(0,1))
    for x in trange(diff):
        path = dynamic_prog(output)
        output = remove_column(output,path)
    output = np.rot90(output,3,(0,1))
    return output


# tester() pour generer un tableau 2d des nombre aleatoires au lieu d'
# utiliser chaque fois une image 
def tester():
    n = 5
    new = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            new[i,j] = random.randint(0,90)
    print(new)
    return new


"""
    POUR VOIR LE SEAM  :
    image = Image.open(input_image).convert('RGB')
    img = np.array(image)
    path = dynamic_prog(img)
    input = redline(img,path)
"""



def main():
    if len(sys.argv) != 5:
        print('USAGE : seam_carving.py  <r/c> <scale> <image_input> <image_output', file=sys.stderr)
        sys.exit(1)

    Seam_Axis = sys.argv[1]
    scale = float(sys.argv[2])
    input_image = sys.argv[3]
    output_image = sys.argv[4]
    image = Image.open(input_image).convert('RGB')
    img = np.array(image)

    if Seam_Axis == 'c':
        output = remove_columns_scale(img,scale)
    elif Seam_Axis == 'r':
        output = remove_rows_scale(img,scale)
    else :
        print('USAGE : seam_carving.py  <r/c> <scale> <image_input> <image_output', file=sys.stderr)
        sys.exit(1)
    
    Image.fromarray(np.uint8(output)).save('output/'+output_image + '.png')


if __name__ == '__main__':
    main()
