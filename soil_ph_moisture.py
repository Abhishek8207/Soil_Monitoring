import spidev
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Function to read data from a channel on MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data
    
# Route to get both moisture and pH levels
@app.route('/sensors', methods=['GET'])
def get_sensor_data():
    moisture_level = read_channel(0)  # Soil moisture sensor on CH0
    ph_level = read_channel(1)        # pH sensor on CH1
    return jsonify({
        'moisture': moisture_level,
        'ph': ph_level
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
