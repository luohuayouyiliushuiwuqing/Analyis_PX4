#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ULOG解析器测试脚本
"""

import sys
import os
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from ulog_parser import ULogParser
import matplotlib.pyplot as plt


def test_parser(log_file):
    """测试ULOG解析器的所有功能"""
    print("=" * 80)
    print("ULOG解析器测试")
    print("=" * 80)

    try:
        # 1. 测试初始化
        print("\n1. 测试初始化...")
        parser = ULogParser(log_file)
        print(f"   ✓ 成功加载日志文件: {os.path.basename(log_file)}")
        print(f"   ✓ 总共包含 {len(parser.message_names)} 个主题")

        # 2. 测试数据获取方法
        print("\n2. 测试数据获取方法...")
        dataset = parser.get_dataset_safe('vehicle_attitude')
        print(f"   ✓ get_dataset_safe: {dataset is not None}")

        fields = parser.get_field_names('vehicle_attitude')
        print(f"   ✓ get_field_names: {len(fields)} 个字段")

        timestamps = parser.get_timestamps('vehicle_attitude')
        print(f"   ✓ get_timestamps: {len(timestamps)} 个时间戳")

        # 3. 测试数据显示方法
        print("\n3. 测试数据显示方法...")

        methods = [
            ('showVelocity', '速度'),
            ('show_attitude', '姿态'),
            ('show_position', '位置'),
            ('show_battery', '电池'),
            ('show_actuator', '电机'),
            ('show_sensor_data', '传感器'),
        ]

        for method_name, desc in methods:
            try:
                fig, ax = plt.subplots()
                if method_name == 'show_sensor_data':
                    getattr(parser, method_name)(ax, 'accel')
                else:
                    getattr(parser, method_name)(ax)
                plt.close(fig)
                print(f"   ✓ {desc}显示: 成功")
            except Exception as e:
                print(f"   ✗ {desc}显示: 失败 - {e}")

        # 4. 测试仪表板
        print("\n4. 测试仪表板...")
        try:
            parser.show_dashboard()
            print("   ✓ 仪表板显示: 成功")
        except Exception as e:
            print(f"   ✗ 仪表板显示: 失败 - {e}")

        # 5. 测试字段列表
        print("\n5. 测试字段列表...")
        try:
            parser.show_field_list('vehicle_attitude')
            print("   ✓ 字段列表显示: 成功")
        except Exception as e:
            print(f"   ✗ 字段列表显示: 失败 - {e}")

        # 6. 测试数据导出
        print("\n6. 测试数据导出...")
        try:
            output_file = 'test_vehicle_attitude.csv'
            result = parser.export_to_csv('vehicle_attitude', output_file)
            if result and os.path.exists(output_file):
                print(f"   ✓ 数据导出: 成功 ({output_file})")
                os.remove(output_file)  # 清理测试文件
            else:
                print("   ✗ 数据导出: 失败")
        except Exception as e:
            print(f"   ✗ 数据导出: 失败 - {e}")

        # 7. 测试主题列表
        print("\n7. 测试主题列表...")
        try:
            parser.get_data()
            print("   ✓ 主题列表显示: 成功")
        except Exception as e:
            print(f"   ✗ 主题列表显示: 失败 - {e}")

        # 8. 测试三维位置显示
        print("\n8. 测试三维位置显示...")
        try:
            # GPS三维显示
            fig = plt.figure(figsize=(10, 8))
            ax3d = fig.add_subplot(111, projection='3d')
            parser.show_3d_position(ax3d, use_gps=True)
            plt.close(fig)
            print("   ✓ 三维GPS位置显示: 成功")

            # 本地位置三维显示
            fig = plt.figure(figsize=(10, 8))
            ax3d = fig.add_subplot(111, projection='3d')
            parser.show_3d_position(ax3d, use_gps=False)
            plt.close(fig)
            print("   ✓ 三维本地位置显示: 成功")
        except Exception as e:
            print(f"   ✗ 三维位置显示: 失败 - {e}")

        # 9. 测试数据处理器方法
        print("\n9. 测试数据处理器方法...")
        try:
            attitude_data = parser.get_attitude_data()
            print(f"   ✓ get_attitude_data: {attitude_data is not None}")

            position_data = parser.get_position_data()
            print(f"   ✓ get_position_data: {position_data is not None}")

            velocity_data = parser.get_velocity_data()
            print(f"   ✓ get_velocity_data: {velocity_data is not None}")

            battery_data = parser.get_battery_data()
            print(f"   ✓ get_battery_data: {battery_data is not None}")
        except Exception as e:
            print(f"   ✗ 数据处理器方法: 失败 - {e}")

        print("\n" + "=" * 80)
        print("所有测试完成！")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    # 查找测试日志文件
    test_logs = [
        '/home/igs/yhj_demo/sim_projects/demo_analyis_px4/logs/log_42_2026-3-5-14-42-52.ulg',
        '/home/igs/yhj_demo/sim_projects/demo_analyis_px4/logs/log_37_2026-3-5-14-36-42.ulg',
    ]

    log_file = None
    for log in test_logs:
        if os.path.exists(log):
            log_file = log
            break

    if not log_file:
        print("错误: 未找到测试日志文件")
        print("请确保以下文件存在:")
        for log in test_logs:
            print(f"  - {log}")
        sys.exit(1)

    success = test_parser(log_file)
    sys.exit(0 if success else 1)
