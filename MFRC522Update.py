#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
import time

class MFRC522Update(SimpleMFRC522):
  BLOCK_ADDRS = [12,13,14]

  casos=[[[8,9,10],11],
       [[12,13,14],15],
       [[16,17,18],19],
       [[20,21,22],23],
       [[24,25,26],27]
       ]

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

