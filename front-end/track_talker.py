import os

class TrackTalker:
    def tell_calibrate():
        TrackTalker._tell_command("calibrate");
    def tell_restart():
        TrackTalker._tell_command("restart");

    def _tell_command(cmd):
        os.popen("echo " + cmd + " > /tmp/stlrs_cmd")
