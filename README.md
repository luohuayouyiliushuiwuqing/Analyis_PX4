

# PX4 ULog 日志分析工具

[English](#english-version) | 中文

一个功能强大的 PX4 飞行日志（ULog）分析工具，支持数据提取、处理和可视化。

## 功能特性

- **多层架构设计**：数据提取层、数据处理层、可视化层分离，易于维护和扩展
- **多种数据支持**：姿态、位置、GPS、速度、电池、电机输出、传感器数据
- **灵活的可视化**：支持 2D/3D 图表显示、仪表板导出
- **数据导出**：支持导出为 CSV 格式
- **向后兼容**：提供 ULogParser 协调者类，保持 API 兼容性

## 安装依赖

```bash
pip install pandas matplotlib pyulog
```

## 快速开始

### 方式一：直接使用各层组件（推荐）

```python
from data_extractor import DataExtractor
from data_processor import DataProcessor
from visualizer import Visualizer

# 1. 创建数据提取器
extractor = DataExtractor('flight_log.ulg')

# 2. 创建数据处理器
processor = DataProcessor(extractor)

# 3. 创建可视化器
visualizer = Visualizer(processor)

# 4. 显示仪表板
visualizer.show_dashboard()
```

### 方式二：使用协调者（向后兼容）

```python
from ulog_parser import ULogParser

# 创建解析器
parser = ULogParser('flight_log.ulg')

# 获取数据并显示
parser.show_dashboard()
```

### 方式三：命令行使用

```bash
python ulog_parser.py flight_log.ulg
```

## 支持的图表类型

| 类型 | 方法 | 说明 |
|------|------|------|
| 速度 | `show_velocity()` | 显示三维速度变化 |
| 姿态 | `show_attitude()` | 显示飞行姿态（欧拉角） |
| 位置 | `show_position()` | 显示位置变化 |
| GPS位置 | `show_gps_position()` | 显示 GPS 位置轨迹 |
| 3D位置 | `show_3d_position()` | 显示三维空间轨迹 |
| 电池 | `show_battery()` | 显示电池状态 |
| 电机 | `show_actuator()` | 显示电机输出 |
| 传感器 | `show_sensor_data()` | 显示传感器数据（加速度计/陀螺仪/磁力计） |

## 代码结构

```
├── data_extractor.py      # 数据提取层
├── data_processor.py     # 数据处理层
├── visualizer.py          # 可视化层
├── ulog_parser.py        # 协调者（向后兼容）
├── example_usage.py       # 使用示例
└── test_ulog_parser.py   # 测试文件
```

## 扩展示例

### 添加新的数据处理方法

```python
# 在 data_processor.py 中添加
def get_custom_data(self):
    """获取自定义数据"""
    # 数据处理逻辑
    return processed_data
```

### 添加新的图表类型

```python
# 在 visualizer.py 中添加
def show_custom_chart(self, ax):
    """显示自定义图表"""
    # 图表绘制逻辑
    pass
```

## 许可证

MIT License

---

## English Version

# PX4 ULog Analysis Tool

A powerful analysis tool for PX4 flight logs (ULog), supporting data extraction, processing, and visualization.

## Features

- **Layered Architecture**: Clear separation of data extraction, processing, and visualization layers
- **Multiple Data Support**: Attitude, position, GPS, velocity, battery, actuator, and sensor data
- **Flexible Visualization**: 2D/3D charts, dashboard export
- **Data Export**: Export to CSV format
- **Backward Compatible**: ULogParser coordinator class maintains API compatibility

## Installation

```bash
pip install pandas matplotlib pyulog
```

## Quick Start

### Method 1: Direct Component Usage (Recommended)

```python
from data_extractor import DataExtractor
from data_processor import DataProcessor
from visualizer import Visualizer

extractor = DataExtractor('flight_log.ulg')
processor = DataProcessor(extractor)
visualizer = Visualizer(processor)
visualizer.show_dashboard()
```

### Method 2: Using Coordinator (Backward Compatible)

```python
from ulog_parser import ULogParser

parser = ULogParser('flight_log.ulg')
parser.show_dashboard()
```

## License

MIT License