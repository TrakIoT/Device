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
      GPIO.cleanup()
      reader50=MFRC522Update()
      reader50.write_no_block(write, 1)
      write=str('["'+inf+'",'+'["'+sku+'"]]')
      GPIO.cleanup()
      reader1=MFRC522Update()
      reader1.write_no_block(write, 0)
    else:
      print("Acerque el TAG")
      GPIO.cleanup()
      reader40=MFRC522Update()
      id,text=reader40.read_no_block(0)
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
      else:
        opcion_2_1_1 = int(input("Indique el # del registro a eliminar: \n"))
        GPIO.cleanup()
        reader25=MFRC522Update()
        id,text=reader25.read_no_block(0)
        list_info=json.loads(text)
        len_max=len(list_info)
        list_info[1].pop(opcion_2_1_1-1)
        list_info=json.dumps(list_info)
        GPIO.cleanup()
        reader8=MFRC522Update()
        reader8.write_no_block(list_info,0)
        if opcion_2_1_1==1 and len_max == 1:
            GPIO.cleanup()
            reader60=MFRC522Update()
            reader60.write_no_block("",1)
        elif opcion_2_1_1==1 and len_max >1:
            GPIO.cleanup()
            reader8=MFRC522Update()
            id,text=reader8.read_no_block(2)
            GPIO.cleanup()
            reader9=MFRC522Update()
            reader9.write_no_block(text,1)
            GPIO.cleanup()
            reader10=MFRC522Update()
            id, text = reader10.read_no_block(3)
            GPIO.cleanup()
            reader11=MFRC522Update()
            reader11.write_no_block(text,2)
            GPIO.cleanup()
            reader12=MFRC522Update()
            id, text = reader12.read_no_block(4)
            GPIO.cleanup()
            reader13=MFRC522Update()
            reader13.write_no_block(text,3)
            text=""
            GPIO.cleanup()
            reader17=MFRC522Update()
            reader17.write_no_block(text,4)
        elif opcion_2_1_1==2:
            GPIO.cleanup()
            reader14=MFRC522Update()
            id, text = reader14.read_no_block(3)
            GPIO.cleanup()
            reader15=MFRC522Update()
            reader15.write_no_block(text,2)
            GPIO.cleanup()
            reader16=MFRC522Update()
            id, text = reader16.read_no_block(4)
            GPIO.cleanup()
            reader18=MFRC522Update()
            reader18.write_no_block(text,3)
            text=""
            GPIO.cleanup()
            reader19=MFRC522Update()
            reader19.write_no_block(text,4)
        elif opcion_2_1_1 ==3:
            GPIO.cleanup()
            reader20=MFRC522Update()
            id, text = reader20.read_no_block(4)
            GPIO.cleanup()
            reader21=MFRC522Update()
            reader21.write_no_block(text,3) 
            text = ""
            GPIO.cleanup()
            reader22=MFRC522Update()
            reader22.write_no_block(text,4)
        else:
            text = ""
            GPIO.cleanup()
            reader23=MFRC522Update()
            reader23.write_no_block(text,4)
  else:
    print("Acerque el TAG")
    GPIO.cleanup()
    reader24=MFRC522Update()
    id, text = reader24.read_no_block(0)
    list_info = json.loads(text)
    print("Código Localización: " , list_info[0])
    cant_sku = len(list_info[1])
    print("SKUs guardados: ")
    for i in range(0, cant_sku):
        j = i + 1
        print(j , ". " , list_info[1][i])
    num_regi=int(input("Indique el # del registro a leer: \n"))
    GPIO.cleanup()
    reader25=MFRC522Update()
    id, text = reader25.read_no_block(num_regi)
    list_info_sku = json.loads(text)
    print("Sku: ", list_info_sku[0])
    print("Lote: " , list_info_sku[1])
    print("Cantidad: " ,list_info_sku[2])
    print("Fecha de Vencimiento: " , list_info_sku[3])
  t1=['0','0','0','0']
  t2=['0','0','0','0']
  t3=['0','0','0','0']
  t4=['0','0','0','0']
  GPIO.cleanup()
  reader100=MFRC522Update()
  id, text0 = reader100.read_no_block(0)
  t0= json.loads(text0)
  GPIO.cleanup()
  reader101=MFRC522Update()
  id, text1 = reader101.read_no_block(1)
  if len(t0[1])>=1:
    t1= json.loads(text1)
  GPIO.cleanup()
  reader102=MFRC522Update()
  id, text2 = reader102.read_no_block(2)
  if len(t0[1])>=2:
    t2= json.loads(text2)
  GPIO.cleanup()
  reader103=MFRC522Update()
  id, text3 = reader103.read_no_block(3)
  if len(t0[1])>=3:
    t3= json.loads(text3)
  GPIO.cleanup()
  reader104=MFRC522Update()
  id, text4 = reader104.read_no_block(4)
  if len(t0[1])>=4:
    t4= json.loads(text4)
  
  tx=[t1,t2,t3,t4]
  
  f1=str('{ "TAG":"' + t0[0]+'","PRODUCTS":{')
  
  for i in range(0,len(t0[1])):
    cant_text=str(tx[i][2])
    f1=str(f1+'"'+tx[i][0]+'":{ "LOTE": "'+tx[i][1]+'","CANTIDAD":'+cant_text+',"F.VENCIMIENTO":"'+tx[i][3]+'"}')
    if i <len(t0[1])-1:
      f1=str(f1+",")
  
  f1=str(f1+"}}")
  print(f1)
  jsonFile = open("tag.json", "w")
  jsonFile.write(f1)
  jsonFile.close()
    
                   
general()



try:
        #text = input('New data:')
        opc =int(input('Opcion'))
        print("Now place your tag to write")
        print("Written")
        #reader.write_no_block(text,opc)
        GPIO.cleanup()
        reader32=MFRC522Update()
        id,text1 = reader32.read_no_block(opc)
        print(text1)
finally:
        GPIO.cleanup()
  
