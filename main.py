import esp
esp.osdebug(None)
import uio
import json
import machine
import network
import socket
import time
import neopixel


def send_file(cl, filename):
    with open(filename, 'rb') as f:
        body = b'HTTP/1.1 200 OK\r\n\r\n' + f.read()
        n = cl.write(body)
        print('Sent {} of {} bytes'.format(n, len(body)))

led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
px = neopixel.NeoPixel(machine.Pin(15), 50)

# Connect to WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
with open('network.txt', 'r') as f:
    essid, password = [x.strip() for x in f.readlines()]
    sta_if.connect(essid, password)
print('Connecting', end='')
while not sta_if.isconnected():
    print('.', end='')
    led1.off()
    led2.on()
    time.sleep(0.1)
    led1.on()
    led2.off()
    time.sleep(0.1)
print('Connected')
print(sta_if.ifconfig()[0])
led1.off()
led2.off()
time.sleep(0.5)
led1.on()
led2.on()

# Start Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
    cl, addr = s.accept()
    request = uio.BytesIO(cl.recv(1024))
    first_line = request.readline()
    if first_line == b'':
        cl.close()
        continue
    requst_type, path, version = first_line.decode('utf-8').split()
    print('{} requesting {}'.format(requst_type, path))
    x = b' '
    while x != b'' and x != b'\r\n':
        x = request.readline()
        print(x)
    if requst_type == 'GET':
        if path == '/':
            send_file(cl, 'home.html')
        if path == '/scripts.js':
            send_file(cl, 'scripts.js')
    if requst_type == 'POST':
        if path == '/state.json':
            values = json.load(request)
            print(values)
            for i in range(50):
                px[i] = (int(values['g']), int(values['r']), int(values['b']))
            px.write()
            cl.write(b'HTTP/1.1 200 OK\r\n\r\n')
    cl.close()
