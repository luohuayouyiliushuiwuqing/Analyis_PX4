#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用示例 - 展示如何使用分层架构的PX4日志分析工具
"""

import sys
import os
import matplotlib.pyplot as plt

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from data_extractor import DataExtractor
from data_processor import DataProcessor
from visualizer import Visualizer
from ulog_parser import ULogParser


def example_direct_usage():
    """示例：直接使用各层组件"""
    print("=" * 80)
    print("示例1: 直接使用各层组件")
    print("=" * 80)

    # 1. 使用数据提取器
    log_file = '/home/igs/yhj_demo/sim_projects/demo_analyis_px4/logs/log_42_2026-3-5-14-42-52.ulg'
    extractor = DataExtractor(log_file)
    print(f"\n1. 数据提取器:")
    print(f"   文件: {extractor.file_path}")
    print(f"   消息数量: {extractor.get_message_count()}")

    # 2. 使用数据处理器
    processor = DataProcessor(extractor)
    attitude_data = processor.get_attitude_data()
    if attitude_data:
        print(f"\n2. 数据处理器:")
        print(f"   姿态数据时间戳数量: {len(attitude_data['timestamps'])}")
        print(f"   滚转角范围: {attitude_data['roll'].min():.2f}° ~ {attitude_data['roll'].max():.2f}°")

    # 3. 使用可视化器
    visualizer = Visualizer(processor)
    print(f"\n3. 可视化器:")
    print(f"   已初始化，准备绘制图表")

    # 4. 绘制姿态图表
    fig, ax = plt.subplots(figsize=(10, 6))
    visualizer.show_attitude(ax)
    ax.set_title('姿态数据 - 直接使用组件')
    plt.tight_layout()
    plt.savefig('/tmp/attitude_direct.png')
    print(f"   姿态图表已保存到 /tmp/attitude_direct.png")
    plt.close()


def example_parser_usage():
    """示例：使用ULogParser协调者"""
    print("\n" + "=" * 80)
    print("示例2: 使用ULogParser协调者")
    print("=" * 80)

    log_file = '/home/igs/yhj_demo/sim_projects/demo_analyis_px4/logs/log_42_2026-3-5-14-42-52.ulg'

    # 使用协调者类（向后兼容）
    parser = ULogParser(log_file)
    print(f"\n1. 解析器初始化:")
    print(f"   文件: {parser.file_path}")
    print(f"   消息数量: {len(parser.message_names)}")

    # 获取数据
    attitude_data = parser.get_attitude_data()
    if attitude_data:
        print(f"\n2. 获取数据:")
        print(f"   姿态数据时间戳数量: {len(attitude_data['timestamps'])}")

    # 显示图表
    fig, ax = plt.subplots(figsize=(10, 6))
    parser.show_attitude(ax)
    ax.set_title('姿态数据 - 使用协调者')
    plt.tight_layout()
    plt.savefig('/tmp/attitude_parser.png')
    print(f"   姿态图表已保存到 /tmp/attitude_parser.png")
    plt.close()


def example_custom_visualization():
    """示例：自定义可视化"""
    print("\n" + "=" * 80)
    print("示例3: 自定义可视化")
    print("=" * 80)

    log_file = '/home/igs/yhj_demo/sim_projects/demo_analyis_px4/logs/log_42_2026-3-5-14-42-52.ulg'

    # 使用分层架构创建自定义可视化
    extractor = DataExtractor(log_file)
    processor = DataProcessor(extractor)
    visualizer = Visualizer(processor)

    # 获取多个数据集
    attitude_data = processor.get_attitude_data()
    velocity_data = processor.get_velocity_data()

    # 创建自定义图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # 姿态图表
    if attitude_data:
        ax1.plot(attitude_data['timestamps'], attitude_data['roll'], label='滚转角', linewidth=1)
        ax1.plot(attitude_data['timestamps'], attitude_data['pitch'], label='俯仰角', linewidth=1)
        ax1.plot(attitude_data['timestamps'], attitude_data['yaw'], label='偏航角', linewidth=1)
        ax1.set_xlabel('时间 (s)')
        ax1.set_ylabel('角度 (deg)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_title('姿态数据')

    # 速度图表
    if velocity_data:
        ax2.plot(velocity_data['timestamps'], velocity_data['vz'], label='垂直速度', linewidth=1)
        ax2.plot(velocity_data['timestamps'], velocity_data['vxy'], label='水平速度', linewidth=1)
        ax2.set_xlabel('时间 (s)')
        ax2.set_ylabel('速度 (m/s)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_title('速度数据')

    plt.tight_layout()
    plt.savefig('/tmp/custom_visualization.png')
    print(f"   自定义图表已保存到 /tmp/custom_visualization.png")
    plt.close()


if __name__ == "__main__":
    # 检查日志文件是否存在
    log_file = '/home/igs/yhj_demo/sim_projects/demo_analyis_px4/logs/log_42_2026-3-5-14-42-52.ulg'
    if not os.path.exists(log_file):
        print(f"错误: 日志文件不存在: {log_file}")
        sys.exit(1)

    # 运行示例
    example_direct_usage()
    example_parser_usage()
    example_custom_visualization()

    print("\n" + "=" * 80)
    print("所有示例完成！")
    print("=" * 80)
