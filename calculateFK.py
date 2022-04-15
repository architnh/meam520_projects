import numpy as np
from math import pi

class FK():

    def __init__(self):

        # TODO: you may want to define geometric parameters here that will be
        # useful in computing the forward kinematics. The data you will need
        # is provided in the lab handout


        pass

    def forward(self, q):
        """
        INPUT:
        q - 1x7 vector of joint angles [q0, q1, q2, q3, q4, q5, q6]

        OUTPUTS:
        jointPositions -8 x 3 matrix, where each row corresponds to a rotational joint of the robot or end effector
                  Each row contains the [x,y,z] coordinates in the world frame of the respective joint's center in meters.
                  The base of the robot is located at [0,0,0].
        T0e       - a 4 x 4 homogeneous transformation matrix,
                  representing the end effector frame expressed in the
                  world frame
        """

        # Your Lab 1 code starts here

        jointPositions = np.zeros((8,3))
        T0e = np.identity(4)

        q0 = q[0]
        q1 = q[1]
        q2 = q[2]
        q3 = q[3]
        q4 = q[4]
        q5 = q[5]
        q6 = q[6]

        a = np.array([0,0,0,0.0825,0.0825,0,0.088,0])
        alpha = np.array([0,-pi/2,pi/2,pi/2,pi/2,-pi/2,pi/2,0])
        d = np.array([0.141,0.192,0,0.316,0,0.384,0,0.21])
        theta = np.array([0,q0,q1,q2,pi+q3,q4,q5-pi,q6-pi/4])

        joint_excursion =  np.array([[0,0,0,1],
        			      [0,0,0,1],
        			      [0,0,0.195,1],
        			      [0,0,0,1],
        			      [0,0,0.125,1],
        			      [0,0,-0.015,1],
        			      [0,0,0.051,1],
        			      [0,0,0,1]])

        for i in range (0,8):

            A = np.array([[np.cos(theta[i]),-np.sin(theta[i]) * np.cos(alpha[i]),
                              np.sin(theta[i]) * np.sin(alpha[i]),a[i] * np.cos(theta[i])],
                             [np.sin(theta[i]),np.cos(theta[i]) * np.cos(alpha[i]),
                             -np.cos(theta[i]) * np.sin(alpha[i]),a[i] * np.sin(theta[i])],
                             [0,np.sin(alpha[i]),np.cos(alpha[i]),d[i]],
                             [0,0,0,1]]) #DH convention


            T0e = T0e @ A


            jointPositions[i,:] = (T0e @ joint_excursion[i,:].T)[:-1]

        # Your code ends here

        return jointPositions, T0e

    # feel free to define additional helper methods to modularize your solution for lab 1


    # This code is for Lab 2, you can ignore it ofr Lab 1
    def get_axis_of_rotation(self, q):
        """
        INPUT:
        q - 1x7 vector of joint angles [q0, q1, q2, q3, q4, q5, q6]

        OUTPUTS:
        axis_of_rotation_list: - 3x7 np array of unit vectors describing the axis of rotation for each joint in the
                                 world frame

        """
        # STUDENT CODE HERE: This is a function needed by lab 2
        z = np.zeros(shape = (3,7))
        T = self.compute_Ai(q)
        for i in range (0, len(T)):
            #z[0:3,x] = np.cross(axis[:, x], (on-joint_positions[x,:]))
            #z[3:6,x] = axis[:, x]
            z[0:3,i] = T[i][0:3,2]
            #np.append(z, T[i][:,2])
            #print(z)
            #print(" ")
        return(z)

    def compute_Ai(self, q):
        """
        INPUT:
        q - 1x7 vector of joint angles [q0, q1, q2, q3, q4, q5, q6]

        OUTPUTS:
        Ai: - 4x4 list of np array of homogenous transformations describing the FK of the robot. Transformations are not
              necessarily located at the joint locations

        """
        T = []
        for k in range(1, 8):
            jointPositions = np.zeros((8,3))
            T0k = np.identity(4)

            q0 = q[0]
            q1 = q[1]
            q2 = q[2]
            q3 = q[3]
            q4 = q[4]
            q5 = q[5]
            q6 = q[6]

            a = np.array([0,0,0,0.0825,0.0825,0,0.088,0])
            alpha = np.array([0,-pi/2,pi/2,pi/2,pi/2,-pi/2,pi/2,0])
            d = np.array([0.141,0.192,0,0.316,0,0.384,0,0.21])
            theta = np.array([0,q0,q1,q2,pi+q3,q4,q5-pi,q6-pi/4])

            joint_excursion =  np.array([[0,0,0,1],
            			      [0,0,0,1],
            			      [0,0,0.195,1],
            			      [0,0,0,1],
            			      [0,0,0.125,1],
            			      [0,0,-0.015,1],
            			      [0,0,0.051,1],
            			      [0,0,0,1]])

            for i in range (0,k):

                A = np.array([[np.cos(theta[i]),-np.sin(theta[i]) * np.cos(alpha[i]),
                                  np.sin(theta[i]) * np.sin(alpha[i]),a[i] * np.cos(theta[i])],
                                 [np.sin(theta[i]),np.cos(theta[i]) * np.cos(alpha[i]),
                                 -np.cos(theta[i]) * np.sin(alpha[i]),a[i] * np.sin(theta[i])],
                                 [0,np.sin(alpha[i]),np.cos(alpha[i]),d[i]],
                                 [0,0,0,1]]) #DH convention


                T0k = T0k @ A
            T.append(T0k)
        #print(T)
        return(T)

if __name__ == "__main__":

    np.set_printoptions(precision=3)
    fk = FK()

    # matches figure in the handout
    #q = np.array([0,0,0,-pi/2,0,pi/2,pi/4])
    q = np.array([-0.39266, -1.63911,  0.,      -2.48547,  0.,       0.84636,  0.39274])

    joint_positions, T0e = fk.forward(q)

    print("Joint Positions:\n",joint_positions)
    print("End Effector Pose:\n",T0e)
