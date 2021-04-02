import Leap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

# Leap Motion Controller Setup
controller = Leap.Controller()
controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

# Matplotlib Setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', xlim=(-300, 300), ylim=(-200, 400), zlim=(-300, 300))
ax.view_init(elev=45., azim=122)

points = np.zeros((3, 22))
patches = ax.scatter(points[0], points[1], points[2], s=[20]*22, alpha=1)

def get_points():
	frame = controller.frame()
	hand = frame.hands.rightmost
	if not hand.is_valid: return np.array(patches._offsets3d)
	fingers = hand.fingers

	X = []
	Y = []
	Z = []

	# Add the position of the palms
	X.append(hand.palm_position.x)
	Y.append(hand.palm_position.y)
	Z.append(hand.palm_position.z)

	# Add wrist position
	arm = hand.arm
	print(arm.wrist_position)
	X.append(arm.wrist_position.x)
	Y.append(arm.wrist_position.y)
	Z.append(arm.wrist_position.z)

	# Add fingers
	for finger in fingers:
		for joint in range(0,4):
			'''
			0 = JOINT_MCP – The metacarpophalangeal joint, or knuckle, of the finger.
			1 = JOINT_PIP – The proximal interphalangeal joint of the finger. This joint is the middle joint of a finger.
			2 = JOINT_DIP – The distal interphalangeal joint of the finger. This joint is closest to the tip.
			3 = JOINT_TIP – The tip of the finger.
			'''
			X.append(finger.joint_position(joint)[0])
			Y.append(finger.joint_position(joint)[1])
			Z.append(finger.joint_position(joint)[2])

	return np.array([X, Z, Y])

def save_points(points,name='points.csv'):
	np.savetxt(name, points, delimiter=',')

def plot_points(points):
	patches.set_offsets(points[:2].T)
	patches.set_3d_properties(points[2], zdir='z')

def animate(i):
	points = get_points()
	#print(points)
	plot_points(points)

	# Save some test points for us to work with. 
	if (i == 300):
		print("Wooooo")
		save_points(points, 'test_points.csv')
		##quit()
	return patches,

def main():
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=2)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()
	