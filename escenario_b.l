init_grid(bat_principal, cargas_secundarias)

mientras 1 == 1 ejecutar
    carga_sistema = estado_carga(bat_principal)
    
    si carga_sistema < 20 entonces
        conmutar_linea(cargas_secundarias, OFF)
    fin_si
    
    si carga_sistema > 40 entonces
        conmutar_linea(cargas_secundarias, ON)
    fin_si
fin_mientras
