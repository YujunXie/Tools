''' head pose estimation
library requirements: dlib opencv imutils

'''
import cv2
import dlib
import numpy as np
from imutils import face_utils

face_landmark_path = './shape_predictor_68_face_landmarks.dat'

# 14个3D人脸模型点
object_pts = np.float32([[6.825897, 6.760612, 4.402142],
                         [1.330353, 7.122144, 6.903745],
                         [-1.330353, 7.122144, 6.903745],
                         [-6.825897, 6.760612, 4.402142],
                         [5.311432, 5.485328, 3.987654],
                         [1.789930, 5.393625, 4.413414],
                         [-1.789930, 5.393625, 4.413414],
                         [-5.311432, 5.485328, 3.987654],
                         [2.005628, 1.409845, 6.165652],
                         [-2.005628, 1.409845, 6.165652],
                         [2.774015, -2.080775, 5.048531],
                         [-2.774015, -2.080775, 5.048531],
                         [0.000000, -3.116408, 6.097667],
                         [0.000000, -7.415691, 4.070434]])

# 8个3D映射点
reprojectsrc = np.float32([[10.0, 10.0, 10.0],
                           [10.0, 10.0, -10.0],
                           [10.0, -10.0, -10.0],
                           [10.0, -10.0, 10.0],
                           [-10.0, 10.0, 10.0],
                           [-10.0, 10.0, -10.0],
                           [-10.0, -10.0, -10.0],
                           [-10.0, -10.0, 10.0]])

# 绘制12个3D体坐标点
line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0],
              [4, 5], [5, 6], [6, 7], [7, 4],
              [0, 4], [1, 5], [2, 6], [3, 7]]


def get_head_pose(shape, im_shape):

    K = [im_shape[1], 0.0, im_shape[1]/2,
         0.0, im_shape[1], im_shape[0]/2,
         0.0, 0.0, 1.0]
    D = [0.0, 0.0, 0.0, 0.0]
    cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
    dist_coeffs = np.array(D).reshape(4, 1).astype(np.float32)

    # 选取68个关键点中的14个点
    image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                            shape[39], shape[42], shape[45], shape[31], shape[35],
                            shape[48], shape[54], shape[57], shape[8]])

    _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)

    reprojectdst, _ = cv2.projectPoints(reprojectsrc, rotation_vec, translation_vec, cam_matrix,
                                        dist_coeffs)

    reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))

    # calc euler angle
    rotation_mat, _ = cv2.Rodrigues(rotation_vec)
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

    return reprojectdst, euler_angle


def main():

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to connect to camera.")
        return
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            start_time = time.time()
            face_rects = detector(frame, 0)

            if len(face_rects) > 0:
                for i in range(len(face_rects)):
                    shape = predictor(frame, face_rects[i])
                    start_time = time.time()
                    shape = face_utils.shape_to_np(shape)

                    reprojectdst, euler_angle = get_head_pose(shape , frame.shape)
                    
                    for (x, y) in shape:
                        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                    for start, end in line_pairs:
                        cv2.line(frame, reprojectdst[start], reprojectdst[end], (0, 0, 255))

                    # (上下点头)
                    cv2.putText(frame, "pitch: " + "{:7.2f}".format(euler_angle[0, 0]), (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 0, 0), thickness=2)
                    # (左右摇头)
                    cv2.putText(frame, "yaw: " + "{:7.2f}".format(euler_angle[1, 0]), (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 0, 0), thickness=2)
                    # (左右摆头)
                    cv2.putText(frame, "roll: " + "{:7.2f}".format(euler_angle[2, 0]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 0, 0), thickness=2)

                cv2.imshow("test", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


if __name__ == '__main__':
    main()
