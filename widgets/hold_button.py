from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.clock import Clock
from datetime import datetime

class HoldButton(ButtonBehavior, Widget):
    def __init__(self, duration, on_complete,**kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.press_time_start = None #Set to None till the button is pressed
        self.clock_event = None
        self.on_complete = on_complete

    def on_press(self):
        #Save time and start metronome when button is pressed
        self.press_time_start = datetime.now()
        self.clock_event = Clock.schedule_interval(self.check_tick, 0.1) #Check hold every 0.1 seconds

    def on_release(self):
        #Stop metronome and reset the start time
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event = None #Removing the clock event reference
        self.press_time_start = None

    def check_tick(self, dt):
        elapsed_time = datetime.now() - self.press_time_start
        if elapsed_time.total_seconds() >= self.duration:
            #Stop metronome and add a minute to the duration for the next hold
            if self.clock_event:
                self.clock_event.cancel()
                self.clock_event = None #Same as on_release, removing clock event reference
            self.press_time_start = None
            self.on_complete()

