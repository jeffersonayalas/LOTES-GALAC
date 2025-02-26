def process_payment(self):
        url = self.api_data.get('url')
        db = self.api_data.get('db')
        username = self.api_data.get('username')
        api_key = self.api_data.get('api_key')
        password = self.api_data.get('password')

        montos = []

        process_data = open("process_payment.txt", 'a')
        process_data.write("\n###########################################################################################################")
        
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


        #print(type(self.widget_pagos))
        # Verifica si self.widget_pagos no es un booleano
        if self.widget_pagos != 'false':
            # Verifica el contenido de invoice_payments_widget
            if isinstance(self.info.get("invoice_payments_widget"), str):
                try:
                    self.pagos = json.loads(self.info["invoice_payments_widget"])["content"]
                    # Asegúrate de que 'content' realmente esté en self.pagos
                    if isinstance(self.pagos, list):  # Verifica que sea una lista
                        for pay in self.pagos:
                            name_payment = pay.get('name', 'Sin nombre')
                            diary = pay.get('journal_name', 'Sin diario')
                            amount = pay.get('amount', 0)
                            currency = pay.get('currency', 'Sin moneda')
                            date = pay.get('date', 'Sin fecha')
                            payment_id = pay.get('payment_id', 'Sin ID de pago')
                            payment_method = pay.get('payment_method_name', 'Sin método de pago')
                            move_id = pay.get('move_id', 'Sin ID de movimiento')
                            ref = pay.get('ref', 'Sin referencia').replace("\\n", "").replace("\n", "")
                            print(type(ref))
                            process_data.write(f"\n- - - - - Nombre: {name_payment} Diario: {diary} Monto de pago: {amount} Moneda: {currency} Fecha: {date} ID de pago: {payment_id} Método de pago: {payment_method} ID de factura: {move_id} Referencia de pago: {ref} - - - - -")
                            
                            currency_code = 'VES' 
                            #Determinar montos totales (se realiza consulta de la tasa a traves de API)
                            currency_id = models.execute_kw(db, uid, password, 'res.currency', 'search', [[('name', '=', currency_code)]])
                            montos.append(amount)

                            consulta_fecha = date
                            print(consulta_fecha)
                            if currency_id:
                                # 1. Intentar obtener la tasa de cambio para la fecha específica
                                rate = models.execute_kw(
                                    db,
                                    uid,
                                    password,
                                    'res.currency.rate',
                                    'search_read',
                                    [[
                                        ('currency_id', '=', currency_id[0]),
                                        ('name', '=', consulta_fecha)  # Buscar por la fecha exacta
                                    ]],
                                    {'fields': ['name', 'company_rate', 'currency_id']}
                                )

                                if rate:
                                    # Se encontró la tasa para la fecha específica
                                    print(rate)
                                    print(f"Fecha: {rate[0]['name']}, Tasa: {rate[0]['company_rate']}")
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
                                        print(f"No se encontró la tasa para la fecha {consulta_fecha}. Se usará la tasa más cercana anterior.")
                                        print(f"Fecha: {nearest_rate[0]['name']}, Tasa: {nearest_rate[0]['company_rate']}")
                                    else:
                                        print("No se encontró ninguna tasa de cambio disponible para la moneda.")
                            else:
                                print("No se encontró ninguna moneda con ese código.")

                    else:
                        print("El contenido no es una lista válida.")
                except json.JSONDecodeError:
                    print("Error al decodificar JSON. Asegúrate de que el formato sea correcto.")
            else:
                print("El valor de invoice_payments_widget no es un string válido.")
        