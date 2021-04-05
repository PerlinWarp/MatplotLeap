import Leap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

# Leap Motion Controller Setup
controller = Leap.Controller()
controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
NUM_POINTS = 22

SAVE = True
points_list = []

def on_close(event):
	print("Closed Figure")

	if (SAVE):
		print("Saving all points gathered")
		np.savetxt("all_points.csv", points_list, delimiter=',')

# Matplotlib Setup
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close)
ax = fig.add_subplot(111, projection='3d', xlim=(-300, 300), ylim=(-200, 400), zlim=(-300, 300))
ax.view_init(elev=45., azim=122)

points = np.zeros((3, NUM_POINTS))
patches = ax.scatter(points[0], points[1], points[2], s=[20]*NUM_POINTS, alpha=1)

def get_points():
	frame = controller.frame()
	hand = frame.hands.rightmost
	if not hand.is_valid: return np.array(patches._offsets3d)
	fingers = hand.fingers

	X = []
	Y = []
	Z = []

	# Add the position of the palms
	X.append(-1 *hand.palm_position.x)
	Y.append(hand.palm_position.y)
	Z.append(hand.palm_position.z)

	# Add wrist position
	X.append(-1 * hand.wrist_position.x)
	Y.append(hand.wrist_position.y)
	Z.append(hand.wrist_position.z)

	# Add Elbow
	#arm = hand.arm
	#X.append(arm.elbow_position.x)
	#Y.append(arm.elbow_position.y)
	#Z.append(arm.elbow_position.z)

	# Add fingers
	for finger in fingers:
		for joint in range(0,4):
			'''
			0 = JOINT_MCP – The metacarpophalangeal joint, or knuckle, of the finger.
			1 = JOINT_PIP – The proximal interphalangeal joint of the finger. This joint is the middle joint of a finger.
			2 = JOINT_DIP – The distal interphalangeal joint of the finger. This joint is closest to the tip.
			3 = JOINT_TIP – The tip of the finger.
			'''
			X.append(-1 * finger.joint_position(joint)[0])
			Y.append(finger.joint_position(joint)[1])
			Z.append(finger.joint_position(joint)[2])

	return np.array([X, Z, Y])

def save_points(points,name='points.csv'):
	# Save one single row to disk
	np.savetxt(name, points, delimiter=',')

def plot_points(points):
	patches.set_offsets(points[:2].T)
	patches.set_3d_properties(points[2], zdir='z')

def plot_lines(points):
	mcps = []
	
	# Wrist
	wrist = points[:,1]
	
	# For Each of the 5 fingers
	for i in range(0,5):
		n = 4*i + 2

		# Get each of the bones
		mcp = points[:,n+0]
		pip = points[:,n+1]
		dip = points[:,n+2]
		tip = points[:,n+3]
		
		# Connect the lowest joint to the middle joint    
		bot = plt3d.art3d.Line3D([mcp[0], pip[0]], [mcp[1], pip[1]], [mcp[2], pip[2]])
		ax.add_line(bot)
		
		# Connect the middle joint to the top joint
		mid = plt3d.art3d.Line3D([pip[0], dip[0]], [pip[1], dip[1]], [pip[2], dip[2]])
		ax.add_line(mid)       
		
		# Connect the top joint to the tip of the finger
		top = plt3d.art3d.Line3D([dip[0], tip[0]], [dip[1], tip[1]], [dip[2], tip[2]])
		ax.add_line(top)        

		# Connect each of the fingers together
		mcps.append(mcp)
	for mcp in range(0,4):
		line = plt3d.art3d.Line3D([mcps[mcp][0], mcps[mcp+1][0]],
								  [mcps[mcp][1], mcps[mcp+1][1]],
								  [mcps[mcp][2], mcps[mcp+1][2]])
		ax.add_line(line)
	# Create the right side of the hand joining the pinkie mcp to the "wrist"
	line = plt3d.art3d.Line3D([wrist[0], mcps[4][0]],
								  [wrist[1], mcps[3+1][1]],
								  [wrist[2], mcps[3+1][2]])
	ax.add_line(line)
	
	# Generate the "Wrist", note right side is not right.
	line = plt3d.art3d.Line3D([wrist[0], mcps[0][0]],
								  [wrist[1], mcps[0][1]],
								  [wrist[2], mcps[0][2]])
	ax.add_line(line)


def animate(i):
	# Reset the plot
	ax.cla()
	# Really you can just update the lines to avoid this
	ax.view_init(elev=45., azim=122)
	ax.set_xlim3d([-300, 300])
	ax.set_xlabel('X [mm]')
	ax.set_ylim3d([-200, 400])
	ax.set_ylabel('Y [mm]')
	ax.set_zlim3d([-300, 300])
	ax.set_zlabel('Z [mm]')

	points = get_points()
	if (SAVE):
		points_list.append(points.flatten())

	patches = ax.scatter(points[0], points[1], points[2], s=[10]*NUM_POINTS, alpha=1)
	plot_points(points)
	plot_lines(points)

	return patches,

def main():
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=2)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()
	