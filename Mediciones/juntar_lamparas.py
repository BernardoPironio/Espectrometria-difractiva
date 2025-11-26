import numpy as np
import pandas as pd
import os
from tqdm import tqdm
from pathlib import Path


def obtener_espectros(ruta, sep = ',', sep_str = ';'):
    #ruta  -->   Debe ser la dirección de la carpeta correspondiente al elemento
    mediciones = os.listdir(ruta)
    
    #-----------------------
    # Cargo las mediciones
    #-----------------------
    lamb_e, I_e = [], []
    for med in tqdm(mediciones):
        if med[-4:] == '.csv':
            ruta_med = ruta / f'{med}'
            df = pd.read_csv(ruta_med, sep = sep)[52 : -1].astype('string').to_numpy()[:, 0]
            datai = [ (data.split(sep_str)) for data in df]
            
            lamb_i = [ float(di[0]) for di in datai]
            I_i = [ float(di[1]) for di in datai]
            lamb_e.append(lamb_i), I_e.append(I_i)
            
    lamb_e, I_e = np.array(lamb_e), np.array(I_e)
    
    #----------------------
    # Valor medio y std
    #----------------------
    I, err_I = [], []
    lamb, err_lamb = [], []
    for i in range(0, len(lamb_i)):
        I.append(np.mean(I_e[:, i])), err_I.append(np.std(I_e[:, i]))
        lamb.append(np.mean(lamb_e[:, i])), err_lamb.append(np.std(lamb_e[:, i]))
        
    """
    Primera lista:
        * Elemento_0: lista de valores medios sobre longitud de onda
        * Elemento_1: lista de valores std sobre longitud de onda
    Segunda lista:
        * Elemento_0: lista de valores medios sobre intensidad
        * Elemento_1: lista de valores std sobre intensidad
    """
    return lamb, err_lamb, I, err_I


direccion_ejecutable = Path('juntar_lamparas.py').parent
direccion_arhivos = direccion_ejecutable / 'Mediciones'

Elementos = os.listdir(direccion_arhivos)

for elemento in Elementos:
    if elemento[-2:] != 'py':
        print(elemento)
        datos = {}
                
        ruta_elemento = direccion_arhivos / f'{elemento}'
        
        lamb_i, err_lamb_i, I_i, err_I_i = obtener_espectros(ruta_elemento)

        datos['Intensidad'] = I_i
        datos['err_Intensidad'] = err_I_i
        datos['Longitud_onda'] = lamb_i
        datos['err_Longitud_onda'] = err_lamb_i
        
        df = pd.DataFrame(datos)
        df.to_pickle(direccion_arhivos / f'{elemento}.pickle')
        

        
