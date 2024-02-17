import os
import sys

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QCheckBox, QHBoxLayout, QLabel, \
    QPushButton, QTableWidget, QTableWidgetItem
from matplotlib.backend_bases import PickEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator


class Weapon:
    """
        武器
    """

    def __init__(self, name, one_damage, shoot_time, capacity, weapon_type, disruptor=0, hammer_point=0):
        self.name = name
        self.one_damage = one_damage
        self.shoot_time = shoot_time
        self.disruptor = disruptor
        self.hammer_point = hammer_point
        self.capacity = capacity
        self.weapon_type = weapon_type

    def comps_damage(self, times, shielded, reduce=0):
        """
            计算枪械某一枪的累计伤害
        """
        result_damage = 0
        for _ in range(times):
            one_damage_t = self.one_damage * (1 - reduce)
            if self.disruptor != 0 and result_damage + one_damage_t < shielded:
                one_damage_t = round(self.one_damage * (1 + self.disruptor))
            shield_health = max(0, shielded - result_damage)
            one_damage_t = max(0, one_damage_t - shield_health) * (1 + self.hammer_point) + min(one_damage_t,
                                                                                                shield_health)
            result_damage += round(one_damage_t)
        return result_damage


weapon_datas = [
    Weapon(name="猎兽", one_damage=15, weapon_type="冲锋枪", capacity=[20, 25, 30, 35],
           shoot_time=[1, 54, 102, 150, 202, 487, 523, 571, 619, 674, 952, 999, 1056, 1104, 1152, 1418, 1474, 1522,
                       1570,
                       1619, 1902, 1950, 2006, 2054, 2082, 2370, 2418, 2470, 2522, 2570, 2835, 2884, 2938, 2986,
                       3034]),
    Weapon(name="R99", one_damage=11, weapon_type="冲锋枪", capacity=[17, 20, 23, 26],
           shoot_time=[1, 66, 122, 183, 238, 286, 335, 387, 438, 504, 552, 619, 674, 723, 788, 838, 886, 952, 999,
                       1056, 1123,
                       1171, 1236, 1286, 1334, 1387]),
    Weapon(name="电冲", one_damage=15, weapon_type="冲锋枪", capacity=[19, 21, 23, 26],
           shoot_time=[1, 122, 183, 254, 335, 420, 504, 588, 674, 735, 838, 923, 999, 1086, 1171, 1255, 1334, 1418,
                       1502,
                       1585, 1666, 1750, 1838, 1922, 2006, 2082
                       ]),
    Weapon(name="CAR", one_damage=12, weapon_type="冲锋枪", capacity=[19, 21, 23, 26],
           shoot_time=[1, 66, 134, 202, 274, 335, 399, 474, 523, 588, 656, 723, 788, 855, 923, 988, 1038, 1104,
                       1171, 1236,
                       1303, 1370, 1434, 1502, 1550, 1619]),
    Weapon(name="转换者", one_damage=16, disruptor=0.2, weapon_type="冲锋枪", capacity=[19, 22, 25, 27],
           shoot_time=[1, 102, 202, 304, 399, 504, 599, 703, 814, 904, 1019, 1104, 1207, 1303, 1418, 1502, 1599,
                       1702, 1807,
                       1922, 2018, 2122, 2218, 2303, 2418, 2502, 2618]),
    Weapon(name="RE45", one_damage=12, hammer_point=0.35, weapon_type="冲锋枪", capacity=[16, 19, 22, 25],
           shoot_time=[1, 86, 150, 238, 304, 387, 474, 535, 619, 686, 788, 855, 935, 999, 1086, 1152, 1236, 1322,
                       1387, 1474,
                       1534, 1619, 1702, 1786, 1854]),
    Weapon(name="R301", one_damage=13, weapon_type="步枪",
           capacity=[18, 20, 25, 28],
           shoot_time=[1, 86, 150, 218, 304, 371, 455, 523, 599, 686, 751, 838, 904, 971, 1038, 1104, 1187, 1255, 1322,
                       1398, 1486, 1550, 1619, 1702, 1771, 1854, 1922, 1986]),
    Weapon(name="平行步枪", one_damage=18, weapon_type="步枪",
           capacity=[20, 25, 28, 30],
           shoot_time=[1, 122, 202, 323, 399, 504, 588, 686, 799, 904,
                       999, 1086, 1207, 1286, 1398, 1486, 1586, 1702, 1807, 1902,
                       2006, 2082, 2206, 2282, 2406, 2482, 2606, 2682, 2786, 2884]),

    Weapon(name="汗洛", one_damage=20, weapon_type="步枪",
           capacity=[18, 23, 27, 30],
           shoot_time=[1, 66, 134, 399, 474, 535, 814, 886, 952, 1219,
                       1286, 1350, 1634, 1702, 1750, 2054, 2122, 2170, 2454, 2522,
                       2587, 2870, 2938, 2986, 3282, 3350, 3418, 3682, 3750, 3818]),

    Weapon(name="喷火", one_damage=18, weapon_type="机枪",
           capacity=[35, 40, 45, 50],
           shoot_time=[1, 122, 238, 335, 455, 552, 674, 788, 904, 999,
                       1123, 1219, 1334, 1454, 1550, 1666, 1786, 1902, 2006, 2103,
                       2218, 2322, 2434, 2551, 2654, 2770, 2870, 2986, 3102, 3206,
                       3318, 3434, 3538, 3654, 3767, 3870, 3986, 4102, 4222, 4339,
                       4454, 4551, 4671, 4787, 4902, 5004, 5119, 5235, 5338, 5450]),
    Weapon(name="暴走", one_damage=26, weapon_type="机枪",
           capacity=[28, 32, 34, 40],
           shoot_time=[15, 203, 395, 594, 795, 1002, 1194, 1398, 1598, 1798,
                       1998, 2198, 2398, 2600, 2810, 2998, 3210, 3418, 3619, 3819,
                       4031, 4231, 4431, 4634, 4818, 5018, 5218, 5414, 5616, 5814,
                       6015, 6216, 6415, 6615, 6815, 7015, 7216, 7416, 7616, 7816]),
]

