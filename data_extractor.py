#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据提取层 - 负责从ULOG文件提取原始数据
"""

import os
from datetime import datetime
from pyulog import ULog


class DataExtractor:
    """数据提取器 - 负责从ULOG文件读取原始数据"""

    def __init__(self, ulog_file):
        """
        初始化数据提取器

        Args:
            ulog_file: ULOG文件路径
        """
        if not os.path.exists(ulog_file):
            raise FileNotFoundError(f"日志文件不存在: {ulog_file}")

        self.file_path = ulog_file
        self.ulog = ULog(ulog_file)
        self.data_list = self.ulog.data_list
        self.message_names = [dataset.name for dataset in self.ulog.data_list]

    def get_dataset(self, name):
        """
        获取数据集

        Args:
            name: 数据集名称

        Returns:
            数据集对象，如果不存在返回None
        """
        try:
            return self.ulog.get_dataset(name)
        except:
            return None

    def get_dataset_safe(self, name):
        """
        安全获取数据集（别名方法）

        Args:
            name: 数据集名称

        Returns:
            数据集对象，如果不存在返回None
        """
        return self.get_dataset(name)

    def get_field_names(self, dataset_name):
        """
        获取数据集的所有字段名

        Args:
            dataset_name: 数据集名称

        Returns:
            字段名列表
        """
        dataset = self.get_dataset(dataset_name)
        if dataset:
            return list(dataset.data.keys())
        return []

    def get_field_data(self, dataset_name, field_name):
        """
        获取指定数据集的字段数据

        Args:
            dataset_name: 数据集名称
            field_name: 字段名称

        Returns:
            字段数据，如果不存在返回None
        """
        dataset = self.get_dataset(dataset_name)
        if dataset and field_name in dataset.data:
            return dataset.data[field_name]
        return None

    def get_timestamps(self, dataset_name):
        """
        获取数据集的时间戳

        Args:
            dataset_name: 数据集名称

        Returns:
            时间戳数组（秒，以第一个时间戳为起点），如果不存在返回None
        """
        dataset = self.get_dataset(dataset_name)
        if dataset and 'timestamp' in dataset.data:
            timestamps = dataset.data['timestamp']
            return (timestamps - timestamps[0]) / 1e6  # 转换为秒，以第一个时间戳为起点
        return None

    def get_start_gps_offset_timestamps(self):
        """
        获取起始 GPS 偏移时间戳
        Returns:
            第一个GPS时间戳，如果不存在返回None
        """
        dataset = self.get_dataset("vehicle_gps_position")
        if dataset is None or 'timestamp' not in dataset.data:
            return None
        ts = dataset.data['time_utc_usec']
        if len(ts) == 0:
            return None
        return ts[0] / 1e6

    def get_gps_offset_timestamps(self, dataset_name, return_datetime=False):
        """
        获取 GPS 偏移时间戳
        Args:
            dataset_name: 数据集名称
            return_datetime: 是否返回 datetime 对象（默认为 False，返回数值时间戳）
        Returns:
            GPS时间戳（数值或 datetime），如果不存在返回None
        """

        start_time = self.get_start_gps_offset_timestamps()
        d_time = self.get_timestamps(dataset_name)

        if d_time is None:
            return None

        offset_time = []
        if return_datetime:
            # 返回 datetime 对象（用于显示）
            for dt in d_time:
                offset_time.append(datetime.fromtimestamp(start_time + dt))
            return offset_time
        else:
            # 返回数值时间戳（用于绘图）
            for dt in d_time:
                offset_time.append(start_time + dt)
            return d_time

    def get_all_message_names(self):
        """
        获取所有消息名称

        Returns:
            消息名称列表
        """
        return self.message_names

    def get_message_count(self):
        """
        获取消息数量

        Returns:
            消息数量
        """
        return len(self.message_names)

    def get_file_info(self):
        """
        获取文件信息

        Returns:
            文件信息字典
        """
        return {
            'file_path': self.file_path,
            'file_name': os.path.basename(self.file_path),
            'message_count': self.get_message_count(),
            'message_names': self.message_names
        }
