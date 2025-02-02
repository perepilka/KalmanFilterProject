import numpy as np
import random
import matplotlib.pyplot as plt




def generate_true_signal(signals_dict: dict):
    """
    Generuje idealny sygnał wysokości w funkcji czasu.
    
    Parametry:
    signals_dict (dict): Słownik parametrów symulacji:
        - speed: prędkość zmian wysokości [m/s]
        - start_height: początkowa wysokość [m]
        - time_step: krok czasowy [s]
        - flight_time: całkowity czas lotu [s]
    """
    signals_x = []
    signals_y = []
    
    height_changes_speed = signals_dict.get("speed", 2)
    start_height = signals_dict.get("start_height", 0)
    time_step = signals_dict.get("time_step", 0.05)
    flight_time = signals_dict.get("flight_time", 600)

    max_steps = int(flight_time / time_step)
    
    
    for i in range(max_steps):
        current_time = round(time_step * i, 3)
        calculated_y = start_height + height_changes_speed * current_time
        
        # Obcinamy wartości ujemne do zera
        current_y = max(calculated_y, 0.0)
        
        signals_y.append(round(current_y, 3))
        signals_x.append(current_time)

    return signals_x, signals_y

def generate_noised_signals_on_sensor(signals_y):
    """
    Generuje zaszumione pomiary radarowe z różnymi poziomami szumu.
    
    Parametry:
    signals_y (list): Lista idealnych wartości wysokości
    
    Zwraca:
    list: Zaszumione pomiary wysokości
    """
    noised_signals_y = []
    radar_noise_under_152_4m = 0.03  # Szum poniżej 152.4 m (3%)
    radar_noise_higher_152_4m = 0.05  # Szum powyżej 152.4 m (5%)

    for signal in signals_y:
        if signal <= 152.4:
            noise = random.uniform(-radar_noise_under_152_4m, radar_noise_under_152_4m)
        elif 152.4 < signal <= 762:
            noise = random.uniform(-radar_noise_higher_152_4m, radar_noise_higher_152_4m)
        else:
            noise = 0  # Brak szumu powyżej 762 m
        noised_signal = round(signal + signal * noise, 3)
        noised_signals_y.append(noised_signal)

    return noised_signals_y


def generate_noised_signals_on_damaged_sensor(signals_y):
    noised_signals_y = []
    radar_noise_under_152_4m = 0.03  # Szum poniżej 152.4 m (3%)
    radar_noise_higher_152_4m = 0.05  # Szum powyżej 152.4 m (5%)

    for signal in signals_y:
        if signal <= 152.4:
            noise = random.uniform(-radar_noise_under_152_4m, radar_noise_under_152_4m)
        elif 152.4 < signal <= 762:
            noise = random.uniform(-radar_noise_higher_152_4m, radar_noise_higher_152_4m)
        else:
            noise = 0  # Brak szumu powyżej 762 m
        noised_signal = round(signal + signal * noise, 3)
        noised_signals_y.append(noised_signal)

    return noised_signals_y


def show_signal(signals_x, signals_y, 
                xlabel="Czas (s)", 
                ylabel="Wysokość (m)", 
                title="Wykres sygnału"):
    """
    Wizualizacja pojedynczego sygnału
    
    Parametry:
    signals_x (list): Wartości czasu
    signals_y (list): Wartości wysokości
    """
    plt.plot(signals_x, signals_y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.show()

def show_result(signals_x, signals_y, noised_signals_y, 
                taked_kalman_signals_x, y_estimates_kalman, sensor_id):
    """
    Wizualizacja porównawcza sygnałów: 
    idealnego, zaszumionego i przefiltrowanego
    
    Parametry:
    sensor_id (str): Identyfikator czujnika
    """
    plt.plot(signals_x, signals_y, label="Sygnał idealny")
    plt.plot(signals_x, noised_signals_y, label="Sygnał zaszumiony")
    plt.plot(taked_kalman_signals_x, y_estimates_kalman, label="Sygnał przefiltrowany")
    plt.xlabel("Czas (s)")
    plt.ylabel("Wysokość (m)")
    plt.title(f"Porównanie sygnałów [{sensor_id}]")
    plt.legend()
    plt.grid()
    plt.show()

def show_result_json(signals_x, signals_y, noised_signals_y, 
                    taked_kalman_signals_x, y_estimates_kalman):
    """
    Wizualizacja wyników z pliku JSON
    """
    plt.plot(signals_x, signals_y, label="Sygnał idealny")
    plt.plot(signals_x, noised_signals_y, label="Sygnał zaszumiony")
    plt.plot(taked_kalman_signals_x, y_estimates_kalman, label="Sygnał przefiltrowany")
    plt.xlabel("Czas (s)")
    plt.ylabel("Wysokość (m)")
    plt.title("Połączone przefiltrowane sygnały")
    plt.legend()
    plt.grid()
    plt.show()