import simulationBuilder as sim
import signalsGeneratingShowing as signals
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

default_folder = r""

simulation_signal_dict = {
    "speed": 2,
    "start_height": 0,
    "time_step": 0.05,
    "flight_time": 600
}

def save_data_to_json(
    signals_y: list,
    signals_x: list,
    noised_signals_y_1: list,
    estimated_signals_y_1: list,
    noised_signals_y_2: list,
    estimated_signals_y_2: list,
    combined_estimated_y: list,
    kalman_step: float,
    parent_window: tk.Toplevel
):
    if not (len(signals_y) == len(signals_x) == len(noised_signals_y_1) == len(noised_signals_y_2)):
        raise ValueError("Długości sygnałów muszą być równe")
    
    if not (len(estimated_signals_y_1) == len(estimated_signals_y_2) == len(combined_estimated_y)):
        raise ValueError("Długości estymowanych sygnałów muszą być równe")

    save_window = tk.Toplevel()
    save_window.withdraw()

    

    json_file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        initialfile = "symulacja",
        filetypes=[("Pliki JSON", "*.json"), ("Wszystkie pliki", "*.*")],
        title="Zapisz plik JSON symulacji",
        parent=save_window,
        initialdir=default_folder
    )

    if not json_file_path:
        save_window.destroy()
        print("Anulowano zapis")
        return

    data = {
        "signals_y": signals_y,
        "signals_x": signals_x,
        "noised_signals_y_1": noised_signals_y_1,
        "noised_signals_y_2": noised_signals_y_2,
        "estimated_signals_y_1": estimated_signals_y_1,
        "estimated_signals_y_2": estimated_signals_y_2,
        "combined_estimated_y": combined_estimated_y,
        "kalman_step": kalman_step
    }

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Plik został zapisany: {json_file_path}")

    txt_file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile = "szczegóły_symulacji",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")],
        title="Zapisz parametry symulacji",
        parent=save_window,
        # initialdir=default_folder
    )
    std_noisy_sensor_1, std_filtred_sensor_1 = calculate_std_errors(signals_y,noised_signals_y_1,estimated_signals_y_1)
    std_noisy_sensor_2, std_filtred_sensor_2 = calculate_std_errors(signals_y,noised_signals_y_2,estimated_signals_y_2)
    std_noisy_sensor_combined, std_filtred_sensor_combined = calculate_std_errors(signals_y,combined_estimated_y,estimated_signals_y_1)
    reduction_percentage = calculate_reduction_percentage(std_noisy_sensor_1, std_filtred_sensor_combined)

    if txt_file_path:
        try:
            with open(txt_file_path, 'w', encoding='utf-8') as f:
                for key, value in simulation_signal_dict.items():
                    f.write(f"{key}: {value}\n")
                f.write("Wyniki statystyczne:")
                f.write(f"\nOdchylenie standardowe sygnałów zaszumowanych na pierwszym sensorze: {std_noisy_sensor_1}")
                f.write(f"\nOdchylenie standardowe sygnałów odfiltrowanych na pierwszym sensorze: {std_filtred_sensor_1}")
                f.write(f"\nOdchylenie standardowe sygnałów zaszumowanych na drugim sensorze: {std_noisy_sensor_2}")
                f.write(f"\nOdchylenie standardowe sygnałów odfiltrowanych na drugim sensorze: {std_filtred_sensor_2}")
                f.write(f"\nOdchylenie standardowe sygnałów odfiltrowanych na połączonych sensorach: {std_filtred_sensor_combined}")
                f.write(f"\nProcentowa redukcja odchylenia standardowego: {reduction_percentage:.2f}%")

            print(f"Parametry zapisano do: {txt_file_path}")
        except Exception as e:
            messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać parametrów: {str(e)}")
    else:
        print("Anulowano zapis parametrów")

    save_window.destroy()
    parent_window.destroy()

def combine_estimates(y1, P1, y2, P2):
    y_combined = (P2 * y1 + P1 * y2) / (P1 + P2)
    P_combined = (P1 * P2) / (P1 + P2)
    return y_combined, P_combined

def calculate_std_errors(real_values, noisy_values, filtered_values):
    """
Oblicza odchylenie standardowe błędów dla zaszumionego oraz odfiltrowanego sygnału.

Parametry:
    real_values (list lub np.array): Rzeczywiste wartości sygnału.
    noisy_values (list lub np.array): Zaszumione wartości sygnału.
    filtered_values (list lub np.array): Odfiltrowane wartości sygnału.

Zwraca:
    tuple: (std_noisy, std_filtered)
        std_noisy    - odchylenie standardowe błędu zaszumionego sygnału,
        std_filtered - odchylenie standardowe błędu odfiltrowanego sygnału.
"""
    real = np.array(real_values)
    noisy = np.array(noisy_values)
    filtered = np.array(filtered_values)
    
    error_noisy = noisy - real
    
    error_filtered = filtered - real

    std_noisy = np.std(error_noisy)
    std_filtered = np.std(error_filtered)

    return std_noisy, std_filtered

