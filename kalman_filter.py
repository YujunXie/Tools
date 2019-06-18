import numpy as np 
import scipy.linalg

class KalmanFilter(object):
	"""A simple Kalman filter for tracking bounding boxes in image space.

	    The 8-dimensional state space

	    x, y, a, h, vx, vy, va, vh

	    contains the bounding box center position (x, y), aspect ratio a, height h,
	    and their respective velocities.

	    	Object motion follows a constant velocity model. The bounding box location
	    (x, y, a, h) is taken as direct observation of the state space (linear
	    observation model).
	"""
	def __init__(self):
		ndim, dt = 4, 1.

		self.F = np.eye(2 * ndim, 2 * ndim)
		for i in range(ndim):
			self.F[i, ndim+i] = dt
		self.H = np.eys(ndim, 2 * ndim)

		self._std_weight_position = 1. / 10.
		self._std_weight_velocity = 1. / 80.

	def initiate(self, measurement):
	"""Create track from unassociated measurement.

        Parameters
        ----------
        measurement : ndarray
            Bounding box coordinates (x, y, a, h) with center position (x, y),
            aspect ratio a, and height h.

        Returns
        -------
        (ndarray, ndarray)
            Returns the mean vector (8 dimensional) and covariance matrix (8x8
            dimensional) of the new track. Unobserved velocities are initialized
            to 0 mean.
    """

    	mean_pos = measurement
    	mean_vel = np.zeros_like(mean_pos)
	    mean = np.r_[mean_pos, mean_vel]

	    std = [
	    	2 * self._std_weight_position * measurement[3],
	        2 * self._std_weight_position * measurement[3],
	        1e-2,
	        2 * self._std_weight_position * measurement[3],
	        10 * self._std_weight_velocity * measurement[3],
	        10 * self._std_weight_velocity * measurement[3],
	        1e-5,
	        10 * self._std_weight_velocity * measurement[3]]
	    covariance = np.diag(np.square(std))
	    return mean_vel, covariance

	def predict(self, mean, covariance):
	"""Run Kalman filter prediction step.

        Parameters
        ----------
        mean : ndarray
            The 8 dimensional mean vector of the object state at the previous
            time step.
        covariance : ndarray
            The 8x8 dimensional covariance matrix of the object state at the
            previous time step.

        Returns
        -------
        (ndarray, ndarray)
            Returns the mean vector and covariance matrix of the predicted
            state. Unobserved velocities are initialized to 0 mean.
    """
		std_pos = [
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[3],
            1e-2,
            self._std_weight_position * mean[3]]
        std_vel = [
            self._std_weight_velocity * mean[3],
            self._std_weight_velocity * mean[3],
            1e-5,
            self._std_weight_velocity * mean[3]]
        Q = np.diag(np.square(np.r_[std_pos, std_vel]))
        mean = np.dot(self.F, mean)
        covariance = np.linalg.multi_dot((
        	self.F, covariance, self.F.T) + Q)
        return mean, covariance

    def project(self, mean, covariance):
    """Project state distribution to measurement space.

        Parameters
        ----------
        mean : ndarray
            The state's mean vector (8 dimensional array).
        covariance : ndarray
            The state's covariance matrix (8x8 dimensional).

        Returns
        -------
        (ndarray, ndarray)
            Returns the projected mean and covariance matrix of the given state
            estimate.
    """
    	std = [
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[3],
            1e-1,
            self._std_weight_position * mean[3]]
        R = np.diag(np.square(std))
        mean = np.dot(self.H, mean)
        covariance = np.linalg.multi_dot((
        	self.H, covariance, self.H.T))
        return mean, covariance + R

	def update(self, mean, covariance, measurement):
	"""Run Kalman filter correction step.

        Parameters
        ----------
        mean : ndarray
            The predicted state's mean vector (8 dimensional).
        covariance : ndarray
            The state's covariance matrix (8x8 dimensional).
        measurement : ndarray
            The 4 dimensional measurement vector (x, y, a, h), where (x, y)
            is the center position, a the aspect ratio, and h the height of the
            bounding box.

        Returns
        -------
        (ndarray, ndarray)
            Returns the measurement-corrected state distribution.
    """
    	projected_mean, projected_cov = self.project(mean, covariance)
    	chol_factor, lower = scipy.linalg.cho_factor(
            projected_cov, lower=True, check_finite=False)
        # 计算卡尔曼增益
        kalman_gain = scipy.linalg.cho_solve(
            (chol_factor, lower), np.dot(covariance, self._update_mat.T).T,
            check_finite=False).T
        d = measurement - projected_mean
        new_mean = mean + np.dot(d, kalman_gain.T)
        new_covariance = covariance - np.linalg.multi_dot((
        	kalman_gain, projected_cov, kalman_gain.T))
        return new_mean, new_covariance

from __future__ import print_function
from filterpy.kalman import KalmanFilter

class KalmanFilter(object):
	
	def __init__(self, measurement):
	"""Initialises a tracker using initial bounding box.
	"""
	    #define constant velocity model
	    # x：系统状态 z：观测值
	    self.kf = KalmanFilter(dim_x=7, dim_z=4)
	    # 状态转移矩阵
	    self.kf.F = np.array([[1,0,0,0,1,0,0],[0,1,0,0,0,1,0],[0,0,1,0,0,0,1],[0,0,0,1,0,0,0],  [0,0,0,0,1,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]])
	    # 测量矩阵
	    self.kf.H = np.array([[1,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,1,0,0,0,0],[0,0,0,1,0,0,0]])

	    # 测量噪声
	    self.kf.R[2:,2:] *= 10.
	    # 协方差矩阵
	    self.kf.P[4:,4:] *= 1000. #give high uncertainty to the unobservable initial velocities
	    self.kf.P *= 10.
	    # 系统过程噪声
	    self.kf.Q[-1,-1] *= 0.01
	    self.kf.Q[4:,4:] *= 0.01

	    # 观测值初始化
	    self.kf.x[:4] = measurement

	def update(self,measurement):
    """Updates the state vector with observed bbox.
    """
    	self.kf.update(measurement)

   	def predict(self):
    """Advances the state vector and returns the predicted bounding box estimate.
    """
    	if((self.kf.x[6]+self.kf.x[2])<=0):
      		self.kf.x[6] *= 0.0
    	return self.kf.predict()