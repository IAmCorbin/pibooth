# -*- coding: utf-8 -*-

import time
import subprocess
try:
    import pibooth.controls.camera.arducam_mipicamera as arducam
except ImportError:
    arducam = None  # arducam is optional
import v4l2
from pibooth.utils import LOGGER, memorize
from pibooth.language import get_translated_text
from pibooth.controls.camera.base import BaseCamera


@memorize
def ardu_camera_connected():
    """Return True if an Arducam camera is found.
    """
    LOGGER.info("ardu_camera_connected()")
    if not arducam:
        return False  # arducam is not installed
    try:
        LOGGER.info("Attempting to initialize arducam camera")
        camera = arducam.mipi_camera()
        LOGGER.info("Arducam - Open camera...")
        camera.init_camera()
        LOGGER.info("Arducam - Close camera...")
        camera.close_camera()
        return True
    except OSError:
        pass
    except Exception:
        pass
    return False


class ArduCamera(BaseCamera):

    """Camera management
    """

    """if picamera:
        IMAGE_EFFECTS = list(picamera.PiCamera.IMAGE_EFFECTS.keys())
    else:
        IMAGE_EFFECTS = []
    """

    def __init__(self,
                 iso=200,
                 resolution=(2328, 1748),
                 rotation=0,
                 flip=False,
                 delete_internal_memory=False):
        BaseCamera.__init__(self, resolution, delete_internal_memory)
        self._cam = arducam.mipi_camera()
        LOGGER.info("Arducam - Open camera...")
        self._cam.init_camera()
        """TODO: Determine Arducam Properties        
        self._cam.framerate = 15  # Slower is necessary for high-resolution
        self._cam.video_stabilization = True
        self._cam.vflip = False
        self._cam.hflip = flip
        self._cam.resolution = resolution
        self._cam.iso = iso
        self._cam.rotation = rotation
        """
        LOGGER.info("Arducam - Setting Resolution to: {}x{}".format(resolution[0],resolution[1]))
        self._cam.set_resolution(resolution[0], resolution[1])


    def _show_overlay(self, text, alpha):
        """Add an image as an overlay.
        """
        LOGGER.info("Arducam - show_overlay...")
        raise NotImplementedError

    def _hide_overlay(self):
        """Remove any existing overlay.
        """
        LOGGER.info("Arducam - hide_overlay...")
        raise NotImplementedError

    def preview(self, window, flip=True):
        """Display a preview on the given Rect (flip if necessary).
        """
        LOGGER.info("Arducam - preview...")
        self._window = window
        rect = window.get_rect()
        self._cam.start_preview(fullscreen = False, window = (0, 0, rect.width, rect.height))                                
        LOGGER.info("Arducam - Reset the focus...")
        self._cam.reset_control(v4l2.V4L2_CID_FOCUS_ABSOLUTE)
        LOGGER.info("Arducam - Enable Auto Exposure...")
        self._cam.software_auto_exposure(enable = True)
        LOGGER.info("Arducam - Enable Auto White Balance...")
        self._cam.software_auto_white_balance(enable = True)

    def preview_countdown(self, timeout, alpha=60):
        """Show a countdown of `timeout` seconds on the preview.
        Returns when the countdown is finished.
        """
        LOGGER.info("Arducam - preview-countdown...")
        while timeout > 0:
            time.sleep(1)
            timeout -= 1
          

    def preview_wait(self, timeout, alpha=60):
        """Wait the given time.
        """
        LOGGER.info("Arducam - previe_wait...")
        raise NotImplementedError

    def stop_preview(self):
        """Stop the preview.
        """
        LOGGER.info("Arducam - stop_preview...")
        self._cam.stop_preview()
        self._window = None      

    def capture(self, filename, effect=None):
        """Capture a new picture in a file.
        """
        LOGGER.info("Arducam - Attempt Capture..")
        frame = self._cam.capture(encoding = 'jpeg')
        frame.as_array.tofile(filename)
        self._captures[filename] = None


    def quit(self):
        """Close the camera driver, it's definitive.
        """
        LOGGER.info("Arducam - Close camera...")
        self._cam.close_camera()     
