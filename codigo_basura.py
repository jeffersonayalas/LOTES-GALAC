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