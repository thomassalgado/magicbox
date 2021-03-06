import RPi.GPIO as GPIO
import time
import redis
import json
from Tkinter import *

#open conection with redis
r = redis.StrictRedis(host='<redis_ip>', port=<redis_port>, db=0)

try:
        while True:
                #getting message from redis
                strJson = r.lpop("fichas_liberar")
                if(strJson == None):
                        print "Fila Vazia"
                else:
                        #decode json
                        user = json.loads(strJson)
                        name = user["name"]
                        id = user["id"]
                        
                        #moving servo motor / pins from raspberry pi 1
                        GPIO.setmode(GPIO.BOARD)
                        GPIO.setup(7, GPIO.OUT)
                        p = GPIO.PWM(7,50)
                        p.start(2.5)
                        time.sleep(0.5)
                        p.ChangeDutyCycle(6.0)
                        time.sleep(0.5)
                        GPIO.cleanup()

                        #show message
                        root = Tk()
                        root.wm_title("Venha buscar sua ficha")
                        text = Text(font=("Helvetica",100))
                        text.pack(fill='both', expand=True)
                        text.tag_configure("tag-center", justify='center')
                        text.insert('end','Cliente\n' + name + "\nVenha buscar sua ficha\n" + "Compra Numero\n" + id, 'tag-center')
                        root.after(20000, lambda: root.destroy())
                        root.mainloop()
                time.sleep(5)

except KeyboardInterrupt:
        GPIO.cleanup()
