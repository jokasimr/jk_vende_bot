# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    MapProxy,
    Vector,
    WeatherForecast,
    config,
)
from vendeeglobe.utils import distance_on_surface

CREATOR = "ItWillBeFine"  # This is your team name

import random
import numpy as np

class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = CREATOR  # Mandatory attribute
        self.avatar = "jk_vende_bot/avatar.gif"  # Optional attribute

        self.course = [
            Checkpoint(latitude=19.069698, longitude= -67.166883, radius=50),
            Checkpoint(latitude=18.150004, longitude= -68.258117, radius=50),
            Checkpoint(latitude=17.026520, longitude= -68.878516, radius=50),
            Checkpoint(latitude=14.022048, longitude= -74.434660, radius=50),
            Checkpoint(latitude=9.802589, longitude= -81.129015, radius=50),
            Checkpoint(latitude=8.893603, longitude= -79.492349, radius=50),
            Checkpoint(latitude=5.598162, longitude= -78.230821, radius=50),
            Checkpoint(latitude=16.768590, longitude= -160.150297, radius=50),
            Checkpoint(latitude=17.723622, longitude= -169.754068, radius=50),
            Checkpoint(latitude=7.946156, longitude= 134.545313, radius=50),
            Checkpoint(latitude=5.340338, longitude= 125.777469, radius=50),
            Checkpoint(latitude=2.336296, longitude= 120.490082, radius=50),
            Checkpoint(latitude=-0.836084, longitude= 118.587360, radius=50),
            Checkpoint(latitude=-4.201526, longitude= 117.390125, radius=50),
            Checkpoint(latitude=-5.092431, longitude= 112.787736, radius=50),
            Checkpoint(latitude=-5.604317, longitude= 106.043190, radius=50),
            Checkpoint(latitude=-5.839524, longitude= 105.726030, radius=50),

            Checkpoint(latitude=-5.976526, longitude= 105.619868, radius=50),

            Checkpoint(latitude=-6.514981, longitude= 105.612105, radius=50),
            Checkpoint(latitude=-6.63397, longitude= 105.214215, radius=50),
            Checkpoint(latitude=-8.781315, longitude= 76.069988, radius=50),
            Checkpoint(latitude=9.037740, longitude= 64.598015, radius=50),
            Checkpoint(latitude=13.825921, longitude= 54.472747, radius=50),
            Checkpoint(latitude=11.902736, longitude= 44.600362, radius=50),
            Checkpoint(latitude=12.642493, longitude= 43.275341, radius=50),
            Checkpoint(latitude=15.024852, longitude= 41.971500, radius=50),
            Checkpoint(latitude=25.536587, longitude= 35.723644, radius=50),
            Checkpoint(latitude=28.078345, longitude= 33.535253, radius=50),
            Checkpoint(latitude=28.951397, longitude= 32.836814, radius=50),
            Checkpoint(latitude=29.930378, longitude= 32.537955, radius=50),
            Checkpoint(latitude=30.909998, longitude= 32.353132, radius=50),
            Checkpoint(latitude=32.909998, longitude= 32.353132, radius=50),
            Checkpoint(latitude=32.942841, longitude= 26.912203, radius=50),
            Checkpoint(latitude=36.300864, longitude= 15.321960, radius=50),
            Checkpoint(latitude=37.866955, longitude= 10.996238, radius=50),
            Checkpoint(latitude=37.630378, longitude= 2.526095, radius=50),
            Checkpoint(latitude=36.016696, longitude= -4.312707, radius=50),
            Checkpoint(latitude=35.941754, longitude= -5.602107, radius=50),
            Checkpoint(latitude=36.221094, longitude= -11.882399, radius=50),
            Checkpoint(latitude=43.288277, longitude= -13.552321, radius=50),
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=5,
            ),
        ]

        '''
        self.course = [
            Checkpoint(latitude=43.797109, longitude=-11.264905, radius=50),
            Checkpoint(longitude=-29.908577, latitude=17.999811, radius=50),
            Checkpoint(latitude=-11.441808, longitude=-29.660252, radius=50),
            Checkpoint(longitude=-63.240264, latitude=-61.025125, radius=50),
            Checkpoint(latitude=2.806318, longitude=-168.943864, radius=1990.0),
            Checkpoint(latitude=-62.052286, longitude=169.214572, radius=50.0),
            Checkpoint(latitude=-15.668984, longitude=77.674694, radius=1190.0),
            Checkpoint(latitude=-39.438937, longitude=19.836265, radius=50.0),
            Checkpoint(latitude=14.881699, longitude=-21.024326, radius=50.0),
            Checkpoint(latitude=44.076538, longitude=-18.292936, radius=50.0),
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=5,
            ),
        ]
        '''

    def run(
        self,
        t: float,
        dt: float,
        longitude: float,
        latitude: float,
        heading: float,
        speed: float,
        vector: np.ndarray,
        forecast: WeatherForecast,
        world_map: MapProxy,
    ):
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            The weather forecast for the next 5 days.
        world_map:
            The map of the world: 1 for sea, 0 for land.
        """
        instructions = Instructions()
        for ch in self.course:
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            jump = dt * np.linalg.norm(speed)
            if dist < 2.0 * ch.radius + jump:
                instructions.sail = min(ch.radius / jump, 1)
            else:
                instructions.sail = 1.0
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                break
            if speed < 5:
                instructions.heading = heading + 4 * np.random.randn()

        return instructions
