#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PX4 ULOG 数据分析工具 - 主解析器类

整合数据提取、数据处理和UI显示三个层
"""

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from data_extractor import DataExtractor
from data_processor import DataProcessor
from visualizer import Visualizer


class ULogParser:
    """ULOG解析器 - 协调数据提取、处理和显示"""

    def __init__(self, ulog_file):
        """
        初始化ULOG解析器

        Args:
            ulog_file: ULOG文件路径
        """
        # 初始化各层组件
        self.data_extractor = DataExtractor(ulog_file)
        self.data_processor = DataProcessor(self.data_extractor)
        self.visualizer = Visualizer(self.data_processor)

        # 为了向后兼容，保留一些属性
        self.file_path = ulog_file
        self.message_names = self.data_extractor.get_all_message_names()
        self.categories = self.data_processor.get_categories()

    # ========== 数据提取方法 ==========

    def get_dataset_safe(self, name):
        """安全获取数据集"""
        return self.data_extractor.get_dataset_safe(name)

    def get_field_names(self, dataset_name):
        """获取数据集的所有字段名"""
        return self.data_extractor.get_field_names(dataset_name)

    def get_field_data(self, dataset_name, field_name):
        """获取指定数据集的字段数据"""
        return self.data_extractor.get_field_data(dataset_name, field_name)

    def get_timestamps(self, dataset_name):
        """获取数据集的时间戳"""
        return self.data_extractor.get_timestamps(dataset_name)

    # ========== 数据处理方法 ==========

    def get_attitude_data(self):
        """获取姿态数据"""
        return self.data_processor.get_attitude_data()

    def get_position_data(self):
        """获取位置数据"""
        return self.data_processor.get_position_data()

    def get_gps_position_data(self):
        """获取GPS位置数据"""
        return self.data_processor.get_gps_position_data()

    def get_3d_position_data(self, use_gps=True):
        """获取三维位置数据"""
        return self.data_processor.get_3d_position_data(use_gps)

    def get_velocity_data(self):
        """获取速度数据"""
        return self.data_processor.get_velocity_data()

    def get_battery_data(self):
        """获取电池状态数据"""
        return self.data_processor.get_battery_data()

    def get_actuator_data(self):
        """获取电机/舵机输出数据"""
        return self.data_processor.get_actuator_data()

    def get_sensor_data(self, sensor_type='accel'):
        """获取传感器数据"""
        return self.data_processor.get_sensor_data(sensor_type)

    # ========== UI显示方法 ==========

    def show_attitude(self, ax):
        """显示姿态数据"""
        self.visualizer.show_attitude(ax)

    def show_position(self, ax):
        """显示位置数据"""
        self.visualizer.show_position(ax)

    def show_gps_position(self, ax):
        """显示GPS位置数据"""
        self.visualizer.show_gps_position(ax)

    def show_3d_position(self, ax3d, use_gps=True):
        """显示三维位置轨迹"""
        self.visualizer.show_3d_position(ax3d, use_gps)

    def show_sensor_data(self, ax, sensor_type='accel'):
        """显示传感器数据"""
        self.visualizer.show_sensor_data(ax, sensor_type)

    def show_battery(self, ax):
        """显示电池状态"""
        self.visualizer.show_battery(ax)

    def show_actuator(self, ax):
        """显示电机/舵机输出"""
        self.visualizer.show_actuator(ax)

    def showVelocity(self, ax, offset=1):
        """显示速度数据（向后兼容）"""
        self.visualizer.show_velocity(ax, offset)

    def show_dashboard(self):
        """显示仪表板"""
        file_name = os.path.basename(self.file_path)
        self.visualizer.show_dashboard(file_name)

    def info(self, plot_type='velocity'):
        """显示图表信息"""
        file_name = os.path.basename(self.file_path)
        self.visualizer.show_info(plot_type, file_name)

    # ========== 数据导出方法 ==========

    def export_to_csv(self, dataset_name, output_path=None):
        """导出数据集到CSV文件"""
        try:
            import pandas as pd
        except ImportError:
            print("需要安装 pandas: pip install pandas")
            return False

        dataset = self.data_extractor.get_dataset(dataset_name)
        if not dataset:
            print(f"数据集 '{dataset_name}' 不存在")
            return False

        if output_path is None:
            output_path = f"{dataset_name}.csv"

        try:
            df = pd.DataFrame(dataset.data)
            df.to_csv(output_path, index=False)
            print(f"已导出 {dataset_name} 到 {output_path}")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False

    # ========== 信息显示方法 ==========

    def get_data(self):
        """显示所有主题信息"""
        print(f"\n{'=' * 80}")
        print(f"日志文件: {self.file_path}")
        print(f"总共包含 {len(self.message_names)} 个主题")
        print(f"{'=' * 80}\n")

        for category, topics in self.categories.items():
            if topics:
                print(f"【{category}】 ({len(topics)} 个主题)")
                print("-" * 60)
                for name in sorted(topics):
                    try:
                        dataset = self.data_extractor.get_dataset(name)
                        field_count = len(dataset.data.keys())
                        sample_count = len(list(dataset.data.values())[0]) if dataset.data else 0
                        print(f"  {name:45s} 字段: {field_count:3d}  样本: {sample_count:6d}")
                    except Exception as e:
                        print(f"  {name:45s} (无法读取: {str(e)[:30]})")
                print()

    def show_field_list(self, dataset_name):
        """显示指定数据集的所有字段"""
        dataset = self.data_extractor.get_dataset(dataset_name)
        if not dataset:
            print(f"数据集 '{dataset_name}' 不存在")
            return

        print(f"\n数据集: {dataset_name}")
        print(f"字段列表 ({len(dataset.data)} 个):")
        print("-" * 60)
        for field_name in sorted(dataset.data.keys()):
            data = dataset.data[field_name]
            if isinstance(data, np.ndarray):
                print(f"  {field_name:30s} 类型: {data.dtype}  长度: {len(data)}")
            else:
                print(f"  {field_name:30s} 类型: {type(data).__name__}")


def print_usage():
    """打印使用说明"""
    print("""
