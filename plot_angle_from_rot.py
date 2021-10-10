import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

from resources.Windows import Leap
import MatplotLeap as leapplot

# Leap Motion Controller Setup
controller = Leap.Controller()
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
ax = fig.add_subplot(121, projection='3d', xlim=(-300, 300), ylim=(-200, 400), zlim=(-300, 300))
ax2 = fig.add_subplot(122, projection='3d', xlim=(-300, 300), ylim=(-200, 400), zlim=(-300, 300))
ax.view_init(elev=45., azim=122)
ax2.view_init(elev=45., azim=122)

points = np.zeros((3, NUM_POINTS))
a_points = np.zeros((3, 16))
patches = ax.scatter(points[0], points[1], points[2], s=[20]*NUM_POINTS, alpha=1)
angle_plot = ax2.scatter(a_points[0], a_points[1], a_points[2], s=[10]*16, alpha=1)

# Angle Utils
def get_rotation_matrix(bone):
	basis = bone.basis
	x_basis = basis.x_basis
	y_basis = basis.y_basis
	z_basis = basis.z_basis
	matrix = Leap.Matrix(x_basis, y_basis, z_basis).to_array_3x3()
	matrix = np.reshape(matrix, newshape=(3, 3))
	print("Basis", matrix)
	return matrix

def get_angles_from_rot(rot_mat):
	"""
	Function from LearnOpenCV, Satya Mallick:
	https://www.learnopencv.com/rotation-matrix-to-euler-angles/
	https://github.com/spmallick/learnopencv/blob/master/RotationMatrixToEulerAngles/rotm2euler.py
	"""
	sy = math.sqrt(rot_mat[0, 0] * rot_mat[0, 0] + rot_mat[1, 0] * rot_mat[1, 0])
	singular = sy < 1e-6

	if not singular:
		x = math.atan2(rot_mat[2, 1], rot_mat[2, 2])
		y = math.atan2(-rot_mat[2, 0], sy)
		z = math.atan2(rot_mat[1, 0], rot_mat[0, 0])
	else:
		x = math.atan2(-rot_mat[1, 2], rot_mat[1, 1])
		y = math.atan2(-rot_mat[2, 0], sy)
		z = 0

	return [x,y,z]
	#return [math.degrees(angle) for angle in [x, y, z]]

def get_rot_from_angles(theta) :
	# Calculates Rotation Matrix given euler angles.
	"""
	Function from LearnOpenCV, Satya Mallick:
	https://www.learnopencv.com/rotation-matrix-to-euler-angles/
	https://github.com/spmallick/learnopencv/blob/master/RotationMatrixToEulerAngles/rotm2euler.py
	"""
	x = np.array([
		[1,         0,                  0                   ],
		[0,         math.cos(theta[0]), -math.sin(theta[0]) ],
		[0,         math.sin(theta[0]), math.cos(theta[0])  ]
	])

	y = np.array([
		[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
		[0,                     1,      0                   ],
		[-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
	])

	z = np.array([
		[math.cos(theta[2]),    -math.sin(theta[2]),    0],
		[math.sin(theta[2]),    math.cos(theta[2]),     0],
		[0,                     0,                      1]
	])

	R = np.dot(z, np.dot(y, x))
	return R

finger_bones = ['metacarpals', 'proximal', 'intermediate', 'distal']

def get_angles(hand):
	'''
	Gets angles in degrees for all joints in the hand.
	Do I need the basis vector for the hands?
	'''
	angles = []

	for finger in hand.fingers:
		bone_angles = []
		for b in range(0,4):
			if (b == 0):
				# The
				last_bone = hand
			else:
				last_bone = finger.bone(b-1)
			bone = finger.bone(b)
			# Generate rotation matrices from basis vectors
			last_bone_mat = get_rotation_matrix(last_bone)
			bone_mat = get_rotation_matrix(bone)
			# Get rotation matrix between bones, change of basis
			rot_mat = np.matmul(
				bone_mat, last_bone_mat.transpose()
				)

			# Generate euler angles in degrees from rotation matrix
			bone_angles.append(get_angles_from_rot(rot_mat))
		angles.append(bone_angles)
	return angles

def animate(i):
	# Reset the plots
	leapplot.reset_plot(ax)
	leapplot.reset_plot(ax2)

	points = leapplot.get_bone_points(controller)
	a_points = points

	if (points is not None):
		if (SAVE):
			points_list.append(points.flatten())

		patches = ax.scatter(points[0], points[1], points[2], s=[10]*NUM_POINTS, alpha=1)
		leapplot.plot_points(points, patches)
		leapplot.plot_bone_lines(points, ax)

		frame = controller.frame()
		hand = frame.hands.frontmost

		if hand.is_valid:
			#print('\r', leap_hand.get_angles(), end='')
			angles = np.array(get_angles(hand))

			print("angles", angles)
			print("angles shape: ", angles.shape)


			# Turn the angles into points
			X = [0]
			Y = [0]
			Z = [0]
			for finger in range(0,5):
				for bone in range(0,4):
					pitch = angles[finger,bone, 0]
					yaw = angles[finger,bone, 1]
					roll = angles[finger,bone, 2]

					theta = angles[finger,bone, :]

					#theta = [pitch, yaw, roll]
					rot_mat = get_rot_from_angles(theta)
					# Which basis is this bone defined in???
					bone_assume = np.array([0,20,0])
					new_bone = rot_mat.dot(bone_assume)#.dot(get_rot_from_angles(angles[0, bone, :]))

					# Debugging
					if (finger == 1):
						if (bone == 1):
							print("Pitch degrees",theta[0] * 57.296)
							print("Angles", theta)
							print("rot_mat ", rot_mat)
							print("Det" ,np.linalg.det(rot_mat))
							# Testing time
							print("nb", new_bone)


					x = X[finger*3+bone] + new_bone[0]
					y = Y[finger*3+bone] + new_bone[1]
					z = Z[finger*3+bone] + new_bone[2]

					X.append(x)
					Y.append(y)
					Z.append(z)

		# Convert to a numpy array
		a_points = [X, Z, Y]
		a_points = np.array(a_points)

		# Creating the 2nd plot
		angle_plot = ax2.scatter(a_points[0], a_points[1], a_points[2], alpha=1)
		# Plot Angle points
		leapplot.plot_points(a_points, angle_plot)


def main():
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=2)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()


