""" 
                #Recorriendo los pagos para obtener el diario y el codigo de moneda del pago 
                for pago in total_pays:
                    if pago.get('journal_id')[1] in diarios_de_caja:
                        print("----------->>>>" + str(pago.get('journal_id')[1]))
                        if pago.get('currency_id')[1] == 'VES':
                            print("----------->>>>" + str(pago.get('currency_id')[1]))
                            count_payment += 1
                            diarios_pagos.write("\n" + str(pago.get('journal_id')) + " " + str(pago.get('amount')) + " " + str(pago.get('currency_id')[1]))
                print(payment_data"""


#Obtenemos la tasa para cada una de las fechas de los pagos en account_payment_widget
        for pay in pay_content: #content contiene los pagos del cliente (uno o varios pagos - es un arreglo de diccionarios)
            payment_id = pay['account_payment_id']
            print(payment_id)
            ###### REALIZAR CONSULTA PARA OBTENER ID DE PAGO Y EL CREADOR PARA APLICAR LOS FILTROS ######
            fields_payment = [
                'create_uid', 
                'journal_id', 'amount', 'currency_id',
                'amount', 'date', 'payment_method_name', 'move_id']

            payment_data = models.execute_kw(db, uid, api_key, 'account.payment', 'read', [payment_id], {'fields': fields_payment})
            print(payment_data)
            """ 
            #consultar tasas para pagos
            currency_code = 'VES'
            # Determinar montos totales (se realiza consulta de la tasa a través de API)
            currency_id = models.execute_kw(db, uid, password, 'res.currency', 'search', [[('name', '=', currency_code)]])
                    
            consulta_fecha = payment_data[0].get('date')
                
            if currency_id:
                # 1. Intentar obtener la tasa de cambio para la fecha específica
                rate = models.execute_kw(
                    db,
                    uid,
                    assword,
                    'res.currency.rate',
                    search_read',
                    [[
                        ('currency_id', '=', currency_id[0]),
                        ('name', '=', consulta_fecha)  # Buscar por la fecha exacta
                    ]],
                        {'fields': ['name', 'company_rate', 'currency_id']}
                    )

                    if rate:
                        # Se encontró la tasa para la fecha específica
                        #print(f"Fecha: {rate[0]['name']}, Tasa: {rate[0]['company_rate']}")
                        payment_data[0]['rate'] = rate[0]['company_rate']
                    else:
                        # 2. Si no encuentra, buscar la fecha más cercana anterior
                        nearest_rate = models.execute_kw(
                            db,
                            uid,
                            password,
                            'res.currency.rate',
                            'search_read',
                            [[
                                ('currency_id', '=', currency_id[0]),
                                ('name', '<', consulta_fecha)  # Buscar la fecha más cercana anterior
                            ]],
                            {'fields': ['name', 'company_rate', 'currency_id'], 'limit': 1}  # Mueve 'limit' aquí en el diccionario de opciones
                        )
                        if nearest_rate:
                            #print(f"No se encontró la tasa para la fecha {consulta_fecha}. Se usará la tasa más cercana anterior.")
                            #print(f"Fecha: {nearest_rate[0]['name']}, Tasa: {nearest_rate[0]['company_rate']}")
                            payment_data[0]['rate'] = nearest_rate[0]['company_rate']
                        else:
                            print("No se encontró ninguna tasa de cambio disponible para la moneda.")
            else:
                        print("No se encontró ninguna moneda con ese código.")
                total_pays.append(payment_data[0]) #Puede ser un diccionario que contenga informacion de pagos + tasa
                #print(" - - - - - - " + str(total_pays) + " - - - - - - ")
            else:
                print("- - - - CLIENTE POSIBLEMENTE TIENE DESCUENTO - - - -")

            """