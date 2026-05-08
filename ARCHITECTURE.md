# PX4 日志分析工具 - 架构说明

## 项目结构

```
demo_analyis_px4/
├── data_extractor.py      # 数据提取层
├── data_processor.py      # 数据处理层
├── visualizer.py          # UI显示层
├── ulog_parser.py         # 主解析器（协调者）
├── test_ulog_parser.py    # 测试脚本
├── example_usage.py       # 使用示例
├── ARCHITECTURE.md        # 架构说明文档
├── ulogParser_README.md   # 用户文档
└── logs/                  # 日志文件目录
```

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

## 各层职责

### 1. DataExtractor (数据提取层)

**文件**: `data_extractor.py`

**职责**:
- 从ULOG文件读取原始数据
- 提供安全的数据访问方法
- 不包含任何业务逻辑或显示逻辑

**主要方法**:
- `get_dataset(name)`: 获取数据集
- `get_field_names(dataset_name)`: 获取字段名
- `get_field_data(dataset_name, field_name)`: 获取字段数据
- `get_timestamps(dataset_name)`: 获取时间戳

**优点**:
- 单一职责：只负责数据提取
- 易于测试：可以单独测试数据提取逻辑
- 可替换：可以轻松替换为其他数据源

### 2. DataProcessor (数据处理层)

**文件**: `data_processor.py`

**职责**:
- 数据转换和计算
- 四元数转欧拉角、速度计算等
- 数据分类和组织

**主要方法**:
- `quaternion_to_euler()`: 四元数转欧拉角
- `get_attitude_data()`: 获取姿态数据
- `get_position_data()`: 获取位置数据
- `get_velocity_data()`: 获取速度数据
- `get_battery_data()`: 获取电池数据
- `get_categories()`: 获取主题分类

**优点**:
- 业务逻辑集中：所有数据处理逻辑都在这里
- 可复用：不同的UI可以复用相同的数据处理逻辑
- 易于维护：修改数据处理逻辑不影响其他层

### 3. Visualizer (UI显示层)

**文件**: `visualizer.py`

**职责**:
- 图表绘制和显示
- 使用matplotlib进行可视化
- 不包含数据处理逻辑

**主要方法**:
- `show_attitude()`: 显示姿态图表
- `show_position()`: 显示位置图表
- `show_dashboard()`: 显示仪表板
- `show_3d_position()`: 显示三维位置

**优点**:
- 显示逻辑集中：所有图表绘制都在这里
- 可替换：可以轻松替换为其他UI框架（如Plotly、Bokeh）
- 易于定制：可以轻松创建自定义图表

### 4. ULogParser (协调者)

**文件**: `ulog_parser.py`

**职责**:
- 整合以上三个组件
- 提供统一的API接口
- 保持向后兼容性

**主要方法**:
- `__init__()`: 初始化各层组件
- 数据提取方法：`get_dataset_safe()`, `get_field_names()` 等
- 数据处理方法：`get_attitude_data()`, `get_position_data()` 等
- UI显示方法：`show_attitude()`, `show_position()` 等

**优点**:
- 向后兼容：保持与旧代码的兼容性
- 简化使用：提供统一的API接口
- 灵活性：用户可以直接使用各层组件，也可以使用协调者

## 使用方式

### 方式1: 直接使用各层组件（推荐）

```python
from data_extractor import DataExtractor
from data_processor import DataProcessor
from visualizer import Visualizer

# 1. 创建数据提取器
extractor = DataExtractor('log.ulg')

# 2. 创建数据处理器
processor = DataProcessor(extractor)

# 3. 创建可视化器
visualizer = Visualizer(processor)

# 4. 获取数据并显示
attitude_data = processor.get_attitude_data()
visualizer.show_attitude(ax)
```

### 方式2: 使用协调者（向后兼容）

```python
from ulog_parser import ULogParser

# 创建解析器
parser = ULogParser('log.ulg')

# 获取数据
attitude_data = parser.get_attitude_data()

# 显示图表
parser.show_attitude(ax)
```

## 优势

1. **关注点分离**: 数据提取、处理和显示逻辑分离，代码更清晰
2. **易于测试**: 各层可以单独测试
3. **易于扩展**: 可以轻松添加新的数据处理方法或图表类型
4. **易于维护**: 修改某一层不影响其他层
5. **灵活性**: 可以直接使用各层组件，也可以使用协调者

## 扩展示例

### 添加新的数据处理方法

```python
# 在 data_processor.py 中添加
def get_custom_data(self):
    """获取自定义数据"""
    # 数据处理逻辑
    return custom_data
```

### 添加新的图表类型

```python
# 在 visualizer.py 中添加
def show_custom_chart(self, ax):
    """显示自定义图表"""
    # 图表绘制逻辑
    pass
```

### 替换UI框架

```python
# 创建新的可视化器
class PlotlyVisualizer:
    def __init__(self, data_processor):
        self.data_processor = data_processor
    
    def show_attitude(self):
        # 使用Plotly绘制图表
        pass
```

## 注意事项

1. 各层之间通过接口通信，不直接访问内部实现
2. 数据提取层不包含业务逻辑
3. 数据处理层不包含显示逻辑
4. UI显示层不包含数据处理逻辑
5. 协调者类负责整合各层，提供统一接口
