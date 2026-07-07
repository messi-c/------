# 基于具身智能与多模态数据融合的智能文旅导引机器人

## 📖 项目简介

本项目针对传统人工导览信息传递慢、交互性差等痛点，创新性地将**具身智能**与**多模态数据融合**技术应用于导览服务。机器人以 RDK X5 为核心主控，部署 ROS2 机器人操作系统，深度融合激光雷达（镭神 N10）、奥比中光深度相机、IMU 惯导、GPS 与 4G 模块的感知数据，并搭载 Qwen3-VL 具身智能模型，实现自动导航、旅客跟随、语音交互、人机交互等核心功能。项目已在图书馆等场景完成实地测试，为智能导览提供高效解决方案。

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| **自动导航** | 融合激光SLAM + VSLAM + GPS，实现室内外无缝导航与动态避障 |
| **旅客跟随** | 基于深度相机与人体跟踪算法，实现一对一稳定跟随导览 |
| **语音交互** | 部署 Qwen3-VL 模型，支持多语言识别、实时翻译、声纹定位 |
| **人机交互** | QT 界面 + 微信小程序，支持位置查看、路线查询、呼叫服务 |

---

## 🧠 硬件组成

| 组件 | 型号 | 作用 |
|------|------|------|
| 核心主控 | RDK X5 | 运行 ROS2 与 AI 模型 |
| 电机驱动 | STM32F407VET6 | 底盘运动控制 |
| 激光雷达 | 镭神 N10 | 建图与避障 |
| 深度相机 | 奥比中光 | 视觉感知、目标跟踪 |
| IMU/GPS | — | 姿态监测与室外定位 |
| 4G 模块 | — | 远程数据传输 |
| 麦克风阵列 | 科大讯飞 | 语音采集与声纹识别 |
| 触摸屏 | — | 人机交互界面 |

---

## 🗂️ 软件架构

### 开发环境
- **操作系统**：Ubuntu 22.04
- **ROS 版本**：ROS2 Humble
- **编程语言**：C++ / Python
- **核心算法**：Navigation2, DWA, RTAB-Map, KCF 跟踪, Qwen3-VL

### 代码结构
```
project/
├── depend/                     # 第三方依赖库与编译依赖
├── navigation2-humble/         # Navigation2 官方导航源码
├── ros2_astra_camera/          # 奥比中光深度相机 ROS2 驱动
├── wheeltec_lidar_ros2/        # 激光雷达 ROS2 驱动
├── turn_on_wheeltec_robot/     # 机器人底盘核心启动包
├── wheeltec_joy/               # 手柄遥控功能包
├── wheeltec_robot_keyboard/    # 键盘控制功能包
├── wheeltec_robot_msg/         # 自定义消息包
├── wheeltec_robot_urdf/        # 机器人 URDF 模型
├── wheeltec_robot_slam/        # 激光 SLAM 建图包
├── wheeltec_robot_rtab/        # RTAB-Map 视觉 SLAM 算法包
├── wheeltec_robot_nav2/        # 导航定位功能包
└── simple_follower_ros2/       # 目标跟随功能包
```

---

## 🚀 部署与使用

### 1. 环境准备
```bash
# 安装 ROS2 Humble（参考官方文档）
# 创建工作空间
mkdir -p ~/robot_ws/src
cd ~/robot_ws/src
git clone <your-repo-url>
```

### 2. 编译项目
```bash
cd ~/robot_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

### 3. 传感器驱动配置
- 激光雷达：确认串口权限，配置 `wheeltec_lidar_ros2` 中的端口参数
- 深度相机：安装奥比中光 SDK，确保 USB 连接正常
- IMU/GPS：校准 IMU，检查 GPS 信号

### 4. 启动建图
```bash
# 激光 SLAM 建图
ros2 launch wheeltec_robot_slam slam.launch.py

# 或启动 RTAB-Map 视觉 SLAM
ros2 launch wheeltec_robot_rtab rtabmap.launch.py
```

### 5. 启动导航
```bash
ros2 launch wheeltec_robot_nav2 nav2.launch.py map:=/path/to/map.yaml
```

### 6. 启动旅客跟随
```bash
ros2 launch simple_follower_ros2 follower.launch.py
```

### 7. 启动语音交互
```bash
ros2 launch wheeltec_robot_voice voice.launch.py
```

### 8. 远程监控（微信小程序）
通过 MQTT 桥接，微信小程序可实时查看机器人位置并呼叫导览服务。

---

## 📊 竞品对比

| 竞品 | 语音定位 | 实时翻译 | 录音 | 路径定位准度 | 线控响应时间 | 成本 |
|------|---------|---------|------|-------------|-------------|------|
| 国航 | ✓ | ✓ | ✗ | ±20cm | ≤150ms | 高 |
| 澳博 | ✓ | ✗ | ✗ | ±22cm | ≤120ms | 高 |
| 艾娃 | ✓ | ✗ | ✓ | ±23cm | ≤130ms | 高 |
| **本作品** | **✓** | **✓** | **✓** | **±25cm** | **≤150ms** | **低** |

---

## 📄 参考文献

[1] 徐启航, 李迎, 刘雪凯, 等. 用于导览机器人的轻量化行人姿态检测算法[J]. 计算机测量与控制, 2025, 33(05): 53-61.

[2] 王琦. 基于改进机器学习算法的图书馆智能导览机器人控制[J]. 现代计算机, 2024, 30(09): 66-69.

[3] 葛希逛. 室内导览机器人多传感器融合系统设计与导航试验研究[D]. 浙江师范大学, 2023.

[4] 程启超, 周家武. 语音交互导览机器人的设计[J]. 计算机与数字工程, 2021, 49(06): 1248-1252.

[5] 范彦文. 具身智能机器人关键技术及发展趋势[J]. 数字技术与应用, 2025, 43(04): 19-21.

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request。

## 📬 联系

（请补充联系方式）

## 📄 许可证

MIT License（可自行修改）
