# -*- coding: utf-8 -*-

"""
This file contains the updated Qudi Interface for a scientific camera used for spectroscopy.


Qudi is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Qudi is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Qudi. If not, see <http://www.gnu.org/licenses/>.

Copyright (c) the Qudi Developers. See the COPYRIGHT.txt file at the
top-level directory of this distribution and at <https://github.com/Ulm-IQO/qudi/>
"""
__all__ = ['CameraInterface']

from PySide2 import QtCore
from abc import abstractmethod
from qudi.core.interface import ScalarConstraint
from qudi.core.module import Base
import numpy as np

from enum import Enum


class ReadMode(Enum):
    """ Class defining the possible read modes of the camera

    'FVB': Full vertical binning. Returns the signal integrated over the whole columns of pixels, giving one curve.
    'MULTIPLE_TRACK': The signal is integrated over one or multiple tracks, giving a lost of one or multiple curves.
    'IMAGE': The camera return the signal over all the pixels as a 2d array.
    'IMAGE_ADVANCED': The camera return the signal over the super pixels on a given region of the camera, as a 2d array.
     """
    FVB = 0
    MULTIPLE_TRACKS = 1
    IMAGE = 2
    IMAGE_ADVANCED = 3


class ShutterState(Enum):
    """ Class defining the possible shutter states

    AUTO means the shutter opens only for the acquisition time.
    """
    CLOSED = 0
    OPEN = 1
    AUTO = 4  # Value do not conflict with ShutterState from simple_laser_logic


class Constraints:
    """ Class defining formally the hardware constraints """
    def __init__(self):
        self.name = ''                  # Camera manufacture name (ex : 'Newton940')
        self.width = None               # Camera width in pixels
        self.height = None              # Camera height in pixels
        self.pixel_size_width = None    # Physical width of the pixels in meter
        self.pixel_size_height = None    # Physical height of the pixels in meter
        self.read_modes = []            # Read mode supported by the camera (see ReadMode class)
        self.internal_gains = []        # Internal gains supported by the camera (list of float)
        self.readout_speeds = []        # Readout speed supported by the camera, in Hz (list of float)
        self.has_shutter = False        # Tells if the camera has a shutter
        self.trigger_modes = []         # User defined trigger mode (list of string)
        self.has_cooler = False         # Tells if the camera has a cooling system
        self.temperature = ScalarConstraint(unit='K')     # Temperature limits in kelvin


class ImageAdvancedParameters:
    """ Class defining formally a binning and a region of the camera for IMAGE_ADVANCED mode """
    def __init__(self):
        self.horizontal_binning = 1
        self.vertical_binning = 1
        self.horizontal_start = 0
        self.horizontal_end = None  # Has to be an integer
        self.vertical_start = 0
        self.vertical_end = None  # Has to be an integer


