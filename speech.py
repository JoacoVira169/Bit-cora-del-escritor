import speech_recognition as sr

def prueba():
    mic = sr.Microphone()
    rec = sr.Recognizer()

    with mic as audio_file:
        print('Porfavor, hable...')
        rec.adjust_for_ambient_noise(audio_file)
        audio = rec.listen(audio_file)
        print('Procesando...')
        print('Usted dijo: ' + rec.recognize_google(audio, language='es-ES'))

def speech_es():
    mic = sr.Microphone()
    rec = sr.Recognizer()
    
    with mic as audio_file:
        rec.adjust_for_ambient_noise(audio_file)
        audio = rec.listen(audio_file)
        return rec.recognize_google(audio, language='es-ES')