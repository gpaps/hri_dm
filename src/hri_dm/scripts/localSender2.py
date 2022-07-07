#!/usr/bin/env python
import rospy
import requests
from datetime import datetime

# import from files & fiware imports
from std_msgs.msg import String, Float64
from forthHRIHealthPost import HRI_HealthStatePost
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM, Pose2D

HRI_health_jsonFName = r"/home/gpapo/Desktop/hri_ws/src/hri_dm/scripts/HRI_health.json"
address = "25.45.111.204"
port = 1026

# publishers
pub2HRIDM = rospy.Publisher('taskExec_2HRIDM', TaskExecution2HRIDM, queue_size=100)
pub2Pose2D = rospy.Publisher('Robot_Pose2D', Pose2D, queue_size=100)
# pub2TaskExec = rospy.Publisher(, )

def get_requests(*args):
    r = requests.get("http://25.45.111.204:1026/v2/entities/" + str(args))
    print(r)

    # curl -get  "http://25.45.111.204:1026/v2/entities/"


def send_msg_taskexec2hri():
    global pub2HRIDM
    task_exec = TaskExecution2HRIDM()
    # For synchronization
    task_exec.request_id = 32
    # True if success; False if not
    task_exec.result = True
    # Error type e.g. “null”, “ArmExtFailed”, “ObjLocFailed”, ReachFailed”, “GraspingFailed”, “ArmHomingFailed”, “ArmRecoveryFailed”, “HandOverReachFailed”, “HandOverReleaseFailed”, “NavigationFailed”
    task_exec.error_type = 'null'
    rospy.loginfo(task_exec)
    pub2HRIDM.publish(task_exec)
    print('end_of_message_  sendS_msg_TASKExec2HRI and pub2HRIDM', '\n')


def send_msg_hri2task():
    task_exec2 = HRIDM2TaskExecution()
    task_exec2.action = 'release'  # action
    task_exec2.tool_id = -1
    # location/vector3 geom_msgs location
    task_exec2.location.x = 99999
    task_exec2.location.y = 99999
    task_exec2.location.z = 99999
    # location/nav Pose2D
    task_exec2.navpos.x = 0
    task_exec2.navpos.y = 0
    task_exec2.navpos.theta = 0.0
    # synchronization
    task_exec2.request_id = -1
    # rospy.loginfo(task_exec2)
    # print('end_of_message_  send_msg_HRI2TASK and pub2HRIDM', '\n')
    # pub2task.publish(task_exec2)


def send_msg_pose2d():
    global pub2Pose2D
    pose_task = Pose2D()
    pose_task.x = 1.1
    pose_task.y = 2.2
    pose_task.theta = 60.3
    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    pose_task.timestamp = my_date.isoformat()
    rospy.loginfo(pose_task)
    pub2Pose2D.publish(pose_task)
    print('end_of_message_  send_msg_pose2D and pub2Pose2D', '\n')


def native_sender():
    global result
    rospy.loginfo('sender node starts..')
    # send_msg_hri2task()
    send_msg_taskexec2hri()
    # send_msg_pose2d(), '\n'

if __name__ == '__main__':
    # init the 1st publisher  or init the first pub-in
    rospy.init_node('TaskExecution2HRIDM', anonymous=True)
    HRI_HealthStatePost(address, port, 'forth.ScenePerception.SystemHealth:001', HRI_health_jsonFName)
    # rospy.init_node('HRIDM2TaskExecution', anonymous=True)
    # pub1 = rospy.Publisher('HRIDM2_taskExec', HRIDM2TaskExecution, queue_size=10)

    # rate = rospy.Rate(0.5)  # t=1/f, where f =0.5 <-- rospyRate
    try:
        native_sender()
        # rospy.spin()
    except rospy.ROSInterruptException:
        pass
