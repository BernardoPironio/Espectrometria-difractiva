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


# ---------Cargo los archivos----------
direccion_ejecutable = Path('Resultados_dia3.py').parent
direccion_arhivos = direccion_ejecutable / 'Mediciones_dia3'
direccion_arhivos_guardado = direccion_ejecutable / 'Mediciones_dia3'

archivos = os.listdir(direccion_arhivos)
concentraciones = []
for archivo in archivos:
    if archivo != 'Resultados_dia3.py':
        concentraciones.append(archivo)

for concentracion in concentraciones:
    print(concentracion)
        
    datos_emision = []
    datos_absorcion = []
    
    ruta_conc = direccion_arhivos / f'{concentracion}'
    modo_med = os.listdir(ruta_conc)
    print(modo_med)

    for modo in modo_med:
        print(modo)
        ruta_final = ruta_conc / f'{modo}'
        print(ruta_final)
        try:
            lamb_i, err_lamb_i, I_i, err_I_i = obtener_espectros(ruta_final)
        except:
            lamb_i, err_lamb_i, I_i, err_I_i = obtener_espectros(ruta_final, sep = ';', sep_str = ',')
            

        if modo == 'Emi':
            datos_emision.append(
                {
                    'Intensidad': I_i,
                    'err_Intensidad': err_I_i,
                    'Longitud_onda': lamb_i,
                    'err_Longitud_onda':err_lamb_i
                }
            )
        else:
            datos_absorcion.append(
                {
                    'Intensidad': I_i,
                    'err_Intensidad': err_I_i,
                    'Longitud_onda': lamb_i,
                    'err_Longitud_onda':err_lamb_i
                }
            )
    
    # Guardo los resultados
    #--> Emision
    df_Emision = pd.DataFrame(datos_emision)
    df_Emision.to_pickle(direccion_arhivos_guardado / f'{concentracion}' / 'Emision.pickle')
    
    df_Abosorcion = pd.DataFrame(datos_absorcion)
    df_Abosorcion.to_pickle(direccion_arhivos_guardado / f'{concentracion}' / 'Absorcion.pickle')