def calculate_reduction_percentage(std_noisy, std_filtered):
    """
    Oblicza procentową redukcję odchylenia standardowego błędu.

    Parametry:
        std_noisy (float): odchylenie standardowe błędu zaszumionego sygnału.
        std_filtered (float): odchylenie standardowe błędu odfiltrowanego sygnału.

    Zwraca:
        float: procentowa redukcja odchylenia standardowego, obliczana jako:
               ((std_noisy - std_filtered) / std_noisy) * 100.
               Jeśli std_noisy wynosi 0, zwraca 0.
    """
    if std_noisy != 0:
        reduction_percentage = ((std_noisy - std_filtered) / std_noisy) * 100
    else:
        reduction_percentage = 0
    return reduction_percentage

def show_random():
    signals_x, signals_y = signals.generate_true_signal(simulation_signal_dict)
    estimated_signals_y_1, P1, kalman_step_1, noised_signals_y_1 = sim.KalmanSimulation(
        signals_dict=simulation_signal_dict, 
        signals_x=signals_x, 
        signals_y=signals_y, 
        sensor_id=1
    )
    estimated_signals_y_2, P2, kalman_step_2, noised_signals_y_2 = sim.KalmanSimulation(
        signals_dict=simulation_signal_dict, 
        signals_x=signals_x, 
        signals_y=signals_y, 
        sensor_id=2
    )

    combined_estimates_y = []
    combined_P = []
    for y1, y2 in zip(estimated_signals_y_1, estimated_signals_y_2):
        y_combined, P_combined = combine_estimates(y1, P1, y2, P2)
        combined_estimates_y.append(y_combined)
        combined_P.append(P_combined)

    print("Połączona wariancja:", combined_P[-1])
    print("Średnia połączonych estymatów:", sum(combined_estimates_y)/len(combined_estimates_y))

    signals.show_result(
        signals_x=signals_x, 
        signals_y=signals_y, 
        noised_signals_y=signals.generate_noised_signals_on_sensor(signals_y),
        # noised_signals_y=noised_signals_y_2,
        taked_kalman_signals_x=signals_x[0::1], 
        y_estimates_kalman=combined_estimates_y, 
        sensor_id="Połączone"
    )
    
    save_root = tk.Toplevel()
    save_root.title("Zapisz symulację")

    open_button = tk.Button(
        save_root, 
        text="Zapisz", 
        command=lambda: save_data_to_json(
            signals_x=signals_x,
            signals_y=signals_y, 
            noised_signals_y_1=noised_signals_y_1, 
            noised_signals_y_2=noised_signals_y_2,
            estimated_signals_y_1=estimated_signals_y_1,
            estimated_signals_y_2=estimated_signals_y_2, 
            combined_estimated_y=combined_estimates_y, 
            kalman_step=kalman_step_1,
            parent_window=save_root
        )
    )
    open_button.pack(pady=20)

def show_from_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Wybierz plik JSON",
        filetypes=[("Pliki JSON", "*.json")],
        initialdir=r"C:\Users\yaros\PythonProjectrs\OurProjectNIDUC\dataFolder"
    )
        
    if file_path:
        print(f"Wybrano plik JSON: {file_path}")
        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                sim.showSimulationFromFile(json_data)
        except Exception as e:
            print(f"Błąd odczytu pliku JSON: {e}")
    else:
        print("Nie wybrano pliku.")
    root.destroy()

def main_screen():
    root = tk.Tk()
    root.title("Panel sterowania symulacją")
    root.geometry("300x100")
    
    button_frame = tk.Frame(root, padx=20, pady=20)
    button_frame.pack(expand=True)
    
    new_sim_btn = tk.Button(
        button_frame,
        text="Nowa symulacja",
        command=open_parameter_window,
        width=20
    )
    new_sim_btn.pack(pady=5)
    
    load_btn = tk.Button(
        button_frame,
        text="Wczytaj z pliku",
        command=show_from_file,
        width=20
    )
    load_btn.pack(pady=5)

    root.mainloop()

def open_parameter_window():
    param_window = tk.Toplevel()
    param_window.title("Ustawienia parametrów symulacji")
    
    entries = {}
    for i, (key, value) in enumerate(simulation_signal_dict.items()):
        label_text = key.replace('_', ' ').title() + ":"
        label = tk.Label(param_window, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
        
        entry = tk.Entry(param_window)
        entry.insert(0, str(value))
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[key] = entry

    def on_run_click():
        try:
            new_params = {}
            for key in simulation_signal_dict:
                value = entries[key].get()
                if key in ["speed", "start_height", "time_step"]:
                    new_params[key] = float(value)
                elif key == "flight_time":
                    new_params[key] = int(value)
            
            simulation_signal_dict.update(new_params)
            param_window.destroy()
            show_random()
        except ValueError as e:
            messagebox.showerror("Błąd wejścia", f"Nieprawidłowy format danych: {e}")

    run_btn = tk.Button(
        param_window,
        text="Uruchom symulację",
        command=on_run_click,
        width=15
    )
    run_btn.grid(row=len(simulation_signal_dict), columnspan=2, pady=10)

def main():
    main_screen()

if __name__ == "__main__":
    main()