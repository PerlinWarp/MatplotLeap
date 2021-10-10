import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

import MatplotLeap as leapplot

# Example Positions
NUM_POINTS = 22 # See Columns below for formatting
points = np.array([
	[  26.89253807,  50.71062469,  26.30517006,  -6.53940153, -28.20298195,
	  -43.96928406,   1.59295416, -18.24504852, -15.59684658,  -9.10624218,
	   18.74389076,  -4.08834696, -18.99320984, -28.7378273,   36.90289307,
	   19.9671917,    6.81442356,  -2.79738522,  51.97451019,  43.90403748,
	   36.57212448,  28.60396194],
	 [ 35.12473297,  67.64217377,  79.15477753,  69.94815826,  60.34004593,
	   58.72478104,  32.09606171,  11.13847065,  16.22161102,  24.88112068,
	   22.31115341, -14.11880112, -31.75012016, -40.87027359,  15.9162302,
	  -20.30714417, -39.99034882, -51.30535889,  10.07509327, -20.53441429,
	  -36.16606903, -48.56869125],
	 [151.66641235, 123.82020569, 118.66936493, 147.56196594, 166.81466675,
	  180.52867126, 170.5990448,  145.15351868, 124.28096008, 113.46463776,
	  168.91151428, 165.07273865, 154.32685852, 144.07644653, 162.14595032,
	  160.73678589, 153.32025146, 145.6038208,  151.8303833, 152.60569763,
	  149.65892029, 145.08146667]
 ])

# Example Angles
angles = np.array([
	 [[ 6.80335651e-09, -4.51514916e-01, -1.10714834e+00],
	  [-2.12284823e-01, -1.89584131e-02,  4.08588116e-03],
	  [ 1.12782320e-01, -3.36439092e-09, -3.76808121e-09],
	  [-2.43190810e-01, -1.47738551e-08, -3.13275023e-09]],

	 [[ 1.51001870e-01, -1.66816955e-01, -2.52599157e-02],
	  [ 1.26234886e+00,  1.18541579e-03,  3.72051055e-03],
	  [ 1.10766007e+00, -9.07727204e-09,  1.62977681e-08],
	  [ 5.22654522e-01, -1.12897120e-08,  1.53981473e-08]],

	 [[ 1.48955348e-01, -2.95250742e-02,  1.46350714e-01],
	  [ 5.97808271e-01,  1.37448961e-01,  9.30286183e-02],
	  [ 3.72391062e-01, -4.33029963e-08, -9.43238189e-09],
	  [ 2.40749485e-01, -2.57356516e-08, -1.51517855e-08]],

	 [[ 1.50006118e-01,  1.21617516e-01,  2.20302218e-01],
	  [ 5.11299735e-01,  1.47075129e-01,  8.20371808e-02],
	  [ 3.06999060e-01,  2.59781033e-08, -1.21896506e-08],
	  [ 2.05311882e-01,  3.33055462e-08, -4.01401060e-09]],

	 [[ 1.09821361e-01,  2.62327266e-01,  3.74564087e-01],
	  [ 4.06376774e-01,  2.33796594e-01,  9.93673235e-02],
	  [ 2.64315977e-01,  2.51456589e-08,  2.37648319e-08],
	  [ 1.84392151e-01, -5.94240413e-09,  5.29384378e-09]]
])


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

# Matplotlib Setup
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close)
ax = fig.add_subplot(121, projection='3d', xlim=(-300, 300), ylim=(-200, 400), zlim=(-300, 300))
ax2 = fig.add_subplot(122, projection='3d', xlim=(-300, 300), ylim=(-200, 400), zlim=(-300, 300))
ax.view_init(elev=45., azim=122)
ax2.view_init(elev=45., azim=122)

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


def main():
	try:
		# Reset the plots
		leapplot.reset_plot(ax)
		leapplot.reset_plot(ax2)

		a_points = points

		if (points is not None):
			patches = ax.scatter(points[0], points[1], points[2], s=[10]*NUM_POINTS, alpha=1)
			leapplot.plot_points(points, patches)
			leapplot.plot_bone_lines(points, ax)

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
			angle_plot = ax2.scatter(a_points[0], a_points[1], a_points[2], s=[10]*NUM_POINTS, alpha=1)
			# Plot Angle points
			leapplot.plot_points(a_points, angle_plot)

			plt.show()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()


