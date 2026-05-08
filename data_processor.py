#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据处理层 - 负责数据处理和转换
"""

import numpy as np


class DataProcessor:
    """数据处理器 - 负责数据处理和转换"""

    def __init__(self, data_extractor):
        """
        初始化数据处理器

        Args:
            data_extractor: 数据提取器实例
        """
        self.data_extractor = data_extractor

    def quaternion_to_euler(self, q0, q1, q2, q3):
        """
        四元数转欧拉角

        Args:
            q0, q1, q2, q3: 四元数分量

        Returns:
            (roll, pitch, yaw) 欧拉角（弧度）
        """
        # roll (x-axis rotation)
        sinr_cosp = 2 * (q0 * q1 + q2 * q3)
        cosr_cosp = 1 - 2 * (q1 * q1 + q2 * q2)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        # pitch (y-axis rotation)
        sinp = 2 * (q0 * q2 - q3 * q1)
        pitch = np.arcsin(sinp)

        # yaw (z-axis rotation)
        siny_cosp = 2 * (q0 * q3 + q1 * q2)
        cosy_cosp = 1 - 2 * (q2 * q2 + q3 * q3)
        yaw = np.arctan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

    def get_attitude_data(self):
        """
        获取姿态数据（欧拉角）

        Returns:
            字典包含 timestamps, roll, pitch, yaw，如果数据不存在返回None
        """
        attitude = self.data_extractor.get_dataset("vehicle_attitude")
        if not attitude:
            return None

        timestamps = self.data_extractor.get_timestamps("vehicle_attitude")
        if timestamps is None:
            return None

        # 从四元数计算欧拉角
        q0 = attitude.data['q[0]']
        q1 = attitude.data['q[1]']
        q2 = attitude.data['q[2]']
        q3 = attitude.data['q[3]']

        roll, pitch, yaw = self.quaternion_to_euler(q0, q1, q2, q3)

        return {
            'timestamps': timestamps,
            'roll': np.degrees(roll),
            'pitch': np.degrees(pitch),
            'yaw': np.degrees(yaw)
        }

    def get_position_data(self):
        """
        获取位置数据（本地坐标）

        Returns:
            字典包含 timestamps, x, y, z，如果数据不存在返回None
        """
        pos = self.data_extractor.get_dataset("vehicle_local_position")
        if not pos:
            return None

        timestamps = self.data_extractor.get_timestamps("vehicle_local_position")
        if timestamps is None:
            return None

        return {
            'timestamps': timestamps,
            'x': pos.data['x'],
            'y': pos.data['y'],
            'z': pos.data['z']
        }

    def get_gps_position_data(self):
        """
        获取GPS位置数据

        Returns:
            字典包含 timestamps, lat, lon, alt，如果数据不存在返回None
        """
        gps = self.data_extractor.get_dataset("vehicle_global_position")
        if not gps:
            return None

        timestamps = self.data_extractor.get_timestamps("vehicle_global_position")
        if timestamps is None:
            return None

        return {
            'timestamps': timestamps,
            'lat': gps.data['lat'] * 1e-7,  # 转换为度
            'lon': gps.data['lon'] * 1e-7,  # 转换为度
            'alt': gps.data['alt']  # 海拔高度
        }

    def get_3d_position_data(self, use_gps=True):
        """
        获取三维位置数据

        Args:
            use_gps: True使用GPS数据，False使用本地位置数据

        Returns:
            字典包含 x, y, z 坐标，如果数据不存在返回None
        """
        if use_gps:
            gps_data = self.get_gps_position_data()
            if not gps_data:
                return None

            lat = gps_data['lat']
            lon = gps_data['lon']
            alt = gps_data['alt']

            # 将经纬度转换为近似米（在赤道附近）
            # 1度纬度 ≈ 111公里
            # 1度经度 ≈ 111公里 * cos(纬度)
            lat_m = (lat - lat[0]) * 111000
            lon_m = (lon - lon[0]) * 111000 * np.cos(np.radians(lat))
            alt_m = alt - alt[0]

            return {
                'x': lon_m,
                'y': lat_m,
                'z': alt_m,
                'label': 'GPS轨迹',
                'xlabel': '东向距离 (m)',
                'ylabel': '北向距离 (m)',
                'zlabel': '高度 (m)',
                'title': '三维GPS位置轨迹'
            }
        else:
            pos_data = self.get_position_data()
            if not pos_data:
                return None

            return {
                'x': pos_data['x'],
                'y': pos_data['y'],
                'z': -pos_data['z'],
                'label': '本地位置轨迹',
                'xlabel': 'X (m)',
                'ylabel': 'Y (m)',
                'zlabel': 'Z (m)',
                'title': '三维本地位置轨迹'
            }

    def get_velocity_data(self):
        """
        获取速度数据

        Returns:
            字典包含 timestamps, vz, vxy，如果数据不存在返回None
        """
        vehicle_local_position = self.data_extractor.get_dataset("vehicle_local_position")
        if not vehicle_local_position:
            return None

        timestamps = self.data_extractor.get_timestamps("vehicle_local_position")
        if timestamps is None:
            return None

        vx = vehicle_local_position.data['vx']
        vy = vehicle_local_position.data['vy']
        vz = vehicle_local_position.data['vz']

        vxy = np.sqrt(vx ** 2 + vy ** 2)

        return {
            'timestamps': timestamps,
            'vz': vz,
            'vxy': vxy
        }

    def get_battery_data(self):
        """
        获取电池状态数据

        Returns:
            字典包含 timestamps, voltage, current，如果数据不存在返回None
        """
        battery = self.data_extractor.get_dataset("battery_status")
        if not battery:
            return None

        timestamps = self.data_extractor.get_timestamps("battery_status")
        if timestamps is None:
            return None

        # 尝试不同的电压字段名
        voltage = None
        for field in ['voltage_v', 'voltage_filtered', 'voltage']:
            if field in battery.data:
                voltage = battery.data[field]
                break

        # 尝试不同的电流字段名
        current = None
        for field in ['current_a', 'current_filtered', 'current']:
            if field in battery.data:
                current = battery.data[field]
                break

        return {
            'timestamps': timestamps,
            'voltage': voltage,
            'current': current
        }

    def get_actuator_data(self):
        """
        获取电机/舵机输出数据

        Returns:
            字典包含 timestamps, channels，如果数据不存在返回None
        """
        actuator = self.data_extractor.get_dataset("actuator_motors")
        dataset_name = "actuator_motors"
        if not actuator:
            actuator = self.data_extractor.get_dataset("actuator_outputs")
            dataset_name = "actuator_outputs"
            if not actuator:
                return None

        timestamps = self.data_extractor.get_timestamps(dataset_name)
        if timestamps is None:
            return None

        # 尝试不同的字段名格式
        channels = {}
        for i in range(8):
            field_name = f'control[{i}]' if f'control[{i}]' in actuator.data else f'output[{i}]'
            if field_name in actuator.data:
                channels[f'channel_{i + 1}'] = actuator.data[field_name]

        return {
            'timestamps': timestamps,
            'channels': channels
        }

    def get_sensor_data(self, sensor_type='accel'):
        """
        获取传感器数据

        Args:
            sensor_type: 传感器类型 ('accel', 'gyro', 'mag')

        Returns:
            字典包含 timestamps, x, y, z，如果数据不存在返回None
        """
        if sensor_type == 'accel':
            dataset_name = 'sensor_accel'
            field_prefix = 'accel'
        elif sensor_type == 'gyro':
            dataset_name = 'sensor_gyro'
            field_prefix = 'gyro'
        elif sensor_type == 'mag':
            dataset_name = 'sensor_mag'
            field_prefix = 'mag'
        else:
            return None

        sensor = self.data_extractor.get_dataset(dataset_name)
        if not sensor:
            return None

        timestamps = self.data_extractor.get_timestamps(dataset_name)
        if timestamps is None:
            return None

        # 尝试不同的字段名格式
        field_names = [f for f in sensor.data.keys() if f.startswith(field_prefix)]
        if not field_names:
            return None

        # 获取每个轴的数据
        data = {'timestamps': timestamps}
        for i, field in enumerate(['x', 'y', 'z']):
            field_name = f'{field_prefix}[{i}]' if f'{field_prefix}[{i}]' in sensor.data else f'{field_prefix}_{field}'
            if field_name in sensor.data:
                data[field] = sensor.data[field_name]

        return data

    def get_categories(self):
        """
        获取主题分类

        Returns:
            主题分类字典
        """
        categories = {
            '飞行状态': ['vehicle_status', 'commander_state', 'vehicle_control_mode', 'vehicle_land_detected'],
            '姿态控制': ['vehicle_attitude', 'vehicle_attitude_setpoint', 'vehicle_rates_setpoint',
                         'vehicle_angular_velocity'],
            '位置导航': ['vehicle_local_position', 'vehicle_global_position', 'vehicle_gps_position',
                         'vehicle_local_position_setpoint'],
            'EKF2 融合': ['estimator_local_position', 'estimator_status', 'estimator_innovations',
                          'estimator_global_position', 'estimator_states'],
            '传感器数据': ['sensor_combined', 'sensor_accel', 'sensor_gyro', 'sensor_mag', 'sensor_baro', 'sensor_gps'],
            '电机/舵机': ['actuator_outputs', 'actuator_controls', 'actuator_motors', 'actuator_armed'],
            '外部定位': ['vehicle_vision_position', 'vehicle_odometry', 'vehicle_visual_odometry'],
            '电池状态': ['battery_status'],
            '遥控输入': ['input_rc', 'manual_control_setpoint'],
            '其他': []
        }

        # 自动分类未匹配的主题到"其他"
        message_names = self.data_extractor.get_all_message_names()
        matched_names = set()
        for category, keywords in categories.items():
            if category != '其他':
                for name in message_names:
                    if any(keyword in name for keyword in keywords):
                        matched_names.add(name)

        remaining = [name for name in message_names if name not in matched_names]
        categories['其他'] = remaining

        return categories

    def get_dataset_info(self, dataset_name):
        """
        获取数据集信息

        Args:
            dataset_name: 数据集名称

        Returns:
            数据集信息字典
        """
        dataset = self.data_extractor.get_dataset(dataset_name)
        if not dataset:
            return None

        field_count = len(dataset.data.keys())
        sample_count = len(list(dataset.data.values())[0]) if dataset.data else 0

        return {
            'name': dataset_name,
            'field_count': field_count,
            'sample_count': sample_count
        }

    def get_all_datasets_info(self):
        """
        获取所有数据集信息

        Returns:
            数据集信息列表
        """
        categories = self.get_categories()
        datasets_info = []

        for category, topics in categories.items():
            if topics:
                for name in sorted(topics):
                    info = self.get_dataset_info(name)
                    if info:
                        info['category'] = category
                        datasets_info.append(info)

        return datasets_info
