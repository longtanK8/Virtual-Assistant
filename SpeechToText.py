# import speech_recognition as sr
# import pyaudio
# import wave

print(1+1)



#CHUNK = 1024
#FORMAT = pyaudio.paInt16
#CHANNELS = 2
#RATE = 44100
#RECORD_SECONDS = 3
#WAVE_OUTPUT_FILENAME = "sth.wav"

#p = pyaudio.PyAudio()

#stream = p.open(format=FORMAT,
#                channels=CHANNELS,
#                rate=RATE,
#                input=True,
#                frames_per_buffer=CHUNK)

#print("* recording")

#frames = []

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#    data = stream.read(CHUNK)
#    frames.append(data)

#print("* done recording")

#stream.stop_stream()
#stream.close()
#p.terminate()

#wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#wf.setnchannels(CHANNELS)
#wf.setsampwidth(p.get_sample_size(FORMAT))
#wf.setframerate(RATE)
#wf.writeframes(b''.join(frames))
#wf.close()


#filename = "sth.wav"
# def playBot(command):
#     command = command.split("bài hát ")[1]
#     print(command)

# r = sr.Recognizer()
# cont = True
# while(cont):
#     with sr.Microphone() as source:
#         audio_data = r.record(source, duration=3)
#         print("Recognizing...")
#         # convert speech to text
#         text = ""
#         try:
#             text = r.recognize_google(audio_data, language="vi-VN")
#             print(text)
#         except:
#             cont = True

#     #if text.lower().__contains__("f***"):
#     #    print("Hey! Language!!")
#     #else:
#     #    print("Haizzz...")

#     if text.lower().__contains__("hỗ trợ dừng"):
#         cont = False
#     if text.lower().__contains__("phát bài hát"):
#         playBot(text)