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

def ageRecognize():
    #A Gender and Age Detection program by Mahesh Sawant

    import cv2
    import math
    import argparse

    def highlightFace(net, frame, conf_threshold=0.7):
        frameOpencvDnn=frame.copy()
        frameHeight=frameOpencvDnn.shape[0]
        frameWidth=frameOpencvDnn.shape[1]
        blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections=net.forward()
        faceBoxes=[]
        for i in range(detections.shape[2]):
            confidence=detections[0,0,i,2]
            if confidence>conf_threshold:
                x1=int(detections[0,0,i,3]*frameWidth)
                y1=int(detections[0,0,i,4]*frameHeight)
                x2=int(detections[0,0,i,5]*frameWidth)
                y2=int(detections[0,0,i,6]*frameHeight)
                faceBoxes.append([x1,y1,x2,y2])
                cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
        return frameOpencvDnn,faceBoxes


    parser=argparse.ArgumentParser()
    parser.add_argument('--image')

    args=parser.parse_args()

    faceProto="opencv_face_detector.pbtxt"
    faceModel="opencv_face_detector_uint8.pb"
    ageProto="age_deploy.prototxt"
    ageModel="age_net.caffemodel"
    genderProto="gender_deploy.prototxt"
    genderModel="gender_net.caffemodel"

    MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
    ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList=['Male','Female']

    faceNet=cv2.dnn.readNet(faceModel,faceProto)
    ageNet=cv2.dnn.readNet(ageModel,ageProto)
    genderNet=cv2.dnn.readNet(genderModel,genderProto)

    video=cv2.VideoCapture(args.image if args.image else 0)
    padding=20
    while cv2.waitKey(1)<0 :
        try:
            hasFrame,frame=video.read()
            if not hasFrame:
                cv2.waitKey()
                break
    
            resultImg,faceBoxes=highlightFace(faceNet,frame)
            if not faceBoxes:
                print("No face detected")
                cv2.imshow("Detecting age and gender", frame)
            else:
                for faceBox in faceBoxes:
                    face=frame[max(0,faceBox[1]-padding):
                               min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                               :min(faceBox[2]+padding, frame.shape[1]-1)]

                    blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
                    genderNet.setInput(blob)
                    genderPreds=genderNet.forward()
                    gender=genderList[genderPreds[0].argmax()]
                    print(f'Gender: {gender}')

                    ageNet.setInput(blob)
                    agePreds=ageNet.forward()
                    age=ageList[agePreds[0].argmax()]
                    print(f'Age: {age[1:-1]} years')

                    cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
                    cv2.imshow("Detecting age and gender", resultImg)

        except:
            talk('xảy ra lỗi, vui lòng thử lại sau')
            break;

    video.release()
    cv2.destroyAllWindows()
    talk('đang kết thúc nhận diện độ tuổi')

#response processing
def respond(voice):
    if 'tên gì' in voice or 'là ai' in voice:
        if voice.__contains__('bạn'):
            talk('Tôi là hỗ trợ ảo được viết bởi Trương Tấn Long')
        elif 'tôi' or 'tui' in voice:
            talk('Tôi không biết!')
        else:
            return 

    elif 'nhận diện độ tuổi' in voice:
        talk('đang khởi động trình nhận diện tuổi')
        ageRecognize()
            

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

    elif 'chào' in voice:
        res = ['chào bạn','xin chào','hế lô']
        talk(rd.choice(res))
    
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




