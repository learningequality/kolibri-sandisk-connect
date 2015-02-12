#!/usr/bin/python
import threading
import time
import random
import datetime

stages = ["install_ka_lite", "copy_videos", "setup_hotspot"] # these are dummies

def get_current_stage(sandisk_id): # dummy (should return first stage that is not yet complete)
    return "install_ka_lite"

def mark_stage_completed(sandisk_id, stage): # dummy
    pass # write to spreadsheet here

class WorkerThread(threading.Thread):
    
    def __init__(self, wipi_id, sandisk_id):
        threading.Thread.__init__(self)
        self.wipi_id = wipi_id
        self.sandisk_id = sandisk_id
        self.stage = ""

    def log(self, message):
        print "%s: SanDisk %s @ wipi%d:" % (datetime.datetime.now(), self.sandisk_id, self.wipi_id), message
        self.last_log_message = message
    
    def run(self):
        self.log("Starting worker...")
        self.main_loop()
        self.log("Worker completed!")

    @classmethod
    def get_active(cls):
        return [t for t in threading.enumerate() if isinstance(t, WorkerThread)]

    def main_loop(self):
        self.stage = get_current_stage(self.sandisk_id)
        stage_index = stages.index(self.stage)
        for stage in stages[stage_index:]:
            self.stage = stage
            self.log("Running stage %s..." % stage)
            getattr(self, "run_stage__%s" % stage)() # run the specially named method for this stage
            self.log("Completed stage %s!" % stage)
            mark_stage_completed(self.sandisk_id, stage)
        # play siren here

    def run_stage__install_ka_lite(self):
        self.log("Installing KA Lite...")
        time.sleep(10 * random.random())
        self.log("KA Lite has been installed!")

    def run_stage__copy_videos(self):
        self.log("Copying videos...")
        for i in range(10):
            time.sleep(2 * random.random())
            self.log("Video #%d has been copied!" % i)
        self.log("All videos copied.")

    def run_stage__setup_hotspot(self):
        self.log("Setting up hotspot...")
        time.sleep(1)
        self.log("Hotspot configuration complete.")

if __name__ == "__main__":

    # Create new threads
    thread1 = WorkerThread(1, "CCE5")
    thread2 = WorkerThread(2, "A3DE")

    # Start new Threads
    thread1.start()
    thread2.start()
