# LCD05-Python
### Simple API for interacting with I2C based LCD05 display (python)

#### Functions:

```
lcd_init()
  -> clear display
  -> set cursor home
  -> disable cursor
  -> turn backlight on
```

```
lcd_clear()
  -> clear display
```

```
lcd_setBrightness(val)
  -> set brightness to val(0-255)
```

```
lcd_setContrast(val)
  -> set contrast to val(0-255)
```

```
lcd_home()
  -> set cursor to home
```

```
lcd_setCursor(l,c)
  -> set cursor to (l,c) l(1-2) / c(1-16)
```

```
lcd_backLight(flag)
  -> in case flag true turn on light
  -> in case flag false turn off light
```

```
lcd_noCursor()
  -> disable cursor
```

```
lcd_cursorOn()
  -> enable cursor
```

```
lcd_print(message,line,adjust)
  -> string message
  -> int line
  -> adjust("center","left","right")
```  
