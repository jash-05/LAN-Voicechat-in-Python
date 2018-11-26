import socket
import pyaudio
import wave
import datetime

HOST = 'localhost'   
PORT = 50007         


now=datetime.datetime.now
#record
p = pyaudio.PyAudio()
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000

# for sending data
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
# for receiving data
stream2 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
i=0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
start=now()
print("Voice chat has begun:")
data2='a'
try:
    while data2 != '':
        try:        # sending data
            data  = stream.read(CHUNK)
            s.sendall(data)
        
                # receiving data
            data2 = s.recv(1024)
            if i==0:
                print("Playing audio...")
                i=1
            stream2.write(data2)
        except :
            data2=''  
            break
    end=now()
    d=(end-start).total_seconds()
    m,sec=int(d//60),int(d%60)
    print("\nChat ended. Duration: {:02d}:{:02d}".format(m,sec))
    stream.stop_stream()
    stream.close()
    p.terminate()
    s.close()
except :
    pass
print("Connection closed")
