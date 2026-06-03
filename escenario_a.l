init_grid(bateria_b1, linea_carga)

mientras 1 == 1 ejecutar
    temp_actual = leer_temperatura(bateria_b1)
    
    si temp_actual > 55 entonces
        conmutar_linea(linea_carga, OFF)
    fin_si
fin_mientras
