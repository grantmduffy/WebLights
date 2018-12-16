import esp
esp.osdebug(None)
import time
import socket
import machine
import uio
import ure
import json
import neopixel

PIXEL_COUNT = 50

led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
color = [0, 0, 0]
brightness = 0.1
px = neopixel.NeoPixel(machine.Pin(15), PIXEL_COUNT)


def send_response(status, body=''):
    cl.send(bytes(status + '\r\n\r\n' + body, 'utf-8'))


def parse_request(request):
    print("GOT REQUEST:\n{}".format(request))
    output = {}
    with uio.BytesIO(request) as f:
        output['Type'], output['Path'], output['Version'] = [x.decode('utf-8').strip() for x in f.readline().split()]
        while True:
            x = f.readline()
            if x == b'':
                break
            result = ure.match(b'(.+): (.+)', x)
            if result:
                key = result.group(0).strip()
                val = result.group(1).strip()
                output[key] = val
            if x == b'\r\n':
                output['Body'] = f.read().decode('utf-8')
    return output


def load_resources():
    global essid, password, html, javascript
    with open('network.txt', 'r') as f:
        essid, password = [x.strip() for x in f.readlines()]
    with open('home.html', 'r') as f:
        html = f.read()
    with open('scripts.js', 'r') as f:
        javascript = f.read()


def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
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


def update_color():
    print('R: {}, G: {}, B: {}'.format(*color))


def start_server():
    global cl, brightness, color, px
    run = True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while run:
        cl, addr = s.accept()
        request = cl.recv(1024)
        # print('#### GOT REQUEST ####\n{}\n'.format(request.decode('utf-8')))
        request_data = parse_request(request)
        if request_data['Type'] == 'GET':
            if request_data['Path'] == '/':
                send_response('HTTP/1.1 200 OK', html)
            if request_data['Path'] == '/scripts.js':
                send_response('HTTP/1.1 200 OK', javascript)
        if request_data['Type'] == 'POST':
            if request_data['Path'] == '/state.json':
                command = json.loads(request_data['Body'])
                if 'led1' in command:
                    led1.off() if command['led1'] == 1 else led1.on()
                if 'led2' in command:
                    led2.off() if command['led2'] == 1 else led2.on()
                if 'r' in command:
                    color[0] = command['r']
                    update_color()
                if 'g' in command:
                    color[1] = command['g']
                    update_color()
                if 'b' in command:
                    color[2] = command['b']
                    update_color()
                if 'brightness' in command:
                    brightness = command['brightness']
                if 'r' in command or 'g' in command or 'b' in command:
                    for i, p in enumerate(px):
                        px[i] = color
                    px.write()
                send_response('HTTP/1.1 200 OK', 'Updated Leds')
        cl.close()


def print_dict(dict):
    print('{')
    for key in dict:
        print('\t{}: {}'.format(key, dict[key]))
    print('}')


load_resources()
connect()
start_server()


