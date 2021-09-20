#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pygame
import speech_recognition as sr
import wikipedia
import datetime
from time import strftime
from gtts import gTTS
from dis import dis
import requests, json

wikipedia.set_lang('vi')
language = 'vi'
path = "/usr/lib/chromium-browser/chromedriver"

class assistant_control():
    def check(self):
        try:
            text = get_text()
            if("Trợ lý" in text or "trợ lý" in text):
                speak("Dạ")
                text = get_text()
                rq = requests.get("http://35.194.40.82:5000/modelNLP/{0}/{1}".format("id1",text))
                if rq.status_code == 200:
                    self.text = str(json.loads(rq.content.decode('utf-8'))['result']).strip()
                else:
                    self.text = ""
            else:
                self.text = ""
        except:
            self.text = ""

    def main(self):
        if self.text == "hoi_chuc_nang":
            help_me()
        elif self.text == "chao_hoi":
            hello()
        elif self.text == "hoi_gio":
            get_time_h()
        elif self.text == "hoi_ngay":
            get_time_d()
        elif self.text == "hoi_thoi_tiet":
            current_weather()
        elif self.text == "hoi_dinh_nghia":
            tell_me_about()
        else:
            pass
        self.text = ""

def speak(text):
    #print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.play()
    os.remove("sound.mp3")

def get_audio():
    #print("\nBot: \tĐang nghe \t --__-- \n")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=8, snowboy_configuration=None)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            if("Hồ Chí Minh" in text):
                text = "Ho Chi Minh"
            elif("Đồng Nai" in text):
                text = "Dong Nai"
            return str(text.lower())
        except:
            #print("...")
            return 0

def stop():
    speak("Hẹn gặp lại bạn sau!")

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
    return 0

def hello():
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn. Chúc bạn một ngày tốt lành.")
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn. Bạn đã dự định gì cho chiều nay chưa.")
    else:
        speak("Chào buổi tối bạn. Bạn đã ăn tối chưa nhỉ.")


def get_time_h():
    now = datetime.datetime.now()
    speak('Bây giờ là %d giờ %d phút %d giây' % (now.hour, now.minute, now.second))

def get_time_d():
    now = datetime.datetime.now()
    speak("Hôm nay là ngày %d tháng %d năm %d" %(now.day, now.month, now.year))

def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute, 
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        speak(content)

    else:
        speak("Không tìm thấy địa chỉ của bạn")

def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0].split(".")[0])
    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")
        #time.sleep(5)

def help_me():
    speak("""Bot có thể giúp bạn thực hiện các chức năng sau đây:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Hiển thị ngày
    4. Dự báo thời tiết
    5. Kể bạn biết về thế giới
    6. Điều khiển các thiết bị điện trong nhà của bạn.""")

def control(obj_assistant):
    obj_assistant.check()
    obj_assistant.main()

if __name__ == "__main__":
    obj_assistant = assistant_control()
    #=================== Assistant ===================#
    speak("Xin chào, tôi là trợ lý do Huy Phát tạo ra.")
    while True:
        try:
            control(obj_assistant)
            dis(control)
        except:
            pass

