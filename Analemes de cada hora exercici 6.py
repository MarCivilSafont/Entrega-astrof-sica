# -*- coding: utf-8 -*-
"""
Created on Thu May 22 12:52:59 2025

@author: Usuari
"""

import numpy as np
import matplotlib.pyplot as plt

# Obliquitat de l'eclíptica
ε = np.radians(23.44)  

def calculate_D(y, d):
    return 6.24004077 + 0.01720197 * (365.25 * (y - 2000) + d)

def equation_of_time_precise(y, d):
    D = calculate_D(y, d)
    return -7.659 * np.sin(D) + 9.863 * np.sin(2 * D + 3.5932)

def solar_declination(dia):
    return 23.44 * np.sin(2 * np.pi * (dia - 81) / 365)

def analemma_points(lat, lon, hour, year=2025):
    φ = np.radians(lat)
    λ = np.radians(lon)

    days = np.arange(1, 366)
    altures = []
    azimuts = []

    for d in days:
        δ_deg = solar_declination(d)
        δ = np.radians(δ_deg)

        EoT_min = equation_of_time_precise(year, d)
        H = np.radians(EoT_min * 0.25)

        hour_angle = (hour - 12) * 15 + np.degrees(λ)
        H = H + np.radians(hour_angle)

        alt = np.arcsin(np.sin(φ) * np.sin(δ) + np.cos(φ) * np.cos(δ) * np.cos(H))
        altures.append(np.degrees(alt))

        sin_A = -np.cos(δ) * np.sin(H) / np.cos(alt)
        cos_A = (np.sin(δ) - np.sin(alt) * np.sin(φ)) / (np.cos(alt) * np.cos(φ))
        A = np.arctan2(sin_A, cos_A) % (2 * np.pi)
        azimuts.append(np.degrees(A))

    return np.array(azimuts), np.array(altures)

# Paràmetres
lat = 41.5
lon = 2.107
year = 2025

plt.figure(figsize=(10, 10))
for hour in range(24):
    azimuts, altures = analemma_points(lat, lon, hour, year)
    if hour == 0:
        # Scatter a les 00:00
        plt.scatter(azimuts, altures, label=f'{hour}:00', s=2)
    else:
        # Plot per la resta d'hores
        plt.plot(azimuts, altures, label=f'{hour}:00')


plt.xlabel('Azimut (°)', fontsize=22)
plt.ylabel('Altura (°)', fontsize=22)
plt.grid(True)
plt.legend(loc='upper right', fontsize='medium', ncol=2)
plt.tick_params(axis='both', which='major', labelsize=19)
plt.show()

