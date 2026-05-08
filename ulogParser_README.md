# PX4 ULOG 数据分析工具

这是一个用于解析和可视化PX4飞行日志（ULOG格式）的Python工具。

## 架构设计

本项目采用分层架构，将数据提取、数据处理和UI显示分离：

```
┌─────────────────────────────────────────────────────────────┐
│                    ULogParser (协调者)                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  DataExtractor  │  │ DataProcessor   │  │ Visualizer   │ │
│  │  (数据提取层)    │  │ (数据处理层)    │  │ (UI显示层)   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 各层职责

1. **DataExtractor (数据提取层)**
   - 负责从ULOG文件读取原始数据
   - 提供安全的数据访问方法
   - 不包含任何业务逻辑或显示逻辑

2. **DataProcessor (数据处理层)**
   - 负责数据转换和计算
   - 四元数转欧拉角、速度计算等
   - 数据分类和组织

3. **Visualizer (UI显示层)**
   - 负责图表绘制和显示
   - 使用matplotlib进行可视化
   - 不包含数据处理逻辑

4. **ULogParser (协调者)**
   - 整合以上三个组件
   - 提供统一的API接口
   - 保持向后兼容性

## 功能特性

- **主题分类显示**：自动将日志主题按功能分类（飞行状态、姿态控制、位置导航等）
- **数据可视化**：支持多种图表类型显示
  - 速度图表（垂直速度和水平速度）
  - 姿态图表（滚转、俯仰、偏航角）
  - 位置图表（X、Y、Z坐标）
  - 电池状态图表（电压和电流）
  - 电机输出图表
  - 传感器数据图表（加速度计、陀螺仪、磁力计）
- **仪表板模式**：一次性显示所有关键数据的图表
- **数据导出**：支持将数据导出为CSV格式
- **字段查看**：查看指定数据集的所有字段

## 安装依赖

```bash
pip install pyulog matplotlib numpy pandas
```

## 使用方法

### 基本用法

```bash
# 显示默认图表（速度）
python ulog_parser.py <log_file.ulg>

# 显示帮助信息
python ulog_parser.py --help
```

### 查看所有主题

```bash
python ulog_parser.py <log_file.ulg> --list
```

### 显示仪表板

```bash
python ulog_parser.py <log_file.ulg> --dashboard
```

### 显示特定图表

```bash
# 速度图表
python ulog_parser.py <log_file.ulg> --plot velocity

# 姿态图表
python ulog_parser.py <log_file.ulg> --plot attitude

# 位置图表
python ulog_parser.py <log_file.ulg> --plot position

# 电池状态图表
python ulog_parser.py <log_file.ulg> --plot battery

# 电机输出图表
python ulog_parser.py <log_file.ulg> --plot actuator

# 传感器数据图表
python ulog_parser.py <log_file.ulg> --plot sensor
```

### 查看字段列表

```bash
python ulog_parser.py <log_file.ulg> --fields vehicle_attitude
```

### 导出数据到CSV

```bash
python ulog_parser.py <log_file.ulg> --export vehicle_attitude
```

## 主题分类

工具自动将日志主题分为以下类别：

- **飞行状态**：vehicle_status, commander_state, vehicle_control_mode, vehicle_land_detected
- **姿态控制**：vehicle_attitude, vehicle_attitude_setpoint, vehicle_rates_setpoint, vehicle_angular_velocity
- **位置导航**：vehicle_local_position, vehicle_global_position, vehicle_gps_position, vehicle_local_position_setpoint
- **EKF2 融合**：estimator_local_position, estimator_status, estimator_innovations, estimator_global_position, estimator_states
- **传感器数据**：sensor_combined, sensor_accel, sensor_gyro, sensor_mag, sensor_baro, sensor_gps
- **电机/舵机**：actuator_outputs, actuator_controls, actuator_motors, actuator_armed
- **外部定位**：vehicle_vision_position, vehicle_odometry, vehicle_visual_odometry
- **电池状态**：battery_status
- **遥控输入**：input_rc, manual_control_setpoint
- **其他**：未分类的主题

## 代码结构

- `data_extractor.py` - 数据提取层
  - `DataExtractor` 类：负责从ULOG文件读取原始数据
  - `get_dataset()`：获取数据集
  - `get_field_names()`：获取字段名
  - `get_field_data()`：获取字段数据
  - `get_timestamps()`：获取时间戳

- `data_processor.py` - 数据处理层
  - `DataProcessor` 类：负责数据处理和转换
  - `quaternion_to_euler()`：四元数转欧拉角
  - `get_attitude_data()`：获取姿态数据
  - `get_position_data()`：获取位置数据
  - `get_velocity_data()`：获取速度数据
  - `get_battery_data()`：获取电池数据

- `visualizer.py` - UI显示层
  - `Visualizer` 类：负责图表绘制和显示
  - `show_attitude()`：显示姿态图表
  - `show_position()`：显示位置图表
  - `show_dashboard()`：显示仪表板

- `ulog_parser.py` - 主解析器类
  - `ULogParser` 类：协调者，整合以上组件
  - 提供统一的API接口
  - 保持向后兼容性

## 示例输出

### 主题列表

```
================================================================================
日志文件: /path/to/log.ulg
总共包含 115 个主题
================================================================================

【飞行状态】 (4 个主题)
------------------------------------------------------------
  vehicle_control_mode                          字段:  16  样本:    578
  vehicle_land_detected                         字段:  13  样本:    309
  vehicle_status                                字段:  39  样本:    578

【姿态控制】 (4 个主题)
------------------------------------------------------------
  vehicle_angular_velocity                      字段:   8  样本:  14440
  vehicle_attitude                              字段:  11  样本:   5777
  ...
```

### 字段列表

```
数据集: vehicle_attitude
字段列表 (11 个):
------------------------------------------------------------
  delta_q_reset[0]               类型: float32  长度: 5777
  delta_q_reset[1]               类型: float32  长度: 5777
  q[0]                           类型: float32  长度: 5777
  q[1]                           类型: float32  长度: 5777
  q[2]                           类型: float32  长度: 5777
  q[3]                           类型: float32  长度: 5777
  ...
```

## 注意事项

1. 需要安装 `pyulog` 库来解析ULOG文件
2. 图表显示需要安装 `matplotlib`
3. 导出CSV需要安装 `pandas`
4. 某些主题可能无法读取，这取决于日志文件的内容

## 许可证

MIT License
