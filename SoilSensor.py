import RPi.GPIO as GPIO
import time

# GPIO S
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

    # 初始化上一次状态
last_state = None

try:
  while True:
    current_state = GPIO.input(channel)

    # 仅在状态变化时打印
    if current_state != last_state:
      if current_state:
        print("No Water Detected!")
      else:
        print("Water Detected!")
      last_state = current_state

    # 添加短暂延时减少CPU负载
    time.sleep(0.1)

except KeyboardInterrupt:
  print("\nProgram stopped")
finally:
  GPIO.cleanup()

