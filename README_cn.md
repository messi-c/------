# Intelligent Cultural Tourism Guide Robot Based on Embodied AI and Multimodal Data Fusion

## 📖 Introduction

This project addresses the pain points of traditional manual guide services, such as slow information delivery and poor interactivity. It innovatively applies **embodied intelligence** and **multimodal data fusion** technologies to guide services. The robot is powered by the RDK X5 main controller, running ROS2, and deeply integrates perception data from LiDAR (Leishen N10), Orbbec depth camera, IMU, GPS, and 4G modules. It also deploys the Qwen3-VL embodied AI model to enable core functions including autonomous navigation, visitor following, voice interaction, and human-machine interaction. The project has been field-tested in libraries and other scenarios, providing an efficient solution for intelligent guidance.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Autonomous Navigation** | Combines laser SLAM, VSLAM, and GPS for seamless indoor/outdoor navigation and dynamic obstacle avoidance |
| **Visitor Following** | Uses depth camera and human tracking algorithms for stable one-to-one following guidance |
| **Voice Interaction** | Deploys Qwen3-VL model with multilingual recognition, real-time translation, and voiceprint localization |
| **Human-Machine Interface** | QT-based interface + WeChat Mini Program for location viewing, route query, and service calling |

---

## 🧠 Hardware Components

| Component | Model | Function |
|-----------|-------|----------|
| Main Controller | RDK X5 | Runs ROS2 and AI models |
| Motor Driver | STM32F407VET6 | Chassis motion control |
| LiDAR | Leishen N10 | Mapping and obstacle avoidance |
| Depth Camera | Orbbec | Visual perception, target tracking |
| IMU/GPS | — | Attitude monitoring and outdoor positioning |
| 4G Module | — | Remote data transmission |
| Microphone Array | iFlytek | Voice acquisition and voiceprint recognition |
| Touchscreen | — | Human-machine interaction |

---

## 🗂️ Software Architecture

### Development Environment
- **OS**: Ubuntu 22.04
- **ROS**: ROS2 Humble
- **Languages**: C++ / Python
- **Core Algorithms**: Navigation2, DWA, RTAB-Map, KCF tracking, Qwen3-VL

### Code Structure
```
project/
├── depend/                     # Third-party dependencies
├── navigation2-humble/         # Navigation2 framework source
├── ros2_astra_camera/          # Orbbec depth camera ROS2 driver
├── wheeltec_lidar_ros2/        # LiDAR ROS2 driver
├── turn_on_wheeltec_robot/     # Chassis core launch package
├── wheeltec_joy/               # Gamepad teleoperation
├── wheeltec_robot_keyboard/    # Keyboard teleoperation
├── wheeltec_robot_msg/         # Custom message definitions
├── wheeltec_robot_urdf/        # Robot URDF model
├── wheeltec_robot_slam/        # Laser SLAM mapping
├── wheeltec_robot_rtab/        # RTAB-Map visual SLAM
├── wheeltec_robot_nav2/        # Navigation and localization
└── simple_follower_ros2/       # Target following
```

---

## 🚀 Deployment & Usage

### 1. Environment Setup
```bash
# Install ROS2 Humble (refer to official docs)
# Create workspace
mkdir -p ~/robot_ws/src
cd ~/robot_ws/src
git clone <your-repo-url>
```

### 2. Build the Project
```bash
cd ~/robot_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

### 3. Sensor Driver Configuration
- LiDAR: Check serial port permissions, configure port parameters in `wheeltec_lidar_ros2`
- Depth Camera: Install Orbbec SDK, ensure USB connection
- IMU/GPS: Calibrate IMU, verify GPS signal

### 4. Launch Mapping
```bash
# Laser SLAM
ros2 launch wheeltec_robot_slam slam.launch.py

# Or RTAB-Map visual SLAM
ros2 launch wheeltec_robot_rtab rtabmap.launch.py
```

### 5. Launch Navigation
```bash
ros2 launch wheeltec_robot_nav2 nav2.launch.py map:=/path/to/map.yaml
```

### 6. Launch Visitor Following
```bash
ros2 launch simple_follower_ros2 follower.launch.py
```

### 7. Launch Voice Interaction
```bash
ros2 launch wheeltec_robot_voice voice.launch.py
```

### 8. Remote Monitoring (WeChat Mini Program)
Through MQTT bridging, the Mini Program can display robot position and call guidance services remotely.

---

## 📊 Competitor Comparison

| Competitor | Voice Localization | Real-time Translation | Recording | Positioning Accuracy | Response Time | Cost |
|------------|--------------------|----------------------|-----------|----------------------|---------------|------|
| Guohang    | ✓                  | ✓                    | ✗         | ±20cm                | ≤150ms        | High |
| Aobo       | ✓                  | ✗                    | ✗         | ±22cm                | ≤120ms        | High |
| Aiwa       | ✓                  | ✗                    | ✓         | ±23cm                | ≤130ms        | High |
| **Ours**   | **✓**              | **✓**                | **✓**     | **±25cm**            | **≤150ms**    | **Low** |

---

## 📄 References

[1] Xu Qihang, Li Ying, Liu Xuekai, et al. Lightweight pedestrian pose detection algorithm for guide robots[J]. Computer Measurement & Control, 2025, 33(05): 53-61.

[2] Wang Qi. Library intelligent guide robot control based on improved machine learning algorithm[J]. Modern Computer, 2024, 30(09): 66-69.

[3] Ge Xiguang. Design and navigation experiment of multi-sensor fusion system for indoor guide robot[D]. Zhejiang Normal University, 2023.

[4] Cheng Qichao, Zhou Jiawu. Design of voice-interactive guide robot[J]. Computer & Digital Engineering, 2021, 49(06): 1248-1252.

[5] Fan Yanwen. Key technologies and development trends of embodied intelligent robots[J]. Digital Technology & Application, 2025, 43(04): 19-21.

---

## 🤝 Contributing

Issues and Pull Requests are welcome.

## 📬 Contact

(Please add contact info)

## 📄 License

MIT License (or as you prefer)
