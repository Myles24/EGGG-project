# EGGG 101 Group 322
# CPX will light up and play a sound when dropped

import board, digitalio, time, adafruit_lis3dh, math, busio, neopixel

# Nonsense from the tutorial I had to use bc bad documentation
try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass # not always supported by every board!

buttonA = digitalio.DigitalInOut(board.BUTTON_A) # Initialize button 1
buttonA.direction = digitalio.Direction.INPUT # Basically determines behavior of button state
buttonA.pull = digitalio.Pull.DOWN # Use built in pull down resistor

spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE) # get object to turn speaker on
spkrenable.direction = digitalio.Direction.OUTPUT # use as output
spkrenable.value = True # actually turn it on

audio = AudioOut(board.SPEAKER) # get audio object to call play("sound.wav") on

i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA) # Communicate with accelerometer over I2C
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_2_G

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2, auto_write=False)
RED = (255, 0, 0)
OFF = (0, 0, 0)

FF_MAX = 2

def play_effects():
    # Play the sound and light effects 
    pixels.fill(RED)
    pixels.show()
    play_file("R2D2Scream.wav") # play the sound
    pixels.fill(OFF)
    pixels.show()

def play_file(filename):
    # Plays a wav file of the specified name
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        audio.play(wave)
        while audio.playing:
            pass
 
print("CPX activated")

while True:
    x, y, z = [value for value in lis3dh.acceleration] # get components of acceleration 
    magnitude = math.sqrt(x ** 2 + y ** 2 + z ** 2) # determine magnitude of accel. vector
    #print(magnitude)
    if magnitude < FF_MAX: # if it's close to 0, meaning in free fall with air resistance
        play_effects()
    time.sleep(0.01) # short delay so it detects free fall quickly
