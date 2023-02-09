import requests 

text = "Mukomeze mugire ibihe byiza!" #Text to be generated into voice

host = "https://domain.com" #replace this with your domain
port = 8000 #port number of the api

response = requests.post(f"{host}:{port}/tts", json={"text": text}) 

#Saving the response to .wav file
with open("audio.wav", "wb") as f: 
	f.write(response.content) 
#The response is in bytes format and can be played by most audio media players