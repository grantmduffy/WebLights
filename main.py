import esp
esp.osdebug(None)
import time
import socket
import machine

led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)

# Connect to network
def connect():
    import network
    with open('network.txt', 'r') as f:
        essid, password = [x.strip() for x in f.readlines()]
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(essid, password)
    while not sta_if.isconnected():
        led1.off()
        led2.on()
        time.sleep(0.1)
        led1.on()
        led2.off()
        time.sleep(0.1)
    led1.off()
    led2.off()
    time.sleep(0.5)
    led1.on()
    led2.on()


def start_server():
    run = True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while run:
        cl, addr = s.accept()
        led1.off()
        request = cl.recv(1024).decode('utf-8')
        cl.send(bytes("<body>Hello World</body>", 'utf-8'))
        print('Connection Received\nClient: {}, Address: {}\n####Request####\n{}'.format(cl, addr, request))
        led1.on()
        cl.close()


connect()
start_server()