PX4 ULOG 数据分析工具
======================

用法:
    python ulog_parser.py <log_file> [选项]

选项:
    --list          显示所有主题列表
    --dashboard     显示仪表板（多个图表）
    --plot TYPE     显示指定类型的图表
                    可选类型: velocity, attitude, position, battery, actuator, sensor
    --3d [gps|pos]  显示三维位置轨迹 (gps: GPS数据, pos: 本地位置)
    --fields NAME   显示指定数据集的字段列表
    --export NAME   导出数据集到CSV文件
    --help          显示此帮助信息

示例:
    python ulog_parser.py log.ulg
    python ulog_parser.py log.ulg --list
    python ulog_parser.py log.ulg --plot attitude
    python ulog_parser.py log.ulg --3d gps
    python ulog_parser.py log.ulg --3d pos
    python ulog_parser.py log.ulg --fields vehicle_attitude
    python ulog_parser.py log.ulg --export vehicle_attitude
    """)


if __name__ == "__main__":
    # 默认日志文件路径
    default_log = ""

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='PX4 ULOG 数据分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python ulog_parser.py log.ulg              # 显示默认图表
  python ulog_parser.py log.ulg --list       # 显示所有主题
  python ulog_parser.py log.ulg --dashboard  # 显示仪表板
  python ulog_parser.py log.ulg --plot attitude  # 显示姿态图表
  python ulog_parser.py log.ulg --plot --scale 4 # 显示4倍速度图表
        """
    )
    parser.add_argument('log_file', nargs='?', default=default_log,
                        help='ULOG 日志文件路径')
    parser.add_argument('--list', '-l', action='store_true',
                        help='显示所有主题列表')
    parser.add_argument('--dashboard', action='store_true',
                        help='显示仪表板（多个图表）')
    parser.add_argument('--plot', '-p', type=str, nargs='?', const='velocity', default=None,
                        choices=['velocity', 'attitude', 'position', 'battery', 'actuator', 'sensor'],
                        help='显示指定类型图表，默认 velocity')
    parser.add_argument('--scale', '-s', type=float, default=1.0,
                        help='速度图倍率（仅 velocity 使用）')
    parser.add_argument('--3d', dest='plot_3d', type=str, choices=['gps', 'pos'],
                        help='显示三维位置轨迹 (gps: GPS数据, pos: 本地位置)')
    parser.add_argument('--fields', type=str,
                        help='显示指定数据集的字段列表')
    parser.add_argument('--export', type=str,
                        help='导出数据集到CSV文件')

    args = parser.parse_args()

    try:
        # 创建解析器实例
        parser = ULogParser(args.log_file)

        # 根据参数执行相应操作
        if args.list:
            parser.get_data()
        elif args.dashboard:
            parser.show_dashboard()
        elif args.plot_3d:
            # 显示三维位置轨迹
            use_gps = (args.plot_3d == 'gps')
            fig = plt.figure(figsize=(10, 8))
            ax3d = fig.add_subplot(111, projection='3d')
            parser.show_3d_position(ax3d, use_gps=use_gps)
            plt.tight_layout()
            plt.show()
        elif args.fields:
            parser.show_field_list(args.fields)
        elif args.export:
            parser.export_to_csv(args.export)
        elif args.plot is not None:
            if args.plot == 'velocity':
                fig, ax = plt.subplots()
                parser.showVelocity(ax, args.scale)
                plt.tight_layout()
                plt.show()
            else:
                parser.info(plot_type=args.plot)
        else:
            parser.show_dashboard()

    except FileNotFoundError as e:
        print(f"错误: {e}")
        print(f"请检查文件路径是否正确，或使用 --help 查看帮助")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
