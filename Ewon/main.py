import snowboydecoder
import sys
import signal
import time
import logging
from assistant import Assistant

interrupted = False

logging.basicConfig()
logger = logging.getLogger("daemon")
logger.setLevel(logging.DEBUG)

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

model = sys.argv[1]
# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


#ADD DEVICE ID AND MODEL ID HERE
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
assistant = Assistant(language_code="en-AU",
                      device_model_id="jaeho-a1a7d-jaeho-ux5fka",
                      device_id="47f38cac-3efa-11ec-92a4-e45f0164ccf5")

        

def detect_callback():
    detector.terminate()
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    assistant.assist()
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    detector.start(detected_callback=detect_callback, interrupt_check=interrupt_callback, sleep_time=0.03)


print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detect_callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
