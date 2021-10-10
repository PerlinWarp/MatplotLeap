import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

from resources.Windows import Leap
import MatplotLeap as nl

# Leap Motion Controller Setup
controller = Leap.Controller()
#controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
NUM_POINTS = 22

SAVE = True
points_list = []
'''
finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
bone_names = ['MCP', 'PIP', 'DIP', 'TIP']
# We can of course generate column names on the fly:
for finger in finger_names:
	for bone in bone_names:
		for dim in ["x","y","z"]:
			columns.append(f"{finger}_{bone}_{dim}")

print(columns)
'''
columns = [
		"Palm_x", "Palm_y", "Palm_z",
		"Wrist_x", "Wrist_y", "Wrist_z",
		'Thumb_MCP_x', 'Thumb_MCP_y', 'Thumb_MCP_z',
		'Thumb_PIP_x', 'Thumb_PIP_y', 'Thumb_PIP_z',
		'Thumb_DIP_x', 'Thumb_DIP_y', 'Thumb_DIP_z',
		'Thumb_TIP_x', 'Thumb_TIP_y', 'Thumb_TIP_z',
		'Index_MCP_x', 'Index_MCP_y', 'Index_MCP_z',
		'Index_PIP_x', 'Index_PIP_y', 'Index_PIP_z',
		'Index_DIP_x', 'Index_DIP_y', 'Index_DIP_z',
		'Index_TIP_x', 'Index_TIP_y', 'Index_TIP_z',
		'Middle_MCP_x', 'Middle_MCP_y', 'Middle_MCP_z',
		'Middle_PIP_x', 'Middle_PIP_y', 'Middle_PIP_z',
		'Middle_DIP_x', 'Middle_DIP_y', 'Middle_DIP_z',
		'Middle_TIP_x', 'Middle_TIP_y', 'Middle_TIP_z',
		'Ring_MCP_x', 'Ring_MCP_y', 'Ring_MCP_z',
		'Ring_PIP_x', 'Ring_PIP_y', 'Ring_PIP_z',
		'Ring_DIP_x', 'Ring_DIP_y', 'Ring_DIP_z',
		'Ring_TIP_x', 'Ring_TIP_y', 'Ring_TIP_z',
		'Pinky_MCP_x', 'Pinky_MCP_y', 'Pinky_MCP_z',
		'Pinky_PIP_x', 'Pinky_PIP_y', 'Pinky_PIP_z',
		'Pinky_DIP_x', 'Pinky_DIP_y', 'Pinky_DIP_z',
		'Pinky_TIP_x', 'Pinky_TIP_y', 'Pinky_TIP_z'
		]
# Convert this to headers for numpy saving...
headers = ""
for col in columns:
	headers+= col
	headers+= ","
headers = headers[:-2]

def on_close(event):
	print("Closed Figure")

	if (SAVE):
		print("Saving all points gathered")
		# Alternatively use pandas to remove need to make headers string.
		np.savetxt("all_points.csv", points_list, delimiter=',', header=headers, comments='')

# Matplotlib Setup
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close)
ax = fig.add_subplot(111, projection='3d', xlim=(-300, 300), ylim=(-200, 400), zlim=(-300, 300))
ax.view_init(elev=45., azim=122)

points = np.zeros((3, NUM_POINTS))
patches = ax.scatter(points[0], points[1], points[2], s=[20]*NUM_POINTS, alpha=1)


def get_rel_bone_points(controller):
	'''
	Gets points for a full hand model. (22 points, 66 vars)
	Relative to the hand itself.
	Uses 4 joints for each finger and 3 for the thumb.
	Also uses Palm and Wrist position.
	Note this could be reduced to 21 points as the thumb has 1 less joint.
	'''
	frame = controller.frame()
	hand = frame.hands.rightmost
	if not hand.is_valid: return None

	# Get hand transform
	# Basis Transform from docs
	'''
	See Transforming Finger Coordinates into the Hand’s Frame of Reference
	https://developer-archive.leapmotion.com/documentation/python/devguide/Leap_Hand.html
	'''
	hand_x_basis = hand.basis.x_basis
	hand_y_basis = hand.basis.y_basis
	hand_z_basis = hand.basis.z_basis
	hand_origin = hand.palm_position
	hand_transform = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
	hand_transform = hand_transform.rigid_inverse()

	fingers = hand.fingers

	X = []
	Y = []
	Z = []

	# Add the position of the palms
	# Transform palm position
	palm_pos = hand_transform.transform_point(hand.palm_position)
	X.append(palm_pos.x)
	Y.append(palm_pos.y)
	Z.append(palm_pos.z)

	# Add wrist position
	wrist_pos = hand_transform.transform_point(hand.wrist_position)
	X.append(wrist_pos.x)
	Y.append(wrist_pos.y)
	Z.append(wrist_pos.z)


	# Add fingers
	for finger in fingers:
		for b in range(0, 4):
			'''
			0 = JOINT_MCP – The metacarpophalangeal joint, or knuckle, of the finger.
			1 = JOINT_PIP – The proximal interphalangeal joint of the finger. This joint is the middle joint of a finger.
			2 = JOINT_DIP – The distal interphalangeal joint of the finger. This joint is closest to the tip.
			3 = JOINT_TIP – The tip of the finger.
			'''
			bone = finger.bone(b)
			# Transform the finger
			transformed_position = hand_transform.transform_point(bone.prev_joint)
			X.append(transformed_position[0])
			Y.append(transformed_position[1])
			Z.append(transformed_position[2])

	return np.array([X, Z, Y])

def animate(i):
	# Reset the plot
	nl.reset_plot(ax)

	points = get_rel_bone_points(controller)
	if (points is not None):
		if (SAVE):
			points_list.append(points.flatten())

		patches = ax.scatter(points[0], points[1], points[2], s=[10]*NUM_POINTS, alpha=1)
		nl.plot_points(points, patches)
		nl.plot_bone_lines(points, ax)

def main():
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=2)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()


