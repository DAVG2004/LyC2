import time

class HALSimulator:
    """
    Capa de Abstracción de Hardware (Hardware Abstraction Layer).
    Simula sensores térmicos, baterías y relés.
    """
    def __init__(self):
        self.temperaturas = {
            'bateria_b1': 45.0  # Comienza en 45 grados (Escenario A)
        }
        self.cargas = {
            'bat_principal': 25.0 # Comienza en 25% de carga (Escenario B)
        }
        self.reles = {
            'linea_carga': 'ON',
            'cargas_secundarias': 'ON'
        }
        print("[HAL] Sistema simulado inicializado.")

    def registrar_componentes(self, componentes):
        print(f"[HAL] Registrando componentes en la red: {', '.join(componentes)}")

    def leer_temperatura(self, id_sensor):
        # Para simular, aumentamos la temperatura cada vez que la leemos (para forzar la alarma)
        if id_sensor in self.temperaturas:
            t = self.temperaturas[id_sensor]
            self.temperaturas[id_sensor] += 3.5 # simular calentamiento rápido
            print(f"  [SENSOR] Termopar '{id_sensor}' reporta: {t} °C")
            time.sleep(0.3)
            return t
        return 0.0

    def estado_carga(self, id_bateria):
        # Simulamos descarga de la batería principal
        if id_bateria in self.cargas:
            c = self.cargas[id_bateria]
            
            # Si las cargas secundarias están apagadas, la batería se recupera rápido
            if self.reles.get('cargas_secundarias') == 'OFF':
                self.cargas[id_bateria] += 8.0 # Simular recarga 
            else:
                self.cargas[id_bateria] -= 5.0 # Simular descarga
            
            # Limitar max y min
            if self.cargas[id_bateria] > 100: self.cargas[id_bateria] = 100
            if self.cargas[id_bateria] < 0: self.cargas[id_bateria] = 0
            
            print(f"  [BMS] Batería '{id_bateria}' reporta SoC: {c}%")
            time.sleep(0.3)
            return c
        return 0.0

    def conmutar_linea(self, id_linea, estado):
        self.reles[id_linea] = estado
        print(f"\n==========================================")
        print(f" [ALERTA HAL] RELÉ ACCIONADO FISICAMENTE")
        print(f" | Linea de poder: '{id_linea}'")
        print(f" | Nuevo Estado: {estado}")
        print(f"==========================================\n")
