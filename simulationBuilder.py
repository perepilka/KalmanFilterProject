from filters import KalmanFilter as KF
import signalsGeneratingShowing as signals
import pandas as pd
import json

def KalmanSimulation(signals_dict: dict, signals_x, signals_y, sensor_id, Q1=4.572, Q2=38.1):
    """
    Przeprowadza pełną symulację filtracji Kalmana dla jednego czujnika
    
    Parametry:
    signals_dict (dict): Słownik parametrów symulacji
    signals_x (list): Lista wartości czasu
    signals_y (list): Lista idealnych wartości wysokości
    sensor_id (str/num): Identyfikator czujnika
    Q1 (float): Szum procesu dla niskich wysokości
    Q2 (float): Szum procesu dla wysokich wysokości
    
    Zwraca:
    tuple: (wyestymowane wartości, wariancja, krok Kalmana, zaszumione sygnały)
    """
    kalman_step = 1  # Krok próbkowania dla filtracji
    
    # Generowanie zaszumionych sygnałów
    noised_signals_y = signals.generate_noised_signals_on_sensor(signals_y)
    
    # Pobieranie sygnałów z odpowiednim krokiem
    taked_kalman_signals_x = signals_x[0::kalman_step]
    taked_kalman_signals_y = noised_signals_y[0::kalman_step]
    
    # Wizualizacja surowych danych wejściowych
    signals.show_signal(taked_kalman_signals_x, taked_kalman_signals_y, 
                      title=f"Surowe sygnały wejściowe [{sensor_id}]")
    
    # Inicjalizacja i uruchomienie filtru Kalmana
    kalman_filter = KF(v=signals_dict["speed"], 
                      noised_signals_height=taked_kalman_signals_y, 
                      Q1=Q1, Q2=Q2)
    y_estimates_kalman, P = kalman_filter.run()
    
    # Wizualizacja wyników filtracji
    signals.show_signal(taked_kalman_signals_x, y_estimates_kalman, 
                      title=f"Przefiltrowane sygnały [{sensor_id}]")
    
    # Porównanie wszystkich sygnałów
    signals.show_result(signals_x=signals_x,
                      signals_y=signals_y,
                      noised_signals_y=noised_signals_y,
                      taked_kalman_signals_x=taked_kalman_signals_x,
                      y_estimates_kalman=y_estimates_kalman,
                      sensor_id=sensor_id)
    
    return y_estimates_kalman, P, kalman_step, noised_signals_y

def showSimulationFromFile(json_data):
    """
    Wczytuje i wizualizuje zapisaną symulację z pliku JSON
    
    Parametry:
    json_data (dict): Wczytane dane z pliku JSON
    """
    # Ekstrakcja danych z formatu JSON
    signals_x = json_data['signals_x']
    signals_y = json_data['signals_y']
    noised_signals_y_1 = json_data['noised_signals_y_1']
    noised_signals_y_2 = json_data['noised_signals_y_2']
    estimated_signals_y_1 = json_data['estimated_signals_y_1']
    estimated_signals_y_2 = json_data['estimated_signals_y_2']
    combined_estimated_y = json_data['combined_estimated_y']
    kalman_step = json_data['kalman_step']
    
    # Wizualizacja danych z pierwszego czujnika
    signals.show_signal(signals_x=signals_x[0::kalman_step], 
                      signals_y=noised_signals_y_1[0::kalman_step],
                      title="Surowe sygnały wejściowe [Czujnik 1]")
    
    # Wizualizacja danych z drugiego czujnika
    signals.show_signal(signals_x=signals_x[0::kalman_step], 
                      signals_y=noised_signals_y_2[0::kalman_step],
                      title="Surowe sygnały wejściowe [Czujnik 2]")
    
    # Wyświetlenie połączonych wyników
    signals.show_result_json(signals_x=signals_x,
                           signals_y=signals_y,
                           noised_signals_y=noised_signals_y_1,
                           y_estimates_kalman=combined_estimated_y,
                           taked_kalman_signals_x=signals_x[0::kalman_step])