from pathlib import Path
from picamera2 import Picamera2
from threading import Thread, Event, Lock
from time import sleep
import time
from LogData import PATH 

class CAMERA:
    def __init__(self):
        self.picam2 = Picamera2()
        self.photo_thread = None
        self.video_thread = None
        self.photo_stop_event = Event()
        self.video_stop_event = Event()
        self.operation_lock = Lock() 

        self.save_dir = Path(PATH)
        self.save_dir.mkdir(parents=True, exist_ok=True)

      
        self.still_config = self.picam2.create_still_configuration(
            main={"size": (4608, 2592)},
            controls={
                "FrameDurationLimits": (16666, 16666),  # 60 fps
                "AnalogueGain": 1.0,
                "ExposureTime": 8000,
                "AwbEnable": False,
                "AwbRedGain": 1.8,
                "AwbBlueGain": 1.2
            }
        )
      
        self.video_config = self.picam2.create_video_configuration(
            main={"size": (1920, 1080)},
            controls={
                "FrameDurationLimits": (16666, 16666),  # 60 fps
                "AnalogueGain": 1.0,
                "ExposureTime": 8000,
                "AwbEnable": False,
                "AwbRedGain": 1.8,
                "AwbBlueGain": 1.2
            }
        )

        self.picam2.configure(self.still_config)
        self.picam2.start()
        sleep(2)

    def take_photo(self, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"foto_{timestamp}.jpg"
        full_path = self.save_dir / filename  
        self.picam2.capture_file(str(full_path))

    def _photo_loop(self, interval_seconds):
        while not self.photo_stop_event.is_set():
            with self.operation_lock:
                
                if not self.video_thread or not self.video_thread.is_alive():
                    self.take_photo()
            self.photo_stop_event.wait(interval_seconds)

    def start_taking_photos_periodically(self, interval_seconds):
        if self.photo_thread and self.photo_thread.is_alive():
            return
        self.photo_stop_event.clear()
        self.photo_thread = Thread(target=self._photo_loop, args=(interval_seconds,), daemon=True)
        self.photo_thread.start()

    def stop_taking_photos(self):
        if self.photo_thread and self.photo_thread.is_alive():
            self.photo_stop_event.set()
            self.photo_thread.join()

    def _video_record(self, duration_seconds, filename):
        with self.operation_lock:

            self.stop_taking_photos()

            self.picam2.stop()
            self.picam2.configure(self.video_config)
            self.picam2.start()

            full_path = self.save_dir / filename
            self.picam2.start_recording(str(full_path))

        sleep(duration_seconds)

        with self.operation_lock:
            self.picam2.stop_recording()
            self.picam2.stop()

            self.picam2.configure(self.still_config)
            self.picam2.start()

        self.start_taking_photos_periodically(interval_seconds=5)

    def start_video_recording(self, duration_seconds, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"video_{timestamp}.mp4"
        if self.video_thread and self.video_thread.is_alive():
            return
        self.video_thread = Thread(target=self._video_record, args=(duration_seconds, filename), daemon=True)
        self.video_thread.start()


