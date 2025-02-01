import numpy as np
import random
import matplotlib.pyplot as plt

class KalmanFilter:
    def __init__(self, v: float, noised_signals_height, Q1=4.572, Q2=38.1):
        """
        Inicjalizacja filtru Kalmana
        :param v: Stała prędkość (m/s)
        :param noised_signals_height: Zaszumione pomiary wysokości
        :param Q1: Szum procesu dla wysokości <= 152.4m
        :param Q2: Szum procesu dla wysokości > 152.4m
        """
        self.v = v  # Stała prędkość obiektu
        self.noised_signals_height = noised_signals_height  # Zaszumione sygnały wejściowe
        self.B = 0.05  # Współczynnik wpływu prędkości na pozycję
        self.F = 1  # Macierz przejścia stanu
        self.H = 1  # Macierz obserwacji
        self.I = 1  # Macierz jednostkowa
        self.Q1 = Q1  # Szum procesu dla niskich wysokości
        self.Q2 = Q2  # Szum procesu dla wysokich wysokości
        
        # Dobieranie szumu pomiarowego w zależności od prędkości
        if v <= 3:
            self.R = 0.1  # Niski szum pomiarowy
        elif v <= 7:
            self.R = 0.3  # Umiarkowany szum pomiarowy
        elif v <= 12:
            self.R = 0.6  # Zwiększony szum pomiarowy
        else: self.R = 1  # Wysoki szum pomiarowy
            
        self.x = noised_signals_height[0]  # Początkowa wysokość
        self.P = 1  # Początkowa niepewność estymacji

    def prediction(self):
        """
        Faza predykcji filtru Kalmana
        Zwraca:
            x_pred: Przewidywany stan
            P_pred: Przewidywana niepewność
        """
        # Przewidywanie następnego stanu
        x_pred = self.F * self.x + self.B * self.v
        
        # Obliczanie przewidywanej niepewności
        P_pred = self.F * self.P * self.F + self.R
        
        return x_pred, P_pred

    def update(self, z, x_pred, P_pred):
        """
        Faza aktualizacji filtru Kalmana
        :param z: Aktualny pomiar
        :param x_pred: Przewidywany stan
        :param P_pred: Przewidywana niepewność
        """
        # Przerwanie filtracji powyżej 762 metrów
        if z > 762:
            return z

        # Obliczanie innowacji (różnica między pomiarem a predykcją)
        y = z - self.H * x_pred

        # Dobieranie szumu procesu w zależności od wysokości
        szum_procesu = self.Q1 if z <= 152.4 else self.Q2
        
        # Obliczanie kowariancji innowacji
        S = self.H * P_pred * self.H + self.R + szum_procesu
        
        # Obliczanie wzmocnienia Kalmana
        K = P_pred * self.H / S

        # Aktualizacja estymacji stanu
        self.x = x_pred + K * y
        
        # Aktualizacja niepewności estymacji
        self.P = (self.I - K * self.H) * P_pred
        
        return self.x

    def run(self):
        """
        Główna pętla filtracji Kalmana
        Zwraca:
            x_estimates: Lista wyestymowanych wartości
            P: Końcowa wartość niepewności
        """
        x_estimates = []
        
        # Przetwarzanie wszystkich pomiarów
        for z in self.noised_signals_height:
            # Faza predykcji
            x_pred, P_pred = self.prediction()
            
            # Faza aktualizacji
            x = self.update(z=z, x_pred=x_pred, P_pred=P_pred)
            
            x_estimates.append(x)
            
        return x_estimates, self.P