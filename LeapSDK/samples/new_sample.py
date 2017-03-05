################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
#arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import threading
import requests
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
class SampleListener(Leap.Listener):
    pongheight = 500
    motionLimit = 500
    pongplace = 0
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    handplace = [0,0]
    wordplace = ["",""]
    pongplacement = [0,0]
    url="http://localhost:3030/games"
    def printit(self):
        payload = {'paddle1': SampleListener.pongplacement[0], 'paddle2': SampleListener.pongplacement[1]}
        requests.post(SampleListener.url, data=payload)
        threading.Timer(0.25, self.printit).start()
        print SampleListener.pongplacement
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        self.printit()

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        fingers = frame.fingers
        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"
            print handType
            place = 1
            if hand.is_left:
                place = 0

            vale = hand.palm_position.y/100
            print str(hand.palm_position.y) + " " + str(vale*.65) + " " + str(SampleListener.handplace[place]*.65)
            same = str(round(vale*.65, 2)) == str(round(SampleListener.handplace[place]*.65, 2))
            word = ""
            string = ""
            leniancy = 1

            if same:
                word = "STAY"
                string =  handType + ": NO CHANGE"
            elif SampleListener.handplace[place] < vale:
                word = "UP"
                string = handType + ": UP"
            elif SampleListener.handplace[place] > vale:
                word = "DOWN"
                string = handType + ": DOWN"
            else:
                word = "STAY"
                string = handType + ": NO CHANGE"
            SampleListener.handplace[place] = vale
            newplaceonpong = float(SampleListener.pongheight/SampleListener.motionLimit) * hand.palm_position.y
            SampleListener.pongplacement[place] = newplaceonpong
            print " ( " + word + " ) PLACE: " + str(newplaceonpong)
            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

        # Get gestures
        for gesture in frame.gestures():
            #print "Left hand" if gesture.hands[0].is_left else "Right hand"
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                #print "  Circle "

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                #print "  Swipe "

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                #print "  Key Tap "

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                #print "  Screen Tap "

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
'''
if SampleListener.handplace[place] < vale:
word = "UP"
print handType + ": UP"
elif SampleListener.handplace[place] > vale:
word = "DOWN"
print handType + ": DOWN"
elif abs(SampleListener.handplace[place]*.65-vale*.65) < .1:
word = "STAY"
print handType + ": NO CHANGE"
'''
