# **Kalman Filter-Based Signal Simulation and Noise Reduction**

This project simulates signal generation and processing using Kalman filtering techniques to reduce noise in radar-detected altitude signals.

## **Project Structure**
- `main.py`: Main application with a graphical user interface (GUI) for running simulations, adjusting parameters, and loading data from saved files.
- `simulationBuilder.py`: Contains the simulation logic, including signal noise simulation and the Kalman filtering process.
- `signalsGeneratingShowing.py`: Functions for generating, visualizing, and comparing signals.
- `filters.py`: Implementation of the Kalman filter for signal estimation and noise reduction.

---

## **Features**
- Generate ideal and noisy altitude signals using random noise.
- Apply the Kalman filter to noisy signals to estimate the true signal.
- Visualize and compare the ideal, noisy, and filtered signals.
- Save simulation data and parameters to JSON or text files for later analysis.
- Load saved simulation data and visualize it.

---

## **Installation**

### Prerequisites
- **Python** >= 3.8
- Required packages (can be installed via `pip`):
  ```bash
  pip install numpy matplotlib
  ```

### Running the Application
Clone the repository and navigate to the project directory:
```bash
git clone <repository_url>
cd <repository_directory>
```

Run the application using:
```bash
python main.py
```

---

## **Setting the Default Folder**
For convenient file saving, you can set a default folder where all simulations and parameters will be saved. The default value in the project is:
```python
default_folder = r""
```
However, you can customize this path according to your preference by changing the value of `default_folder` in `main.py`. For example:
```python
default_folder = r"C:\Your\Custom\Path\To\Save\Data"
```
This ensures that when saving or loading files, the application will point to the specified directory by default.

---

## **Usage**

### **1. New Simulation**
- Open the application and select **"Nowa symulacja"**.
- Adjust simulation parameters such as:
  - `speed`: Speed of height change
  - `start_height`: Initial altitude
  - `time_step`: Time step between measurements
  - `flight_time`: Total simulation time
- Run the simulation, visualize the results, and save the data.

### **2. Load from File**
- Select **"Wczytaj z pliku"** to load a previously saved JSON file containing simulation results.
- Visualize the ideal, noisy, and filtered signals.

---

## **Core Functions**

### Signal Generation (`signalsGeneratingShowing.py`)
- **`generate_true_signal()`**: Creates an ideal altitude signal based on user-defined parameters.
- **`generate_noised_signals_on_sensor()`**: Introduces random noise to simulate radar measurement errors.

### Simulation (`simulationBuilder.py`)
- **`KalmanSimulation()`**: Simulates noisy signal processing using the Kalman filter.
- **`showSimulationFromFile()`**: Loads and visualizes saved simulation data.

### Kalman Filter (`filters.py`)
- **`KalmanFilter`**: Implements prediction and update phases of the Kalman filter to estimate the true signal.

---

## **Data Saving and Visualization**
- Simulation data is saved as a JSON file containing signals and Kalman filter estimates.
- Statistical parameters, such as noise reduction percentages, are saved to text files.
- Visualization functions display comparisons of ideal, noisy, and filtered signals.

---

## **Example Output**
![Example Signal Output](dataFolder\Symulacja_2\wynik.png)  
*Visualization of ideal, noisy, and filtered signals.*

---

## **Contributors**
- Your Name(s)
- Project collaborators (if any)

## **License**
This project is licensed under the MIT License. Feel free to use, modify, and distribute.

