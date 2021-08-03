#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522Update import MFRC522Update
import json

reader=MFRC522Update()

def general():
  inf=0
  sku=0
  lote=0
  cantidad=0
  fecha=0
  lista_sku=0
  opcion_1=int(input("Bienvenido, que desea hacer: (Escribir - 1) - (Leer - 2) \n"))
  if opcion_1 ==1:
    opcion_1_1=int(input("(Nuevo Tag - 1) - (Tag Existente - 2): \n"))
    if opcion_1_1==1:
      inf=str(input("Codigo Localizacion: "))
      sku=str(input("Nuevo SKU: "))
      lote=str(input("Lote: "))
      cantidad=str(input("Cantidad: "))
      fecha=str(input("Fecha de Vencimiento (dd-mm-aaaa): "))
      print("Acerque el TAG")
      
      write = str('["' + sku + '",' + '"'+lote+'",'+cantidad+',"'+fecha+'"]')
      reader.write_no_block(write, 1)
      write=str('["'+inf+'",'+'["'+sku+'"]]')
      GPIO.cleanup()
      reader1=MFRC522Update()
      reader1.write_no_block(write, 0)
    else:
      print("Acerque el TAG")
      GPIO.cleanup()
      reader1=MFRC522Update()
      id,text=reader1.read_no_block(0)
      list_info=json.loads(text)
      print("Codigo Localizacion: "+list_info[0])
      cant_sku=len(list_info[1])
      print("SKUs guardados: ")
      for i in range(0,cant_sku):
          j=i+1
          print(j,". ",list_info[1][i])
      opcion_2_1=int(input("(Mod. cantidad de un registro - 1) - (Agregar un Registro - 2) - (Eliminar un Registro - 3): \n"))
      if opcion_2_1==1:
          opcion_2_1_1=int(input("Indique el # del registro a modificar: \n"))
          GPIO.cleanup()
          reader2=MFRC522Update()
          id,text1=reader2.read_no_block(opcion_2_1_1)
          print(text1)
          list_info_sku=json.loads(str(text1))
          n_cant=int(input("Ingrese la nueva cantidad: \n"))
          list_info_sku[2]=n_cant
          list_info_sku=json.dumps(list_info_sku)
          GPIO.cleanup()
          reader3=MFRC522Update()
          reader3.write_no_block(list_info_sku,opcion_2_1_1)
      elif opcion_2_1==2:
          print("Nuevo Registro \n")
          if(cant_sku<4):
              sku = str(input("Nuevo SKU: "))
              lote = str(input("Lote: "))
              cantidad = str(input("Cantidad: "))
              fecha = str(input("Fecha de Vencimiento (dd-mm-aaaa): "))
              write = str('["' + sku + '",' + '"' + lote + '",' + cantidad + ',"' + fecha + '"]')
              GPIO.cleanup()
              reader4=MFRC522Update()
              reader4.write_no_block(write,cant_sku+1)
              GPIO.cleanup()
              reader5=MFRC522Update()
              id,text=reader5.read_no_block(0) 
              list_info=json.loads(text)
              list_info[1].append(sku)
              list_info=json.dumps(list_info)
              GPIO.cleanup()
              reader6=MFRC522Update()
              reader6.write_no_block(list_info,0)
          else:
              print("Sin espacio para guardar en el tag")
                
                    
    
general()

reader32=MFRC522Update()
try:
        #text = input('New data:')
        opc =int(input('Opcion'))
        print("Now place your tag to write")
        print("Written")
        #reader.write_no_block(text,opc)
        id,text1 = reader32.read_no_block(opc)
        print(text1)
finally:
        GPIO.cleanup()


  

  
