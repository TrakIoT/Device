#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import json
import time

class SimpleMFRC522:

  READER = None

  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  BLOCK_ADDRS = [12,13,14]

  casos=[[[8,9,10],11],
       [[12,13,14],15],
       [[16,17,18],19],
       [[20,21,22],23],
       [[24,25,26],27]
       ]

  def __init__(self):
    self.READER = MFRC522()

  def read(self):
      id, text = self.read_no_block()
      while not id:
          id, text = self.read_no_block()
      return id, text

  def read_id(self):
    id = self.read_id_no_block()
    while not id:
      id = self.read_id_no_block()
    return id

  def read_id_no_block(self):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None
      return self.uid_to_num(uid)

  def read_no_block(self,op):
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, self.casos[op][1], self.KEY, uid)
    data = []
    text_read = ''
    if status == self.READER.MI_OK:
        for block_num in self.casos[op][0]:
            block = self.READER.MFRC522_Read(block_num)
            if block:
            		data += block
        if data:
             text_read = ''.join(chr(i) for i in data)
    self.READER.MFRC522_StopCrypto1()
    return id, text_read

  def write(self, text):
      id, text_in = self.write_no_block(text)
      while not id:
          id, text_in = self.write_no_block(text)
      return id, text_in


  def write_no_block(self, text,op):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      self.READER.MFRC522_SelectTag(uid)
      status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, self.casos[op][1], self.KEY, uid)
      self.READER.MFRC522_Read(self.casos[op][1])
      if status == self.READER.MI_OK:
          data = bytearray()
          data.extend(bytearray(text.ljust(len(self.casos[op][0]) * 16).encode('ascii')))
          i = 0
          for block_num in self.casos[op][0]:
            self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
            i += 1
      self.READER.MFRC522_StopCrypto1()
      return id, text[0:(len(self.casos[op][0]) * 16)]

  def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n

reader=SimpleMFRC522()

def general():
  inf=0
  sku=0
  lote=0
  cantidad=0
  fecha=0
  lista_sku=0
  opcion_1=int(input("Bienvenido, qué desea hacer: (Escribir - 1) - (Leer - 2) \n"))
  if opcion_1 ==1:
    opcion_1_1=int(input("(Nuevo Tag - 1) - (Tag Existente - 2): \n"))
    if opcion_1_1==1:
            inf=str(input("Código Localización: "))
            sku=str(input("Nuevo SKU: "))
            lote=str(input("Lote: "))
            cantidad=str(input("Cantidad: "))
            fecha=str(input("Fecha de Vencimiento (dd-mm-aaaa): "))
            print("Acerque el TAG")
            
            write = str('["' + sku + '",' + '"'+lote+'",'+cantidad+',"'+fecha+'"]')
            reader.write_no_block(write, 1)
            write=str('["'+inf+'",'+'["'+sku+'"]]')
            GPIO.cleanup()
            reader1=SimpleMFRC522()
            reader1.write_no_block(write, 0)
    else:
            print("Acerque el TAG")
            GPIO.cleanup()
            reader1=SimpleMFRC522()
            id,text=reader1.read_no_block(0)
            list_info=json.loads(text)
            print("Código Localización: "+list_info[0])
            cant_sku=len(list_info[1])
            print("SKUs guardados: ")
            for i in range(0,cant_sku):
                j=i+1
                print(j,". ",list_info[1][i])
            opcion_2_1=int(input("(Mod. cantidad de un registro - 1) - (Agregar un Registro - 2) - (Eliminar un Registro - 3): \n"))
            if opcion_2_1==1:
                opcion_2_1_1=int(input("Indique el # del registro a modificar: \n"))
                GPIO.cleanup()
                reader2=SimpleMFRC522()
                id,text1=reader2.read_no_block(opcion_2_1_1)
                print(text1)
                list_info_sku=json.loads(str(text1))
                n_cant=int(input("Ingrese la nueva cantidad: \n"))
                list_info_sku[2]=n_cant
                list_info_sku=json.dumps(list_info_sku)
                GPIO.cleanup()
                reader3=SimpleMFRC522()
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
                    reader4=SimpleMFRC522()
                    reader4.write_no_block(write,cant_sku+1)
                    GPIO.cleanup()
                    reader5=SimpleMFRC522()
                    id,text=reader5.read_no_block(0) 
                    list_info=json.loads(text)
                    list_info[1].append(sku)
                    list_info=json.dumps(list_info)
                    GPIO.cleanup()
                    reader6=SimpleMFRC522()
                    reader6.write_no_block(list_info,0)
                else:
                    print("Sin espacio para guardar en el tag")
            else:
                
                    
    
general()

reader32=SimpleMFRC522()
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


  

  
