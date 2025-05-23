# -*- coding: utf-8 -*-
"""
Created on Fri May 23 11:46:42 2025

@author: Usuari
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('mart.csv', header=None)

az_stell = df[2].tolist()[1:]
alt_stell = df[3].tolist()[1:]

def dms_to_decimal_simple(dms_str):
    dms_str = dms_str.strip()
    sign = -1 if dms_str.startswith('-') else 1
    dms_str = dms_str.lstrip('+-')

    grados_part = dms_str.split('°')
    minutos_part = grados_part[1].split("'")
    segundos_str = minutos_part[1].replace('"', '')

    grados = int(grados_part[0])
    minutos = int(minutos_part[0])
    segundos = float(segundos_str)

    decimal = grados + minutos / 60 + segundos / 3600
    return sign * decimal

az_decimal = [dms_to_decimal_simple(az) for az in az_stell]
alt_decimal = [dms_to_decimal_simple(alt) for alt in alt_stell]

plt.figure(figsize=(10, 6))
plt.scatter(az_decimal, alt_decimal, color='orange')

plt.xlabel("Azimut (°)",fontsize=20)
plt.ylabel("Altura (°)",fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=17)
plt.grid(True)
plt.gca().invert_xaxis()
plt.tight_layout()
plt.show()