import webbrowser
from gtts import gTTS
import random as rd
import playsound
import os
from datetime import datetime
import speech_recognition as sr

r = sr.Recognizer()

r.energy_threshold = False

badword = ['mày','tao','*','điên','ngu','dốt']

#to talk
def talk(line):
    tts = gTTS(text=line, lang='vi')
    r = rd.randint(1, 1000000000)
    audio_save = 'audio-' +str(r) + '.mp3'
    tts.save(audio_save)
    playsound.playsound(audio_save)
    print(line)
    os.remove(audio_save)

#audio recording
def record_audio(ask = False):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        if ask:
            talk(ask)
        try:
            audio_data = r.listen(source, timeout = 3.0)
        except:
            return ""
        text = ""
        try:
            text = r.recognize_google(audio_data, language="vi-VN")
        except:
            print("Ooppzzz...")
        return text.lower()
    
voice = record_audio("xin chào").lower()


#response processing
def respond(voice):
    if 'tên gì' in voice or 'là ai' in voice:
        if voice.__contains__('bạn'):
            talk('Tôi là hỗ trợ ảo được viết bởi Trương Tấn Long')
        elif 'tôi' or 'tui' in voice:
            talk('Tôi không biết!')
        else:
            return 
    elif 'tra cứu' in voice:
        result = record_audio('bạn cần tra cứu gì')
        
        if result!="":
            url = 'https://www.google.com/search?q=' + result
            webbrowser.get().open(url)
            res = 'đây là kết quả tìm kiếm được từ từ khóa ' + result
            talk(res)
        else:
            talk('tôi không nghe được bạn nói gì!')
    elif 'tìm' and 'youtube' in voice:
        result = record_audio('bạn cần tìm gì trên Youtube')
        
        if result!="":
            url = 'https://www.youtube.com/results?search_query=' + result
            webbrowser.get().open(url)
            res = 'đây là kết quả tìm kiếm được từ từ khóa ' + result
            talk(res)
        else:
            talk('tôi không nghe được bạn nói gì!')

    elif 'địa điểm' in voice:
        result = record_audio('bạn cần tìm địa điểm nào')
        out = result
        
        if result!="":
            if result.__contains__(" "):
                result = result.split()
                result = '+'.join(result)

            url = 'https://maps.google.com/?q=' + str(result)
            webbrowser.get().open(url)
            res = 'đây là địa điểm tìm kiếm được từ từ khóa ' + out
            talk(res)
        else:
            talk('tôi không nghe được bạn nói gì!')

    elif 'facebook' in voice:
        url = 'https://www.facebook.com'
        if 'mở' in voice:
            webbrowser.get().open(url)
            talk('đang mở facebook')
        elif 'tìm' in voice:
            result = record_audio('bạn cần tìm gì')
            out = result
        
            if result!="":
                if result.__contains__(" "):
                    result = result.split()
                    result = '+'.join(result)

                url+= '/search/top?q=' + str(result)
                webbrowser.get().open(url)
                res = 'đây là kết tìm kiếm được từ từ khóa ' + out
                talk(res)
            else:
                talk('tôi không nghe được bạn nói gì!')

    elif 'mấy giờ' in voice:
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
        res = 'bây giờ là ' + dt_string
        talk(res)

    elif 'hỗ trợ ơi' in voice:
        talk('tôi vẫn đang lắng nghe đây')

    elif 'kết thúc' in voice:
        return False
    
    else:
        for i in badword:
            if i in voice:
                res = ['không được nói tục nhé','bạn đang thiếu văn hóa đấy','kiểm điểm lại cách dùng từ đi nào','chú ý ngôn từ nào']
                talk(rd.choice(res))
                return
        res = str(voice)+' không có trong từ điển của tôi'
        talk(res)


cont = True

#test to know if voice is recorded
def out(voice):
    if voice=="":
        print("haizda")
    elif voice!="":
        print(voice)

#main
while(cont):
    if 'kết thúc' in voice:
        talk('Tạm biệt, hẹn gặp lại')
        cont = False
    else:
        out(voice)
        if voice.lower().__contains__('hỗ trợ ơi'):
            res = ['tôi đây','bạn cần tôi giúp gì nào','tôi có thể giúp gì cho bạn']
            talk(rd.choice(res))
            flag = True
            while(flag):
                voice = record_audio()
                out(voice)
                res = ''
                if 'tạm dừng' in voice:
                    flag = False
                    break
                elif voice != "":
                    res = respond(voice)
                if res == False:
                    cont = res
                    talk('Tạm biệt, hẹn gặp lại')
                    break
                
            if cont:
                talk('hãy nói hỗ trợ ơi để gọi tôi nhé')
    if cont:
        voice = record_audio()




