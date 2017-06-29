import smbus
import time
import datetime
import sys, tty, termios, os

#DATA VALUES DEFINES FROM->http://www.robot-electronics.co.uk/htm/Lcd05tech.htm
LCD_NOOP = 0x00
LCD_CURSORHOME = 0x01
LCD_CURSORPOS = 0x02
LCD_CURSORPOSXY = 0x03
LCD_CURSOROFF = 0x04
LCD_CURSORON = 0x05
LCD_CURSORBLINK = 0x06
LCD_BACKSPACE = 0x08
LCD_TAB = 0x09
LCD_CURSORDOWN = 0x0A
LCD_CURSORUP = 0x0B
LCD_CLEARDISPLAY = 0x0C
LCD_LINEFEED = 0x0D
LCD_CLEARCOLUMN = 0x11
LCD_TABSET = 0x12
LCD_BACKLIGHTON = 0x13
LCD_BACKLIGHTOFF = 0x14
LCD_CUSTOMCHAR = 0x1B
LCD_CONTRAST = 0x1E
LCD_BRIGHTNESS = 0x1F

LCD_WIDTH = 16
LCD_LINE_1 = 1
LCD_LINE_2 = 2

#I2C_ADDRESS FROM TERMINAL "i2cdetect -y 1"
I2C_ADDR = 0x63
COMM = 0x00

ON=True
OFF=False

#USAGE OF SMBUS LIBRARY
bus = smbus.SMBus(1)

#SIMPLE FUNCTION TO GEY KEYBOARD KEYS
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
#INICIALIZATION OF DISPLAY
def lcd_init():
    lcd_clear()
    lcd_home()
    lcd_noCursor()
    lcd_backLight(ON)
#CLEAN THE DISPLAY
def lcd_clear():
    bus.write_byte_data(I2C_ADDR,COMM,LCD_CLEARDISPLAY)
#BRIGHTNESS ADJUSTMENT
def lcd_setBrightness(val):
    bus.write_byte_data(I2C_ADDR,COMM,LCD_BRIGHTNESS)
    bus.write_byte_data(I2C_ADDR,COMM,val)
#CONTRAST ADJUSTMENT
def lcd_setContrast(val):
    bus.write_byte_data(I2C_ADDR,COMM,LCD_CONTRAST)
    bus.write_byte_data(I2C_ADDR,COMM,val)
#SET CURSOR BACK HOME
def lcd_home():
    bus.write_byte_data(I2C_ADDR,COMM,LCD_CURSORHOME)
#SET CURSOR ON LINE & COLUMN
def lcd_setCursor(l,c):
    bus.write_byte_data(I2C_ADDR,COMM,LCD_CURSORPOSXY)
    bus.write_byte_data(I2C_ADDR,COMM,int(hex(l),0))
    bus.write_byte_data(I2C_ADDR,COMM,int(hex(c),0))
#SET BACKLIGHT ON & OGG
def lcd_backLight(flag):
    if(flag==True):
        bus.write_byte_data(I2C_ADDR,COMM,LCD_BACKLIGHTON)
    else:
        bus.write_byte_data(I2C_ADDR,COMM,LCD_BACKLIGHTOFF)
    pass
#DISABLE CURSOR
def lcd_noCursor():
    bus.write_byte_data(I2C_ADDR,COMM,LCD_CURSOROFF)
#ENABLE CURSOR
def lcd_cursorOn():
    bus.write_byte_data(I2C_ADDR,COMM,LCD_CURSORON)
#PRINT MESSAGE WITH ALIGMENT
def lcd_print(message,line,adjust):
    lcd_setCursor(line,1)
    if(adjust=="left"):
        message = message.ljust(LCD_WIDTH," ")
    elif(adjust=="right"):
        message = message.rjust(LCD_WIDTH," ")
    elif(adjust=="center"):
        message = message.center(LCD_WIDTH," ")
    for i in range(LCD_WIDTH):
        bus.write_byte_data(I2C_ADDR,COMM,ord(message[i]))
#USER GUI TO ADJUST CONTRAST
def lcd_adjust_Contrast():
    print("Contrast".center(16," "))
    print("More:+".ljust(16," "))
    print("Less:-".ljust(16," "))
    print("Exit:x".ljust(16," "))
    lcd_print("Hello World!!!",LCD_LINE_1,"center")
    lcd_print("More: + Less: -",LCD_LINE_2,"center")
    val=200
    status = True
    while status==True:
        c_h=getch()
        if c_h =="x":
            status=False
        elif c_h == "+":
            if val<255:
                val=val+1
            else:
                val=255
            lcd_setContrast(val)
        elif c_h == "-":
            if val>0:
                val=val-1
            else:
                val=0
            lcd_setContrast(val)
#USER GUI TO ADJUST BRIGHTNESS
def lcd_adjust_Brightness():
    print("Brightness".center(16," "))
    print("More:+".ljust(16," "))
    print("Less:-".ljust(16," "))
    print("Exit:x".ljust(16," "))
    lcd_print("Hello World!!!",LCD_LINE_1,"center")
    lcd_print("More: + Less: -",LCD_LINE_2,"center")
    val=200
    status = True
    while status==True:
        c_h=getch()
        if c_h =="x":
            status=False
        elif c_h == "+":
            if val<255:
                val=val+1
            else:
                val=255
            lcd_setBrightness(val)
        elif c_h == "-":
            if val>0:
                val=val-1
            else:
                val=0
            lcd_setBrightness(val)

#MAIN EXAMPLE HELLO WORLD AND DATE AND TIME
def main():
    lcd_init()
    lcd_adjust_Contrast()
    lcd_adjust_Brightness()
    print("ctrl-c to exit()")
    while True:

        now = datetime.datetime.now()
        shour=str(now.hour).rjust(2,"0") +":"+str(now.minute).rjust(2,"0")+":"+str(now.second).rjust(2,"0")
        sdate=str(now.day).rjust(2,"0") +"/"+str(now.month).rjust(2,"0")+"/"+str(now.year).rjust(4,"0")

        lcd_print("Hello World!!!",LCD_LINE_1,"center")
        lcd_print(shour,LCD_LINE_2,"right")

        time.sleep(3)

        # Send some more text
        lcd_print("Hello World!!!",LCD_LINE_1,"center")
        lcd_print(sdate,LCD_LINE_2,"right")

        time.sleep(3)


if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_clear()
    lcd_backLight(OFF)
