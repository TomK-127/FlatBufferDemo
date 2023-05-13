import numpy as np
import matplotlib.pyplot as plt
from .space_object import SpaceObject


class SolarSystem:
    def __init__(self):
        self.objects = []
        self.num_objects = 0
