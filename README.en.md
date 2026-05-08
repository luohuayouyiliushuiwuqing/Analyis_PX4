# PX4 ULog Analysis Tool

[English](#english-version) | 中文

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

# 1. Create data extractor
extractor = DataExtractor('flight_log.ulg')

# 2. Create data processor
processor = DataProcessor(extractor)

# 3. Create visualizer
visualizer = Visualizer(processor)

# 4. Display dashboard
visualizer.show_dashboard()
```

### Method 2: Using Coordinator (Backward Compatible)

```python
from ulog_parser import ULogParser

# Create parser
parser = ULogParser('flight_log.ulg')

# Get data and display
parser.show_dashboard()
```

### Method 3: Command Line Usage

```bash
python ulog_parser.py flight_log.ulg
```

## Supported Chart Types

| Type | Method | Description |
|------|--------|-------------|
| Velocity | `show_velocity()` | Display 3D velocity changes |
| Attitude | `show_attitude()` | Display flight attitude (Euler angles) |
| Position | `show_position()` | Display position changes |
| GPS Position | `show_gps_position()` | Display GPS position trajectory |
| 3D Position | `show_3d_position()` | Display 3D spatial trajectory |
| Battery | `show_battery()` | Display battery status |
| Actuators | `show_actuator()` | Display motor outputs |
| Sensors | `show_sensor_data()` | Display sensor data (accelerometer/gyroscope/magnetometer) |

## Code Structure

```
├── data_extractor.py      # Data extraction layer
├── data_processor.py     # Data processing layer
├── visualizer.py          # Visualization layer
├── ulog_parser.py        # Coordinator (backward compatible)
├── example_usage.py       # Usage examples
└── test_ulog_parser.py   # Test file
```

## Extension Examples

### Add New Data Processing Method

```python
# Add to data_processor.py
def get_custom_data(self):
    """Get custom data"""
    # Data processing logic
    return processed_data
```

### Add New Chart Type

```python
# Add to visualizer.py
def show_custom_chart(self, ax):
    """Display custom chart"""
    # Chart plotting logic
    pass
```

## License

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