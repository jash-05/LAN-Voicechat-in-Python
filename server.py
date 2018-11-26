
# Echo server program
import socket
import pyaudio
import wave
import datetime

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
RECORD_SECONDS = 4000
now=datetime.datetime.now

#HOST = '127.0.0.1'
HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
try:
    s.listen(1)
    conn, addr = s.accept()
    print('Connected to address:', addr[0],'port:',addr[1])
    start=now()
except KeyboardInterrupt:
    pass

p = pyaudio.PyAudio()

# for receiving data
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
# for sending data
stream2 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


data='a'
i=0
try:
    while data != '':
        try:			# receiving data
            data = conn.recv(1024)
            stream.write(data)
            if i==0:
                print("Playing audio...")
                i=1
        except KeyboardInterrupt:
         	break
        try:		# sending data
            data2  = stream2.read(CHUNK)
            conn.sendall(data2)
        except KeyboardInterrupt:
         	break
    stream.stop_stream()
    stream.close()
except:
    print("Client ended connection")
end=now()
d=(end-start).total_seconds()
m,sec=int(d//60),int(d%60)
print("\nChat ended. Duration: {:02d}:{:02d}".format(m,sec))
p.terminate()
print("Connection closed")
conn.close()