class CameraInterface(Base):
    """ This interface is used to manage a camera used for spectroscopy """

    @abstractmethod
    def get_constraints(self) -> Constraints:
        """ Returns all the fixed parameters of the hardware which can be used by the logic.

        @return (Constraints): An object of class Constraints containing all fixed parameters of the hardware
        """
        pass

    ##############################################################################
    #                           Basic functions
    ##############################################################################
    @abstractmethod
    def start_acquisition(self) -> None:
        """ Starts an acquisition of the current mode and returns immediately """
        pass

    @abstractmethod
    def abort_acquisition(self) -> None:
        """ Abort acquisition """
        pass

    @abstractmethod
    def get_ready_state(self) -> bool:
        """ Get the status of the camera, to know if the acquisition is finished or still ongoing.

        @return (bool): True if the camera is ready, False if an acquisition is ongoing

        As there is no synchronous acquisition in the interface, the logic needs a way to check the acquisition state.
        """
        pass

    @abstractmethod
    def get_acquired_data(self) -> np.array:
        """ Return an array of last acquired data.

        @return: Data in the format depending on the read mode.

        Depending on the read mode, the format is :
        'FVB' : 1d array
        'MULTIPLE_TRACKS' : list of 1d arrays
        'IMAGE' 2d array of shape (width, height)
        'IMAGE_ADVANCED' 2d array of shape (width, height)

        Each value might be a float or an integer.
        """
        pass

    ##############################################################################
    #                           Read mode functions
    ##############################################################################
    @abstractmethod
    def get_read_mode(self) -> ReadMode:
        """ Getter method returning the current read mode used by the camera.

        @return (ReadMode): Current read mode
        """
        pass

    @abstractmethod
    def set_read_mode(self, value) -> None:
        """ Setter method setting the read mode used by the camera.

        @param (ReadMode) value: read mode to set
        """
        pass

    ##############################################################################
    #                           Readout speed functions
    ##############################################################################
    @abstractmethod
    def get_readout_speed(self) -> float:
        """ Get the current readout speed of the camera

        This value is one of the possible values given by constraints
        """
        pass

    @abstractmethod
    def set_readout_speed(self, value) -> None:
        """ Set the readout speed of the camera

        @param (float) value: Readout speed to set, must be a value from the constraints readout_speeds list
        """
        pass

    ##############################################################################
    #                           Active tracks functions
    #
    # Method used only for read mode MULTIPLE_TRACKS
    ##############################################################################
    @abstractmethod
    def get_active_tracks(self) -> list:
        """ Getter method returning the read mode tracks parameters of the camera.

        @return (list):  active tracks positions [(start_1, end_1), (start_2, end_2), ... ]

        Should only be used while in MULTIPLE_TRACKS mode
        """
        pass

    @abstractmethod
    def set_active_tracks(self, value) -> None:
        """ Setter method for the active tracks of the camera.

        @param (list) value: active tracks positions  as [(start_1, end_1), (start_2, end_2), ... ]

        Some camera can sum the signal over tracks of pixels (all width times a height given by start and stop pixels)
        This sum is done internally before the analog to digital converter to reduce the signal noise.

        Should only be used while in MULTIPLE_TRACKS mode
        """
        pass

    ##############################################################################
    #                           Image advanced functions
    #
    # Method used only for read mode IMAGE_ADVANCED
    ##############################################################################
    @abstractmethod
    def get_image_advanced_parameters(self) -> ImageAdvancedParameters:
        """ Getter method returning the image parameters of the camera.

        @return (ImageAdvancedParameters): Current image advanced parameters

        Should only be used while in IMAGE_ADVANCED mode
        """
        pass

    @abstractmethod
    def set_image_advanced_parameters(self, value) -> None:
        """ Setter method setting the read mode image parameters of the camera.

        @param (ImageAdvancedParameters) value: Parameters to set

        Should only be used while in IMAGE_ADVANCED mode
        """
        pass

    ##############################################################################
    #                           Gain mode functions
    ##############################################################################
    @abstractmethod
    def get_gain(self) -> float:
        """ Get the current gain.

        @return (float): Current gain

        Gain value should be one in the constraints internal_gains list.
        """
        pass

    @abstractmethod
    def set_gain(self, value) -> None:
        """ Set the gain.

        @param (float) value: New gain, value should be one in the constraints internal_gains list.
        """
        pass

    ##############################################################################
    #                           Exposure functions
    ##############################################################################
    @abstractmethod
    def get_exposure_time(self) -> float:
        """ Get the exposure time in seconds

        @return: (float) exposure time
        """
        pass

    @abstractmethod
    def set_exposure_time(self, value) -> None:
        """ Set the exposure time in seconds.

        @param value: (float) desired new exposure time

        @return: nothing
        """
        pass

    ##############################################################################
    #                           Trigger mode functions
    ##############################################################################

    @abstractmethod
    def get_trigger_mode(self) -> str:
        """ Getter method returning the current trigger mode used by the camera.

        @return (str): Trigger mode

        This string should match one in the constraints trigger_modes list.
        """
        pass

    @abstractmethod
    def set_trigger_mode(self, value) -> None:
        """ Setter method for the trigger mode used by the camera.

        @param (str) value: trigger mode, should match one in the constraints trigger_modes list.
        """
        pass

    ##############################################################################
    #                        Shutter mode function
    #
    # Method used only if constraints.has_shutter
    ##############################################################################
    @abstractmethod
    def get_shutter_state(self) -> ShutterState:
        """ Getter method returning the shutter state.

        @return (ShutterState): The current shutter state
        """
        pass

    @abstractmethod
    def set_shutter_state(self, value) -> None:
        """ Setter method setting the shutter state.

        @param (ShutterState) value: the shutter state to set
        """
        pass

    ##############################################################################
    #                           Temperature functions
    #
    # Method used only if constraints.has_cooler
    ##############################################################################
    @abstractmethod
    def get_cooler_on(self) -> bool:
        """ Getter method returning the cooler status

        @return (bool): True if the cooler is on
        """
        pass

    @abstractmethod
    def set_cooler_on(self, value) -> None:
        """ Setter method for the the cooler status

        @param (bool) value: True to turn it on, False to turn it off
        """
        pass

    @abstractmethod
    def get_temperature(self) -> float:
        """ Getter method returning the temperature of the camera in Kelvin.

        @return (float) : Measured temperature in kelvin
        """
        pass

    @abstractmethod
    def get_temperature_setpoint(self) -> float:
        """ Getter method for the temperature setpoint of the camera.

        @return (float): Current setpoint in Kelvin
        """
        pass

    @abstractmethod
    def set_temperature_setpoint(self, value) -> None:
        """ Setter method for the temperature setpoint of the camera.

        @param (float) value: New setpoint in Kelvin
        """
        pass