# 根据选中的甲类型重新绘制图表
shielded_data = {
    "红甲": ("红甲", 125, "red"),
    "紫甲": ("紫甲", 100, "purple"),
    "蓝甲": ("蓝甲", 75, "blue"),
    "白甲": ("白甲", 50, "#8d8f94"),
    "无甲": ("无甲", 0, "#13151a"),
}

legend_types = {
    "普通": 0,
    "胖子": 0.15
}

capacity_types = [
    "无",
    "白",
    "蓝",
    "紫"
]

weapon_types = [
    "全部",
    "冲锋枪",
    "步枪",
    "机枪"
]


class TimePointDamage(QMainWindow):
    """
        枪械伤害时间点
    """

    def __init__(self):
        super().__init__()
        self.setup_matplotlib()
        self.figure = None
        self.canvas = None
        self.ax = None
        self.annot = None
        # 保存图形对象的引用
        self.lines = []
        self.setup_matplotlib()
        self.init_ui()

    def init_ui(self):

        self.weapon_types_label = QLabel("枪械类型")
        self.weapon_types_combo = QComboBox(self)
        for weapon_type in weapon_types:
            self.weapon_types_combo.addItem(weapon_type)

        self.shielded_label = QLabel("护甲品质：")
        self.comboBox = QComboBox(self)
        for shielded_level in shielded_data:
            self.comboBox.addItem(shielded_level)
        self.legend_types_label = QLabel("传奇类型：")
        self.legend_types_combo = QComboBox(self)
        for legend_type in legend_types:
            self.legend_types_combo.addItem(legend_type)

        self.capacity_types_label = QLabel("弹匣类型：")
        self.capacity_types_combo = QComboBox(self)
        for capacity_type in capacity_types:
            self.capacity_types_combo.addItem(capacity_type)

        self.early_termination_check = QCheckBox(self)
        self.early_termination_check.setText("死亡终止")

        self.confirm_button = QPushButton("确定")
        self.confirm_button.clicked.connect(self.update_plot)

        # 布局设置
        layout = QVBoxLayout()
        param_layout = QHBoxLayout()
        param_layout.addWidget(self.weapon_types_label)
        param_layout.addWidget(self.weapon_types_combo)
        param_layout.addWidget(self.shielded_label)
        param_layout.addWidget(self.comboBox)
        param_layout.addWidget(self.legend_types_label)
        param_layout.addWidget(self.legend_types_combo)
        param_layout.addWidget(self.capacity_types_label)
        param_layout.addWidget(self.capacity_types_combo)
        param_layout.addWidget(self.early_termination_check)
        param_layout.addWidget(self.confirm_button)
        layout.addLayout(param_layout)
        layout.addWidget(self.canvas)

        central_widget = QWidget(None)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("冲锋枪各护甲同时间输出伤害对比")

    def update_plot(self):
        """
            下拉框修改不同甲的数据
        """
        # 获取选中的甲类型
        selected_shield = self.comboBox.currentText()
        legend_type = self.legend_types_combo.currentText()
        early_termination = self.early_termination_check.isChecked()
        capacity_type_index = self.capacity_types_combo.currentIndex()
        weapon_type = self.weapon_types_combo.currentText()
        result = self.plot_data(shielded=shielded_data[selected_shield], reduce=legend_types[legend_type],
                                early_termination=early_termination, capacity_type_index=capacity_type_index,
                                weapon_type=weapon_type)
        self.dte = DynamicTableExample(result)
        self.dte.show()

    def setup_matplotlib(self):
        """
            初始化mat plot lib
        """
        import matplotlib
        # 指定中文字体
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['font.family'] = 'SimHei'
        matplotlib.rcParams['font.size'] = 11
        matplotlib.rcParams['axes.unicode_minus'] = False
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('pick_event', self.on_pick)

    def plot_data(self, shielded, weapon_type, reduce=0, early_termination=False, capacity_type_index=3):
        """
            输出数据
        """
        shielded_name, shielded_health, shielded_color = shielded
        self.ax.clear()  # 清空原有的图表
        self.ax.xaxis.set_major_locator(MultipleLocator(50))
        self.ax.yaxis.set_major_locator(MultipleLocator(15))
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_facecolor('#f0f0f0')  # 浅灰色背景颜色
        # 创建注释对象
        self.annot = self.ax.annotate('', xy=(0, 0), xytext=(10, 10),
                                      textcoords='offset points',
                                      bbox=dict(boxstyle="round", fc="w"),
                                      arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)  # 初始时不可见

        self.ax.set_title('伤害对比')
        self.ax.set_xlabel('子弹射出时间（毫秒）', fontsize=12)
        self.ax.set_ylabel('累计造成伤害', fontsize=12)
        x_max = 0
        y_max = 0
        self.lines = []  # 清空保存的图形对象引用
        result = {}
        if weapon_type != "全部":
            weapon_type_datas = [weapon_data for weapon_data in weapon_datas if weapon_data.weapon_type == weapon_type]
        else:
            weapon_type_datas = weapon_datas

        for weapon_data in weapon_type_datas:
            weapon_name = weapon_data.name
            capacity = weapon_data.capacity[capacity_type_index]

            shoot_time = []
            damage_values = []
            kill_moment = None
            for i in range(len(weapon_data.shoot_time)):
                if i + 1 > capacity:
                    break
                one_damage = weapon_data.comps_damage(times=i + 1, shielded=shielded_health, reduce=reduce)
                shoot_time.append(weapon_data.shoot_time[i])
                damage_values.append(one_damage)
                if one_damage >= shielded_health + 100:
                    if kill_moment is None:
                        kill_moment = {"count": i + 1, "time": weapon_data.shoot_time[i], "damage": one_damage}
                    if early_termination:
                        break

            x_max_t = max(shoot_time)
            y_max_t = max(damage_values)
            x_max = max(x_max_t, x_max)
            y_max = max(y_max_t, y_max)
            line, = self.ax.plot(shoot_time, damage_values, marker='o', linestyle='-', label=weapon_name, markersize=4)
            line.set_pickradius(1)  # 设置选择半径，避免过于敏感
            line.set_picker(True)  # 启用 picker
            self.lines.append(line)  # 保存图形对象引用

            result_item = {"all_use_time": x_max_t}
            result_item["all_bullets"] = capacity
            result_item["all_damage"] = y_max_t
            if kill_moment is not None:
                result_item["is_kill"] = True
                result_item["kill_count"] = kill_moment["count"]
                result_item["kill_time"] = kill_moment["time"]
                result_item["kill_damage"] = kill_moment["damage"]
            else:
                result_item["is_kill"] = False
            result[weapon_name] = result_item

        self.ax.plot([0, x_max], [shielded_health + 100, shielded_health + 100], marker='o', linestyle='-',
                     color=shielded_color,
                     label=shielded_name,
                     markersize=3)
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(0, y_max)
        self.ax.legend(loc='lower right')
        # 刷新图表
        self.canvas.draw()
        return result

    def on_pick(self, event):
        """
            触发图标点，添加注释
        """
        if isinstance(event, PickEvent):
            artist = event.artist
            index = event.ind[0] if event.ind else None
            if index is not None and artist.get_label() != '':
                x_val = artist.get_xdata()[index]
                y_val = artist.get_ydata()[index]

                # 更新注释文本和位置
                text = f"子弹射出时间: {x_val:.0f}ms, 累计伤害: {y_val:.0f}"
                self.annot.set_text(text)
                self.annot.xy = (x_val, y_val)

                # 显示注释
                self.annot.set_visible(True)
                self.canvas.draw_idle()

    def closeEvent(self, event, **kwargs):
        os._exit(0)


