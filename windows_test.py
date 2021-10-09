# Windows Test
'''
Note this will error if you are not using Python3.8
See: https://github.com/leapmotion/LeapCxx/blob/master/samples/Sample.py
'''
import Leap

class SampleListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

	def on_init(self, controller):
		print("Initialized")

	def on_connect(self, controller):
		print("Connected")

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print("Disconnected")

	def on_exit(self, controller):
		print("Exited")

	def on_frame(self, controller):
		# Get the most recent frame and report some basic information
		frame = controller.frame()

		print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
			  frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))

		# Get hands
		for hand in frame.hands:

			handType = "Left hand" if hand.is_left else "Right hand"

			print("  %s, id %d, position: %s" % (
				handType, hand.id, hand.palm_position))

			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction

			# Calculate the hand's pitch, roll, and yaw angles
			print("  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
				direction.pitch * Leap.RAD_TO_DEG,
				normal.roll * Leap.RAD_TO_DEG,
				direction.yaw * Leap.RAD_TO_DEG))

			# Get arm bone
			arm = hand.arm
			print("  Arm direction: %s, wrist position: %s, elbow position: %s" % (
				arm.direction,
				arm.wrist_position,
				arm.elbow_position))

			# Get fingers
			for finger in hand.fingers:

				print("    %s finger, id: %d, length: %fmm, width: %fmm" % (
					self.finger_names[finger.type],
					finger.id,
					finger.length,
					finger.width))

				# Get bones
				for b in range(0, 4):
					bone = finger.bone(b)
					print("      Bone: %s, start: %s, end: %s, direction: %s" % (
						self.bone_names[bone.type],
						bone.prev_joint,
						bone.next_joint,
						bone.direction))

		if not frame.hands.is_empty:
			print("")	

if __name__ == "__main__":
	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)
	try:
		while True:
			pass
	except KeyboardInterrupt:
		controller.remove_listener(listener)