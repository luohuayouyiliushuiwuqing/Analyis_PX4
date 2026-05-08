#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UI显示层 - 负责图表绘制和显示
"""

import matplotlib.pyplot as plt


class Visualizer:
    """可视化器 - 负责图表绘制和显示"""

    def __init__(self, data_processor):
        """
        初始化可视化器

        Args:
            data_processor: 数据处理器实例
        """
        self.data_processor = data_processor

        self.fly_mode = self.data_processor.get_fly_mode_data()
        self.mode_times = self.fly_mode['timestamps']
        self.mode_names = self.fly_mode['nav']

        self._setup_matplotlib()

    def _setup_matplotlib(self):
        """配置matplotlib样式"""
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
        plt.rcParams['axes.unicode_minus'] = False

    def compress_modes(self, mode_times, mode_names, end_time):
        segments = []

        if len(mode_times) == 0:
            return segments

        start = mode_times[0]
        prev_mode = mode_names[0]

        for i in range(1, len(mode_times)):
            if mode_names[i] != prev_mode:
                stop = mode_times[i]
                segments.append((start, stop, prev_mode))
                start = mode_times[i]
                prev_mode = mode_names[i]

        # last segment
        segments.append((start, end_time, prev_mode))

        return segments

    def add_mode_background(self, ax, mode_times, mode_names, end_time):
        segments = self.compress_modes(mode_times, mode_names, end_time)

        MODE_COLORS = {
            "Manual": "#f0f0f0",
            "Position": "#d0ebff",
            "Altitude": "#fff3bf",
            "Offboard": "#d3f9d8",
            "Mission": "#ffd8a8",
            "Hold": "#e5dbff",
            "Return": "#ffc9c9",
            "Land": "#ffe066",
        }

        for start, stop, mode in segments:
            color = MODE_COLORS.get(mode, "#eeeeee")
            ax.axvspan(
                start,
                stop,
                color=color,
                alpha=0.25
            )

    def show_attitude(self, ax):
        """
        显示姿态数据（俯仰、滚转、偏航）

        Args:
            ax: matplotlib坐标轴对象
        """
        attitude_data = self.data_processor.get_attitude_data()
        if not attitude_data:
            return

        ts = attitude_data['timestamps']
        self.add_mode_background(
            ax,
            self.mode_times,
            self.mode_names,
            ts[-1]
        )

        ax.plot(ts, attitude_data['roll'], label='滚转角 (deg)', linewidth=1)
        ax.plot(ts, attitude_data['pitch'], label='俯仰角 (deg)', linewidth=1)
        ax.plot(ts, attitude_data['yaw'], label='偏航角 (deg)', linewidth=1)
        ax.set_xlabel('时间 (s)')
        ax.set_ylabel('角度 (deg)')
        ax.grid(True, alpha=0.3)
        ax.legend()

    def show_position(self, ax):
        """
        显示位置数据（本地坐标）

        Args:
            ax: matplotlib坐标轴对象
        """
        pos_data = self.data_processor.get_position_data()
        if not pos_data:
            return

        ts = pos_data['timestamps']
        self.add_mode_background(
            ax,
            self.mode_times,
            self.mode_names,
            ts[-1]
        )

        ax.plot(ts, pos_data['x'], label='X (m)', linewidth=1)
        ax.plot(ts, pos_data['y'], label='Y (m)', linewidth=1)
        ax.plot(ts, pos_data['z'], label='Z (m)', linewidth=1)
        ax.set_xlabel('时间 (s)')
        ax.set_ylabel('位置 (m)')
        ax.grid(True, alpha=0.3)
        ax.legend()

    def show_gps_position(self, ax):
        """
        显示GPS位置数据

        Args:
            ax: matplotlib坐标轴对象
        """
        gps_data = self.data_processor.get_gps_position_data()
        if not gps_data:
            return

        ts = gps_data['timestamps']
        self.add_mode_background(
            ax,
            self.mode_times,
            self.mode_names,
            ts[-1]
        )

        ax.plot(ts, gps_data['lat'], label='纬度 (deg)', linewidth=1)
        ax.set_xlabel('时间 (s)')
        ax.set_ylabel('纬度 (deg)')
        ax.grid(True, alpha=0.3)
        ax.legend()

    def show_3d_position(self, ax3d, use_gps=True):
        """
        显示三维位置轨迹

        Args:
            ax3d: 3D坐标轴对象
            use_gps: True使用GPS数据，False使用本地位置数据
        """
        pos_data = self.data_processor.get_3d_position_data(use_gps)
        if not pos_data:
            return

        ax3d.plot(pos_data['x'], pos_data['y'], pos_data['z'],
                  linewidth=1, label=pos_data['label'])
        ax3d.set_xlabel(pos_data['xlabel'])
        ax3d.set_ylabel(pos_data['ylabel'])
        ax3d.set_zlabel(pos_data['zlabel'])
        ax3d.set_title(pos_data['title'])
        ax3d.grid(True, alpha=0.3)
        ax3d.legend()

        # 固定仰角，只允许左右旋转（水平旋转）
        ax3d.view_init(elev=30, azim=45)

    def show_sensor_data(self, ax, sensor_type='accel'):
        """
        显示传感器数据

        Args:
            ax: matplotlib坐标轴对象
            sensor_type: 传感器类型 ('accel', 'gyro', 'mag')
        """
        sensor_data = self.data_processor.get_sensor_data(sensor_type)
        if not sensor_data:
            return

        ts = sensor_data['timestamps']
        self.add_mode_background(
            ax,
            self.mode_times,
            self.mode_names,
            ts[-1]
        )

        # 设置ylabel
        if sensor_type == 'accel':
            ylabel = '加速度 (m/s²)'
        elif sensor_type == 'gyro':
            ylabel = '角速度 (rad/s)'
        elif sensor_type == 'mag':
            ylabel = '磁场 (gauss)'
        else:
            return

        # 绘制每个轴的数据
        for field in ['x', 'y', 'z']:
            if field in sensor_data:
                ax.plot(ts, sensor_data[field], label=f'{field.upper()}', linewidth=1)

        ax.set_xlabel('时间 (s)')
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend()

    def show_battery(self, ax):
        """
        显示电池状态

        Args:
            ax: matplotlib坐标轴对象
        """
        battery_data = self.data_processor.get_battery_data()
        if not battery_data:
            return

        timestamps = battery_data['timestamps']
        voltage = battery_data['voltage']
        current = battery_data['current']

        if voltage is not None:
            ax.plot(timestamps, voltage, label='电压 (V)', linewidth=1, color='blue')
            ax.set_xlabel('时间 (s)')
            ax.set_ylabel('电压 (V)', color='blue')
            ax.tick_params(axis='y', labelcolor='blue')
            ax.grid(True, alpha=0.3)

        if current is not None:
            ax2 = ax.twinx()
            ax2.plot(timestamps, current, label='电流 (A)', linewidth=1, color='red')
            ax2.set_ylabel('电流 (A)', color='red')
            ax2.tick_params(axis='y', labelcolor='red')

        if voltage is not None and current is not None:
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        elif voltage is not None:
            ax.legend()

    def show_actuator(self, ax):
        """
        显示电机/舵机输出

        Args:
            ax: matplotlib坐标轴对象
        """
        actuator_data = self.data_processor.get_actuator_data()
        if not actuator_data:
            return

        timestamps = actuator_data['timestamps']
        channels = actuator_data['channels']

        for channel_name, channel_data in channels.items():
            ax.plot(timestamps, channel_data, label=channel_name, linewidth=1)

        ax.set_xlabel('时间 (s)')
        ax.set_ylabel('输出值')
        ax.grid(True, alpha=0.3)
        ax.legend()

    def show_velocity(self, ax):
        """
        显示速度数据（垂直速度和水平速度）

        Args:
            ax: matplotlib坐标轴对象
        """
        velocity_data = self.data_processor.get_velocity_data()
        if not velocity_data:
            return

        ts = velocity_data['timestamps']
        self.add_mode_background(
            ax,
            self.mode_times,
            self.mode_names,
            ts[-1]
        )

        ax.plot(ts, velocity_data['vz'], label='垂直速度 (m/s)', linewidth=1)
        ax.plot(ts, velocity_data['vxy'], label='水平速度 (m/s)', linewidth=1)
        ax.minorticks_on()
        ax.grid(True, 'both', 'y')
        ax.set_xlabel('时间 (s)')
        ax.set_ylabel('速度 (m/s)')
        ax.legend()

    def show_dashboard(self, file_name=None):
        """
        显示仪表板，包含多个图表

        Args:
            file_name: 文件名，用于标题显示
        """
        figure = plt.figure(figsize=(15, 10))

        if file_name:
            figure.suptitle(f'PX4 ULOG 数据分析 - {file_name}', fontsize=16)

        # 速度图表
        ax1 = figure.add_subplot(2, 2, 1)
        self.show_velocity(ax1)
        ax1.set_title('速度')

        # 姿态图表
        ax2 = figure.add_subplot(2, 2, 2)
        self.show_attitude(ax2)
        ax2.set_title('姿态')

        # 位置图表
        ax3 = figure.add_subplot(2, 2, 3)
        self.show_position(ax3)
        ax3.set_title('位置')

        # 三维位置图表
        ax3d = figure.add_subplot(2, 2, 4, projection='3d')
        self.show_3d_position(ax3d, use_gps=False)

        plt.tight_layout()
        plt.show()

    def show_info(self, plot_type='velocity', file_name=None):
        """
        显示图表信息

        Args:
            plot_type: 图表类型 ('velocity', 'attitude', 'position', 'battery', 'actuator', 'sensor')
            file_name: 文件名，用于标题显示
        """
        figure = plt.figure(figsize=(12, 8))
        ax = figure.add_subplot(1, 1, 1)

        if plot_type == 'velocity':
            self.show_velocity(ax)
        elif plot_type == 'attitude':
            self.show_attitude(ax)
        elif plot_type == 'position':
            self.show_position(ax)
        elif plot_type == 'battery':
            self.show_battery(ax)
        elif plot_type == 'actuator':
            self.show_actuator(ax)
        elif plot_type == 'sensor':
            # 显示加速度计数据
            self.show_sensor_data(ax, 'accel')
        else:
            self.show_velocity(ax)

        if file_name:
            ax.set_title(f'{plot_type} - {file_name}')

        plt.tight_layout()
        plt.show()

    def show_3d_position_plot(self, use_gps=True, file_name=None):
        """
        显示三维位置轨迹

        Args:
            use_gps: True使用GPS数据，False使用本地位置数据
            file_name: 文件名，用于标题显示
        """
        fig = plt.figure(figsize=(10, 8))
        ax3d = fig.add_subplot(111, projection='3d')
        self.show_3d_position(ax3d, use_gps=use_gps)
        plt.tight_layout()
        plt.show()