class DynamicTableExample(QMainWindow):
    def __init__(self, result):
        super().__init__(None)
        self.initUI(result)

    def initUI(self, result):
        # 创建表格
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(9)  # 设置初始列数
        self.tableWidget.setHorizontalHeaderLabels(
            ["武器", "是否击杀", "击杀时长", "击杀使用弹容", "击杀伤害", "弹匣总大小", "弹匣总伤", "弹容剩余率",
             "打光弹匣耗时"])

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('对比结果')

        # 使用传递的数据填充表格
        self.populateTable(result)

    def populateTable(self, result):
        for weapon_type, result_item in result.items():
            all_use_time = result_item["all_use_time"]
            all_bullets = result_item["all_bullets"]
            all_damage = result_item["all_damage"]
            if not result_item["is_kill"]:
                row = [weapon_type, "否", "--", "--", "--", all_bullets, all_damage, "0%",
                       f"{all_use_time}ms"]
                self.addRow(row)
                continue

            kill_count = result_item["kill_count"]
            kill_time = result_item["kill_time"]
            kill_damage = result_item["kill_damage"]
            row = [weapon_type, "是", f"{kill_time}ms", kill_count, kill_damage, all_bullets, all_damage,
                   f"{round((all_bullets - kill_count) / all_bullets * 100, 2)}%", f"{all_use_time}ms"]
            self.addRow(row)
            # 调整列和行的大小，使其适应内容
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def addRow(self, row):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        for col, value in enumerate(row):
            item = QTableWidgetItem(str(value))
            self.tableWidget.setItem(row_position, col, item)


def main():
    """
        主方法
    """
    app = QApplication(sys.argv)
    frame_monitor = TimePointDamage()
    frame_monitor.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
