# -*- coding: utf-8 -*-
"""
Created on Mon May 19 08:04:04 2025

@author: Usuari
"""

import numpy as np
import matplotlib.pyplot as plt

# Obliqüitat de l'eclíptica
ε = np.radians(23.44)  

# Funció per calcular l'anomalia mitjana (D) segons el dia i l'any
def calculate_D(y, d):
    return 6.24004077 + 0.01720197 * (365.25 * (y - 2000) + d)

# Equació del temps en minuts, que dependrà de l'anomalia
def equation_of_time_precise(y, d):
    D = calculate_D(y, d)
    return -7.659 * np.sin(D) + 9.863 * np.sin(2 * D + 3.5932)  # en minuts

# Declinació solar (en graus) per a cada dia de l'any
def solar_declination(dia):
    return 23.44 * np.sin(2 * np.pi * (dia - 81) / 365)

# Funció per calcular l'analema per a qualsevol latitud, longitud i hora local
def analemma(lat, lon, hour, year=2025):
    φ = np.radians(lat)  # latitud en radians
    λ = np.radians(lon)  # longitud en radians

    days = np.arange(0, 366)  # Dies de l'any
    altures = []
    azimuts = []

    for d in days:
        δ_deg = solar_declination(d)
        δ = np.radians(δ_deg)

        # EoT en minuts → convertir a angle horari en radians (1 min = 0.25 graus = π/720 radians)
        EoT_min = equation_of_time_precise(year, d)
        H = np.radians(EoT_min * 0.25)

        # Calcular l'hora solar (hora local - longitud ajustada pel meridià)
        hour_angle = (hour - 12) * 15 + np.degrees(λ)  # Horari en graus

        # L'angle horari a les 12:00h solar és correcte en el sistema de coordenades
        H = H + np.radians(hour_angle)

        # Altura solar (en funció de la declinació i l'angle horari)
        alt = np.arcsin(np.sin(φ) * np.sin(δ) + np.cos(φ) * np.cos(δ) * np.cos(H))
        altures.append(np.degrees(alt))

        # Azimut solar (en funció de l'altura i l'angle horari)
        sin_A = -np.cos(δ) * np.sin(H) / np.cos(alt)
        cos_A = (np.sin(δ) - np.sin(alt) * np.sin(φ)) / (np.cos(alt) * np.cos(φ))
        A = np.arctan2(sin_A, cos_A) % (2 * np.pi)
        azimuts.append(np.degrees(A))

    # Dibuix de l'analema
    plt.figure(figsize=(7, 7))
    plt.plot(azimuts, altures, color='r')

    
    plt.xlabel("Azimut (°)",fontsize=18)
    plt.ylabel("Altura  (°)",fontsize=18)
    plt.grid(True)
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.show()

#Analema des de Bellaterra (41.5°N, 2.107°E), hora local 11:00h
analemma(lat=41.5, lon=2.107, hour=11)
