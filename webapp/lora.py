import serial
import os
import pygame
from gtts import gTTS

language = 'vi'
ser = serial.Serial(
        port = '/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2
    )

class Lora():
    def __init__(self,ser=ser):
        self.ser = ser

    def lorasend(self, text):
        self.text = text
        try:
            self.ser.write(self.text)
            self.ser.flush()

        except KeyboardInterrupt:
            self.ser.close()

    def lorareceive(self):
        try:
            s = self.ser.readline()
            data = s.decode()           # decode s
            data = data.rstrip()        # cut "\r\n" at last of string
            if data == "dON":
                speak("Đèn đã bật")
            elif data == "dOFF":
                speak("Đèn đã tắt")
            elif data == "bON":
                speak("Bơm đã bật")
            elif data == "bOFF":
                speak("Bơm đã tắt")
            elif data == "allON" or data == "dON,bOFF" or data == "allOFF" or data == "dOFF,bON": 
                pass
            else: speak("Tác vụ chưa được thực hiện.")

        except:
            ser.close()
            data=""
        finally:
            return data

def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.play()
    os.remove("sound.mp3")