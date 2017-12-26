#!/usr/bin/env python

import numpy as np
from abc import abstractmethod
from simulator import TwoWheelVehicleRobotSimulator

class SubsumptionModule(object):
    def __init__(self):
        super(SubsumptionModule, self).__init__()
        self.__inputs = {}
        self.__outputs = {}
        self.child_modules = {}
        self.on_init()

    def add_child_module(self, name, module):
        self.child_modules[name] = module

    def set_inputs(self, inputs):
        self.__inputs = inputs
        for m in self.child_modules.values():
            m.set_inputs(inputs)

    def get_input(self, name):
        return self.__inputs.get(name, None)

    def set_output(self, name, val):
        self.__outputs[name] = val

    def get_output(self, name):
        return self.__outputs.get(name, None)

    def update(self):
        for m in self.child_modules.values():
            m.update()
        self.on_update()

    @abstractmethod
    def on_init(self):
        pass

    @abstractmethod
    def on_update(self):
        pass


class AvoidModule(SubsumptionModule):
    def on_init(self):
        pass

    def on_update(self):
        self.set_output("left_wheel_speed",  30 * (1 - self.get_input("right_touch")))
        self.set_output("right_wheel_speed", 30 * (1 - self.get_input("left_touch")))


class WanderModule(SubsumptionModule):
    TURN_START_STEP = 100
    TURN_END_STEP = 150
    def on_init(self):
        self.counter = 0
        self.add_child_module('avoid', AvoidModule())

    def on_update(self):
        # count steps not senser activated
        if self.get_input("right_touch") > 0 and self.get_input("left_touch") > 0:
            self.counter = 0
        else:
            self.counter = (self.counter + 1) % self.TURN_END_STEP
        if self.counter < self.TURN_START_STEP:
            # not inhibit avoid module
            self.set_output("left_wheel_speed",  self.child_modules['avoid'].get_output("left_wheel_speed"))
            self.set_output("right_wheel_speed", self.child_modules['avoid'].get_output("right_wheel_speed"))
        elif self.counter == self.TURN_START_STEP:
            # suppress child avoid module and start turning
            if np.random.rand() < 0.5:
                self.set_output("left_wheel_speed",  20)
                self.set_output("right_wheel_speed", 30)
            else:
                self.set_output("left_wheel_speed",  30)
                self.set_output("right_wheel_speed", 20)
        else:
            pass


class FeedingModule(SubsumptionModule):
    def on_update(self):
        pass


######################
# change architecture
######################

#controller = AvoidModule()  # same as braitenberg vehicle (layer0)
controller = WanderModule()  # add wandering module (layer1)
#controller = FeedingModule() # add feeding module (layer2)

#def controll_func(left_sensor, right_sensor):
def controll_func(sensor_data):
    controller.set_inputs(sensor_data)
    controller.update()
    return controller.get_output('left_wheel_speed'), controller.get_output('right_wheel_speed')

if __name__ == '__main__':
    sim = TwoWheelVehicleRobotSimulator(obstacle_num=3)
    #sim = TwoWheelVehicleRobotSimulator(obstacle_num=3, feed_num=30)
    sim.controll_func = controll_func
    sim.run()