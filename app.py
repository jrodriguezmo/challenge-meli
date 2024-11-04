from flask import Flask, jsonify, request
import psutil  # Librería para obtener información del sistema (instala con `pip install psutil`)
import subprocess

app = Flask(__name__)

# Endpoint para obtener el uso de un dispositivo específico o de todos los dispositivos
from flask import Flask, jsonify, request
import psutil  # Librería para obtener información del sistema
import subprocess
import platform

app = Flask(__name__)

# Endpoint para obtener el uso de un dispositivo específico o de todos los dispositivos
@app.route('/device_usage', methods=['GET'])
def get_device_usage():
    # Detectar el sistema operativo
    os_type = platform.system()
    device = request.args.get('device')  # Obtener el parámetro "device" de la URL
    
    disk_usage = {}
    try:
        # Para Windows: Si se especifica un dispositivo como "C:"
        if os_type == "Windows":
            if device:
                # Formato en Windows requiere una unidad (por ejemplo, "C:\\")
                if not device.endswith(':\\'):
                    device = device + ':\\'
                usage = psutil.disk_usage(device)
                disk_usage[device] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            else:
                # Si no se especifica, devolver el uso de todas las unidades montadas
                for part in psutil.disk_partitions():
                    usage = psutil.disk_usage(part.mountpoint)
                    disk_usage[part.device] = {
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    }

        # Para Linux: Las rutas de dispositivos son como "/dev/sda1"
        elif os_type == "Linux":
            if device:
                # Verificar si el dispositivo tiene formato de Linux
                usage = psutil.disk_usage(device)
                disk_usage[device] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            else:
                # Si no se especifica un dispositivo, devolver el uso de todos los dispositivos
                for part in psutil.disk_partitions():
                    usage = psutil.disk_usage(part.mountpoint)
                    disk_usage[part.device] = {
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    }
        else:
            return jsonify({"error": "Unsupported OS type"}), 400

        return jsonify(disk_usage), 200

    except Exception as e:
        return jsonify({"error": f"Device {device} not found: {e}"}), 400

# Endpoint para ejecutar un script interno
@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        # Ejecutar un comando o script interno (aquí se usa un comando de ejemplo)
        result = subprocess.run(['echo', 'Script ejecutado'], capture_output=True, text=True)
        return jsonify({"output": result.stdout.strip()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
