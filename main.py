from machine import Pin, Timer, ADC, PWM
import math, utime

#define the pwm pin
pwm_led = PWM(Pin(25))
pwm_led.freq(100)

#define leds
led_blue = Pin(15, Pin.OUT)
led_yellow = Pin(16, Pin.OUT)
led_blink = Pin(17, Pin.OUT)

#led toggle + timer definition
def blink_led(timer):
    led_blink.toggle()
timer = Timer()

timer.init(freq=2, mode=Timer.PERIODIC, callback=blink_led)

#intern and extern temp sensors
intern_sens = ADC(4)
temp_sens = ADC(28)

#conversion factor and beta for external
conv_factor = 3.3 / 65535
beta_coeff = 3528

#variables and list
temp_lst = []
counter = 0
duty_ccl = 0

def getExternalSensTemp():
    read_adc_val = float(temp_sens.read_u16())
    ext_temp_val = 3.3 * float(read_adc_val) / 65535
    Rt = 1000 * ext_temp_val / (3.3 - ext_temp_val)
    temp = 1/(((math.log(Rt/10000))/beta_coeff) + (1/(273.15 + 25)))
    return temp - 273.15

def getInternalSensTemp():
    read_internal = intern_sens.read_u16() * conv_factor
    return (27 - (read_internal - 0.706)/0.001721)

while True:
    #external
    external_temp = getExternalSensTemp()
    #internal
    internal_temp = getInternalSensTemp()
    #print("Temp internal - " + str(temp_int))
    print("Temp external - " + str(external_temp))
    print("/*****************************************/")
    temp_lst.append(external_temp)

    if (31 < counter):
        temp_lst.pop(0)
    counter += 1

    if (24 < (sum(temp_lst) / len(temp_lst))):
        led_yellow.value(1)
        led_blue.value(0)
    else:
        led_blue.value(1)
        led_yellow.value(0)
    print("Average external temperature - " + str((sum(temp_lst) / len(temp_lst))))
    print("**************************************************************")
    print("**************************************************************")
    print("*************************List size " + str(len(temp_lst)) + "**")
    print(duty_ccl)
    pwm_led.duty_u16(duty_ccl)
    duty_ccl += 500
    if (64000 < duty_ccl):
        duty_ccl = 0

    utime.sleep(1)
