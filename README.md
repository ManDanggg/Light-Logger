# Light Logger

An Arduino reads a photoresistor and streams light levels over USB. A Python script plots the readings live, smooths them with a moving average, alerts when it gets dark, and saves everything to a CSV file.

![Live plot](images/plot.png)

## How it works

1. **Sensor:** a photoresistor and a 10 kΩ resistor form a voltage divider. More light means lower resistance, which raises the voltage at pin A0.
2. **Arduino:** reads A0 ten times a second (`analogRead`, 0 to 1023), sends each value over serial, and turns on an LED when the reading drops below a threshold.
3. **Python:** reads the serial stream with `pyserial`, keeps the latest readings in a NumPy array, computes a 10-sample moving average with `np.convolve`, and updates a Matplotlib plot in real time.

## Hardware

- Arduino UNO R3
- Photoresistor + 10 kΩ resistor (voltage divider on A0)
- LED + 220 Ω resistor (pin 9)

![Wiring](images/wiring.jpg)

## Run it

1. Upload `arduino/light_logger/light_logger.ino` with the Arduino IDE.
2. Close the Arduino Serial Monitor (only one program can use the port).
3. Install dependencies: `pip install -r requirements.txt`
4. Set `PORT` in `python/logger.py` to your board's port.
5. Run `python python/logger.py`. Close the plot window to save `light_log.csv`.

## What I learned
- I learned how to use a voltage divider to reduce signal so microcontroller can read it safely
- I learned how we can use serial communication to connect the Arduino with the computer
- 


## Next steps

- For the next step, I can probably plot for a full day and see the light pattern. 
