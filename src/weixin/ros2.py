import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSDurabilityPolicy, QoSReliabilityPolicy
import paho.mqtt.client as mqtt
import json
from nav_msgs.msg import OccupancyGrid
import math
import numpy as np
from tf2_ros import TransformListener, Buffer, TransformException
from rclpy.duration import Duration
from rclpy.time import Time

# MQTT配置
MQTT_BROKER = "192.168.1.29"
MQTT_PORT = 1883
MQTT_TOPIC_MAP = "ros2/map"
MQTT_TOPIC_POSE = "ros2/pose"
MQTT_CLIENT_ID = "ros2_mqtt_publisher"

class ROS2MQTTBridge(Node):
    def __init__(self):
        super().__init__('ros2_mqtt_bridge')
        self.map_received = False
        self.warmup_timer = None  # 预热定时器（替代oneshot）
        self.pose_timer = None    # 位姿查询定时器
        
        # MQTT初始化
        self.mqtt_client = mqtt.Client(
            client_id=MQTT_CLIENT_ID,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        try:
            self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.get_logger().info(f"成功连接到MQTT服务器: {MQTT_BROKER}:{MQTT_PORT}")
        except Exception as e:
            self.get_logger().error(f"连接MQTT服务器失败: {e}")
            raise SystemExit(1)
        self.mqtt_client.loop_start()
        
        # 地图订阅
        map_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE
        )
        self.map_sub = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            map_qos
        )
        self.get_logger().info("已订阅/map话题，等待地图数据...")

        # TF2初始化
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        # 兼容版：延迟1秒启动位姿定时器（无oneshot参数）
        self.warmup_timer = self.create_timer(1.0, self.start_pose_timer)
        self.get_logger().info("等待1秒加载TF缓存...")

    def start_pose_timer(self):
        """延迟启动位姿查询定时器（手动取消预热定时器）"""
        # 取消预热定时器（实现oneshot效果）
        if self.warmup_timer is not None:
            self.warmup_timer.cancel()
            self.warmup_timer = None
        # 启动位姿查询定时器（10Hz）
        self.pose_timer = self.create_timer(1.0, self.pose_callback)
        self.get_logger().info("位姿查询定时器已启动（10Hz）")

    def map_callback(self, msg: OccupancyGrid):
        """处理地图数据"""
        if self.map_received:
            return
        try:
            self.get_logger().info("===== 成功接收到地图数据 =====")
            map_data = {
                "width": msg.info.width,
                "height": msg.info.height,
                "resolution": msg.info.resolution,
                "origin_x": msg.info.origin.position.x,
                "origin_y": msg.info.origin.position.y,
                "origin_yaw": self.quaternion_to_yaw(msg.info.origin.orientation),
                "data": list(msg.data)
            }
            mqtt_msg = json.dumps(map_data, ensure_ascii=False)
            result = self.mqtt_client.publish(MQTT_TOPIC_MAP, mqtt_msg, qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.get_logger().info(f"成功发布地图到MQTT: {MQTT_TOPIC_MAP}")
                self.map_received = True
            else:
                self.get_logger().error(f"MQTT地图发布失败，错误码: {result.rc}")
        except Exception as e:
            self.get_logger().error(f"处理地图失败: {str(e)}")

    def pose_callback(self):
        """查询TF变换并发布位姿（核心修复）"""
        try:
            # 第一步：检查帧是否存在（关键！避免帧未初始化报错）
            if not self.tf_buffer.can_transform(
                target_frame='map',
                source_frame='base_link',
                time=Time(),
                timeout=Duration(seconds=0.1)
            ):
                self.get_logger().debug("map→base_link 帧暂不可用，跳过本次查询")
                return

            # 第二步：安全查询TF变换
            trans = self.tf_buffer.lookup_transform(
                'map',
                'base_link',
                Time(),  # 最新时间
                timeout=Duration(seconds=0.5)
            )

            # 提取位姿
            pose_data = {
                "x": round(trans.transform.translation.x, 3),
                "y": round(trans.transform.translation.y, 3),
                "yaw": round(self.quaternion_to_yaw(trans.transform.rotation), 3)
            }

            # 发布MQTT
            mqtt_msg = json.dumps(pose_data, ensure_ascii=False)
            result = self.mqtt_client.publish(MQTT_TOPIC_POSE, mqtt_msg, qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                # 可选：调试时打印
                # self.get_logger().info(f"发布位姿: {pose_data}")
                pass
            else:
                self.get_logger().error(f"MQTT位姿发布失败，错误码: {result.rc}")

        except TransformException as e:
            self.get_logger().debug(f"TF查询失败: {str(e)}")
        except Exception as e:
            self.get_logger().error(f"处理位姿失败: {str(e)}")

    def quaternion_to_yaw(self, q):
        """四元数转偏航角"""
        try:
            if q is None or (abs(q.w) < 1e-6 and abs(q.x) < 1e-6 and abs(q.y) < 1e-6 and abs(q.z) < 1e-6):
                return 0.0
            siny_cosp = 2 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
            yaw = math.atan2(siny_cosp, cosy_cosp)
            return yaw
        except Exception as e:
            self.get_logger().error(f"四元数转偏航角失败: {str(e)}")
            return 0.0

def main(args=None):
    rclpy.init(args=args)
    node = ROS2MQTTBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("接收到退出信号，正在关闭...")
    finally:
        # 安全释放所有定时器和资源
        if node.warmup_timer is not None:
            node.warmup_timer.cancel()
        if node.pose_timer is not None:
            node.pose_timer.cancel()
        node.mqtt_client.loop_stop()
        node.mqtt_client.disconnect()
        node.destroy_node()
        rclpy.shutdown()
        print("程序已安全退出")

if __name__ == '__main__':
    main()
