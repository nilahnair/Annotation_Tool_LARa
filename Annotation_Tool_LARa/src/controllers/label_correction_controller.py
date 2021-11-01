"""
Created on 09.07.2020

@author: Erik Altermann
@email: Erik.Altermann@tu-dortmund.de
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from os import sep
from .controller import Controller
import global_variables as g
from _functools import reduce

import pyqtgraph as pg
from controllers.controller import Graph


def mergeable(window_index_a: int, window_index_b: int) -> bool:
    """Checks whether two windows can be merged

    window_index_a should be smaller than window_index_b
    """
    if (window_index_a + 1 == window_index_b) and (window_index_a >= 0) and (
            window_index_b < len(g.windows.windows)):
        window_a = g.windows.windows[window_index_a]
        window_b = g.windows.windows[window_index_b]
        if window_a[2] == window_b[2]:
            a_and_b = [a == b for a, b in zip(window_a[3], window_b[3])]
            return reduce(lambda a, b: a and b, a_and_b)
    return False


class LabelCorrectionController(Controller):
    def __init__(self, gui):
        super(LabelCorrectionController, self).__init__(gui)

        self.was_enabled_once = False

        # self.windows = []
        self.current_window = -1

        self.setup_widgets()

    def setup_widgets(self):
        self.load_tab(f'..{sep}ui{sep}label_correction_mode.ui', "Label Correction")
        # ----Labels----
        self.current_window_label = self.widget.findChild(QtWidgets.QLabel, "lc_current_window_label")

        # ----Scrollbars----
        self.scrollBar = self.widget.findChild(QtWidgets.QScrollBar, "lc_scrollBar")
        self.scrollBar.valueChanged.connect(self.select_window)

        # ----LineEdits----
        # self. = self.widget.get_widget(QtWidgets.QLineEdit,"")
        self.split_at_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_split_at_lineEdit")
        self.move_start_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_move_start_lineEdit")
        self.move_end_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_move_end_lineEdit")

        self.start_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_start_lineEdit")
        self.end_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_end_lineEdit")

        # ----Buttons----
        self.merge_previous_button = self.widget.findChild(QtWidgets.QPushButton, "lc_merge_previous_button")
        self.merge_previous_button.clicked.connect(lambda _: self.merge_previous())
        self.merge_next_button = self.widget.findChild(QtWidgets.QPushButton, "lc_merge_next_button")
        self.merge_next_button.clicked.connect(lambda _: self.merge_next())
        self.merge_all_button = self.widget.findChild(QtWidgets.QPushButton, "lc_merge_all_button")
        self.merge_all_button.clicked.connect(lambda _: self.merge_all_adjacent())

        self.split_at_button = self.widget.findChild(QtWidgets.QPushButton, "lc_split_at_button")
        self.split_at_button.clicked.connect(lambda _: self.split())
        self.move_start_button = self.widget.findChild(QtWidgets.QPushButton, "lc_move_start_button")
        self.move_start_button.clicked.connect(lambda _: self.move_start())
        self.move_end_button = self.widget.findChild(QtWidgets.QPushButton, "lc_move_end_button")
        self.move_end_button.clicked.connect(lambda _: self.move_end())

        self.set_to_frame_split_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_frame_split_button")
        self.set_to_frame_split_button.clicked.connect(
            lambda _: self.split_at_lineEdit.setText(str(self.gui.get_current_frame() + 1)))
        self.set_to_frame_start_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_frame_start_button")
        self.set_to_frame_start_button.clicked.connect(
            lambda _: self.move_start_lineEdit.setText(str(self.gui.get_current_frame() + 1)))
        self.set_to_frame_end_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_frame_end_button")
        self.set_to_frame_end_button.clicked.connect(
            lambda _: self.move_end_lineEdit.setText(str(self.gui.get_current_frame() + 1)))
        self.set_to_start_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_start_button")
        self.set_to_start_button.clicked.connect(
            lambda _: self.move_start_lineEdit.setText(str(g.windows.windows[self.current_window][0] + 1)))
        self.set_to_end_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_end_button")
        self.set_to_end_button.clicked.connect(
            lambda _: self.move_end_lineEdit.setText(str(g.windows.windows[self.current_window][1] + 1)))

        self.window_by_frame_button = self.widget.findChild(QtWidgets.QPushButton, "lc_window__by_frame_button")
        self.window_by_frame_button.clicked.connect(lambda _: self.select_window_by_frame())

        # ----Class buttons----
        self.class_buttons = [QtWidgets.QRadioButton(text) for text in g.classes]
        self.class_layout = self.widget.findChild(QtWidgets.QGroupBox, "classesGroupBox").layout()

        for button in self.class_buttons:
            button.setEnabled(False)
            button.toggled.connect(lambda _: self.move_buttons(self.class_layout, self.class_buttons))
            button.clicked.connect(lambda _: self.change_class())
        self.move_buttons(self.class_layout, self.class_buttons)

        # ----Attribute buttons----
        self.attributeButtons = [QtWidgets.QCheckBox(text) for text in g.attributes]
        layout2 = self.widget.findChild(QtWidgets.QGroupBox, "attributesGroupBox").layout()

        for button in self.attributeButtons:
            button.setEnabled(False)
            button.toggled.connect(lambda _: self.move_buttons(layout2, self.attributeButtons))
            button.clicked.connect(lambda _: self.change_attributes())
        self.move_buttons(layout2, self.attributeButtons)

        # ----Class graph-----------
        self.class_graph = self.widget.findChild(pg.PlotWidget, 'lc_classGraph')

        # ----Status windows-------
        self.status_window = self.widget.findChild(QtWidgets.QTextEdit, 'lc_statusWindow')
        self.add_status_message("Here you can correct wrong Labels.")

    def enable_widgets(self):
        """"""

        if not self.was_enabled_once:
            self.class_graph = Graph(self.class_graph, 'class', interval_lines=False)
            self.was_enabled_once = True

        self.split_at_lineEdit.setValidator(QtGui.QIntValidator(0, g.data.number_samples + 1))
        self.move_start_lineEdit.setValidator(QtGui.QIntValidator(0, g.data.number_samples + 1))
        self.move_end_lineEdit.setValidator(QtGui.QIntValidator(0, g.data.number_samples + 1))

        self.class_graph.setup()
        self.class_graph.reload_classes(g.windows.windows)

        self.reload()

    def reload(self):
        """reloads all window information
        
        called when switching to label correction mode
        """
        # print("reloading LCC")
        self.class_graph.reload_classes(g.windows.windows)

        self.update_frame_lines(self.gui.get_current_frame())

        if g.windows is not None and len(g.windows.windows) > 0:
            self.set_enabled(True)
            self.select_window_by_frame()
            self.select_window(self.current_window)

        else:
            self.set_enabled(False)

    def set_enabled(self, enable: bool):
        """Turns the Widgets of Label Correction Mode on or off based on the enable parameter
        
        Arguments:
        ----------
        enable : bool
            If True and widgets were disabled, the widgets get enabled.
            If False and widgets were enabled, the widgets get disabled.
            Otherwise does nothing.
        ----------
        
        """
        # print("lcm.set_enabled:",\
        #      "\n\t self.enabled:",self.enabled,\
        #      "\n\t enable:",enable,\
        #      "\n\t revision:",self.fixed_window_mode_enabled)
        if not (self.fixed_window_mode_enabled is None or self.fixed_window_mode_enabled == "none"):
            self.split_at_lineEdit.setEnabled(False)
            self.move_start_lineEdit.setEnabled(False)
            self.move_end_lineEdit.setEnabled(False)

            self.merge_previous_button.setEnabled(False)
            self.merge_next_button.setEnabled(False)
            self.merge_all_button.setEnabled(False)

            self.split_at_button.setEnabled(False)
            self.move_start_button.setEnabled(False)
            self.move_end_button.setEnabled(False)

            self.set_to_frame_split_button.setEnabled(False)
            self.set_to_frame_start_button.setEnabled(False)
            self.set_to_frame_end_button.setEnabled(False)
            self.set_to_start_button.setEnabled(False)
            self.set_to_end_button.setEnabled(False)
        else:
            self.split_at_lineEdit.setEnabled(enable)
            self.move_start_lineEdit.setEnabled(enable)
            self.move_end_lineEdit.setEnabled(enable)

            self.merge_previous_button.setEnabled(enable)
            self.merge_next_button.setEnabled(enable)
            self.merge_all_button.setEnabled(enable)

            self.split_at_button.setEnabled(enable)
            self.move_start_button.setEnabled(enable)
            self.move_end_button.setEnabled(enable)

            self.set_to_frame_split_button.setEnabled(enable)
            self.set_to_frame_start_button.setEnabled(enable)
            self.set_to_frame_end_button.setEnabled(enable)
            self.set_to_start_button.setEnabled(enable)
            self.set_to_end_button.setEnabled(enable)

        if not (self.enabled == enable):
            # Only reason why it might be disabled is that there were no windows
            # Therefore setting the current window to 0 as this mode is enabled
            # as soon as there is at least one window
            self.enabled = enable
            for button in self.class_buttons:
                button.setEnabled(enable)
            for button in self.attributeButtons:
                button.setEnabled(enable)

            self.window_by_frame_button.setEnabled(enable)

            self.scrollBar.setEnabled(enable)

    def select_window(self, window_index: int):
        """Selects the window at window_index"""
        if window_index >= 0:
            self.current_window = window_index
        else:
            self.current_window = len(g.windows.windows) + window_index

        self.scrollBar.setRange(0, len(g.windows.windows) - 1)
        self.scrollBar.setValue(self.current_window)

        window = g.windows.windows[self.current_window]
        self.current_window_label.setText("Current Window: " +
                                          str(self.current_window + 1) + "/" + str(len(g.windows.windows)))
        self.start_lineEdit.setText(str(window[0] + 1))
        self.end_lineEdit.setText(str(window[1] + 1))

        self.class_buttons[window[2]].setChecked(True)
        for button, checked in zip(self.attributeButtons, window[3]):
            button.setChecked(checked)

        if self.fixed_window_mode_enabled == "prediction_revision":
            # print(window_index, len(g.windows.windows_1))
            top_buttons = [g.windows.windows_1[window_index][2],
                           g.windows.windows_2[window_index][2],
                           g.windows.windows_3[window_index][2]]
            for i, name in enumerate(g.classes):
                if i == top_buttons[0]:
                    self.class_buttons[i].setText(name + " (#1)")
                elif i == top_buttons[1]:
                    self.class_buttons[i].setText(name + " (#2)")
                elif i == top_buttons[2]:
                    self.class_buttons[i].setText(name + " (#3)")
                else:
                    self.class_buttons[i].setText(name)

        self.highlight_class_bar(window_index, )

    def highlight_class_bar(self, bar_index, **kwargs):
        colors = Controller.highlight_class_bar(self, bar_index)

        self.class_graph.color_class_bars(colors)

    def new_frame(self, frame):
        self.update_frame_lines(frame)
        window_index = self.class_window_index(frame)
        if self.enabled and (self.current_window != window_index):
            self.current_window = window_index
            self.highlight_class_bar(window_index, )
            self.select_window(window_index)

    def update_frame_lines(self, play=None):
        self.class_graph.update_frame_lines(play=play)

    def select_window_by_frame(self, frame=None):
        """Selects the Window around based on the current Frame shown
        
        """
        if frame is None:
            frame = self.gui.get_current_frame()
        window_index = self.class_window_index(frame)
        if window_index is None:
            window_index = -1
        # if the old and new index is the same do nothing.
        if self.current_window != window_index:
            self.current_window = window_index
            # self.reload()
            self.select_window(window_index)
        else:
            self.current_window = window_index

    def merge(self, window_index_a: int, window_index_b: int, check_mergeable=True, reload=True):
        """Tries to merge two windows"""
        if not check_mergeable or mergeable(window_index_a, window_index_b):
            window_b = g.windows.windows[window_index_b]
            g.windows.change_window(window_index_a, end=window_b[1], save=False)
            g.windows.delete_window(window_index_b, save=True)
            if self.current_window == len(g.windows.windows):
                self.current_window -= 1

            if reload:
                self.reload()

    def merge_all_adjacent(self):
        """Tries to merge all mergeable adjacent windows"""
        for i in range(len(g.windows.windows)):
            while mergeable(i, i + 1):
                self.merge(i, i + 1, False, False)
        self.reload()

    def merge_previous(self):
        """Tries to merge the current window with the previous"""

        if self.current_window == 0:
            self.add_status_message("Can't merge the first window with a previous window.")
        else:
            self.merge(self.current_window - 1, self.current_window)

    def merge_next(self):
        """Tries to merge the current window with the next"""

        if self.current_window == len(g.windows.windows) - 1:
            self.add_status_message("Can't merge the last window with a following window.")
        else:
            self.merge(self.current_window, self.current_window + 1)

    def split(self):
        """Splits the current window into two windows at a specified frame"""
        split_point = self.split_at_lineEdit.text()
        if split_point != '':
            split_point = int(self.split_at_lineEdit.text()) - 1
            window = g.windows.windows[self.current_window]
            if window[0] + 25 < split_point < window[1] - 25:
                g.windows.insert_window(self.current_window, window[0], split_point, window[2], window[3], False)
                g.windows.change_window(self.current_window + 1, start=split_point, save=True)
                # self.gui.reloadClasses()
                self.reload()
            else:
                self.add_status_message("The splitting point should be inside the current window")

    def move_start(self):
        """Moves the start frame of the current window to a specified frame
        
        Moves the end of the previous window too.
        """
        start_new = self.move_start_lineEdit.text()
        if start_new != '':
            if self.current_window > 0:
                window_previous = g.windows.windows[self.current_window - 1]
                window_current = g.windows.windows[self.current_window]
                start_new = int(self.move_start_lineEdit.text()) - 1
                if window_previous[0] + 50 < start_new:
                    if start_new < window_current[1] - 50:
                        g.windows.change_window(self.current_window - 1, end=start_new, save=False)
                        g.windows.change_window(self.current_window, start=start_new, save=True)
                        # self.gui.reloadClasses()
                        self.reload()
                    else:
                        self.add_status_message("A window can't start after it ended.")
                else:
                    self.add_status_message("A window can't start before a previous window.")
            else:
                self.add_status_message("You can't move the start point of the first window.")

    def move_end(self):
        """Moves the end frame of the current window to a specified frame
        
        Moves the start of the next window too.
        """
        end_new = self.move_end_lineEdit.text()
        if end_new != '':

            window_current = g.windows.windows[self.current_window]
            end_new = int(self.move_end_lineEdit.text())

            if window_current[0] + 50 < end_new:
                if self.current_window < len(g.windows.windows) - 1:
                    window_next = g.windows.windows[self.current_window + 1]
                    if end_new < window_next[1] - 50:
                        g.windows.change_window(self.current_window, end=end_new, save=False)
                        g.windows.change_window(self.current_window + 1, start=end_new, save=True)
                        # self.gui.reloadClasses()
                        self.reload()
                    else:
                        self.add_status_message("A window can't end after a following window ends.")
                else:
                    if end_new <= g.data.number_samples:
                        g.windows.change_window(self.current_window, end=end_new, save=True)
                        # self.gui.reloadClasses()
                        self.reload()
                    else:
                        self.add_status_message("A window can't end after the end of the data.")
            else:
                self.add_status_message("A window can't end before if started.")

    def change_class(self):
        for i, button in enumerate(self.class_buttons):
            if button.isChecked():
                g.windows.change_window(self.current_window, class_index=i, save=True)
        # self.reload()
        self.class_graph.reload_classes(g.windows.windows)
        self.highlight_class_bar(self.current_window, )

    def change_attributes(self):
        """Looks which Attribute buttons are checked and saves that to the current window"""

        attributes = []
        for button in self.attributeButtons:
            if button.isChecked():
                attributes.append(1)
            else:
                attributes.append(0)
        g.windows.change_window(self.current_window, attributes=attributes, save=True)
        # self.reload()
        self.class_graph.reload_classes(g.windows.windows)
        self.highlight_class_bar(self.current_window, )

    def move_buttons(self, layout: QtWidgets.QGridLayout, buttons: list):
        """Moves all the buttons in a layout
        
        Checked radio/checkbox buttons get moved to the left
        Unchecked buttons get moved to the right
        
        Arguments:
        ----------
        layout : QGridLayout
            the layout on which the buttons should be
        buttons : list
            a list of QRadioButtons or QCheckBox buttons, that should be moved in the layout
        """

        for i, button in enumerate(buttons):
            if button.isChecked():
                layout.addWidget(button, i + 1, 0)
            else:
                layout.addWidget(button, i + 1, 2)

    def get_start_frame(self) -> int:
        """returns the start of the current window"""
        if len(g.windows.windows) > 0:
            return g.windows.windows[self.current_window][0] + 1
        return 1

    def fixed_windows_mode(self, mode: str):
        self.fixed_window_mode_enabled = mode

        if mode is None or mode == "none":
            for i, name in enumerate(g.classes):
                self.class_buttons[i].setText(name)

        self.reload()


class LabelCorrectionControllerVideo(Controller):
    def __init__(self, gui):
        super(LabelCorrectionControllerVideo, self).__init__(gui)

        self.was_enabled_once = False

        # self.windows = []
        self.current_window = -1

        self.setup_widgets()

    def setup_widgets(self):
        self.load_tab(f'..{sep}ui{sep}label_correction_mode_v.ui', "Label Correction")
        # ----Labels----
        self.current_window_label = self.widget.findChild(QtWidgets.QLabel, "lc_current_window_label")

        # ----Scrollbars----
        self.scrollBar = self.widget.findChild(QtWidgets.QScrollBar, "lc_scrollBar")
        self.scrollBar.valueChanged.connect(self.select_window)

        # ----LineEdits----
        # self. = self.widget.get_widget(QtWidgets.QLineEdit,"")
        self.split_at_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_split_at_lineEdit")
        self.move_start_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_move_start_lineEdit")
        self.move_end_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_move_end_lineEdit")

        self.start_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_start_lineEdit")
        self.end_lineEdit = self.widget.findChild(QtWidgets.QLineEdit, "lc_end_lineEdit")

        # ----Buttons----
        self.merge_previous_button = self.widget.findChild(QtWidgets.QPushButton, "lc_merge_previous_button")
        self.merge_previous_button.clicked.connect(lambda _: self.merge_previous())
        self.merge_next_button = self.widget.findChild(QtWidgets.QPushButton, "lc_merge_next_button")
        self.merge_next_button.clicked.connect(lambda _: self.merge_next())
        self.merge_all_button = self.widget.findChild(QtWidgets.QPushButton, "lc_merge_all_button")
        self.merge_all_button.clicked.connect(lambda _: self.merge_all_adjacent())

        self.split_at_button = self.widget.findChild(QtWidgets.QPushButton, "lc_split_at_button")
        self.split_at_button.clicked.connect(lambda _: self.split())
        self.move_start_button = self.widget.findChild(QtWidgets.QPushButton, "lc_move_start_button")
        self.move_start_button.clicked.connect(lambda _: self.move_start())
        self.move_end_button = self.widget.findChild(QtWidgets.QPushButton, "lc_move_end_button")
        self.move_end_button.clicked.connect(lambda _: self.move_end())

        self.set_to_frame_split_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_frame_split_button")
        self.set_to_frame_split_button.clicked.connect(
            lambda _: self.split_at_lineEdit.setText(str(self.gui.get_current_frame() + 1)))
        self.set_to_frame_start_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_frame_start_button")
        self.set_to_frame_start_button.clicked.connect(
            lambda _: self.move_start_lineEdit.setText(str(self.gui.get_current_frame() + 1)))
        self.set_to_frame_end_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_frame_end_button")
        self.set_to_frame_end_button.clicked.connect(
            lambda _: self.move_end_lineEdit.setText(str(self.gui.get_current_frame() + 1)))
        self.set_to_start_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_start_button")
        self.set_to_start_button.clicked.connect(
            lambda _: self.move_start_lineEdit.setText(str(g.windows.windows[self.current_window][0] + 1)))
        self.set_to_end_button = self.widget.findChild(QtWidgets.QPushButton, "lc_set_end_button")
        self.set_to_end_button.clicked.connect(
            lambda _: self.move_end_lineEdit.setText(str(g.windows.windows[self.current_window][1] + 1)))

        self.window_by_frame_button = self.widget.findChild(QtWidgets.QPushButton, "lc_window__by_frame_button")
        self.window_by_frame_button.clicked.connect(lambda _: self.select_window_by_frame())

        # ----Attribute buttons----
        self.attribute_groups_and_dependencies()

        self.attributeButtons = [QtWidgets.QCheckBox(text) for text in g.attributes]
        self.setup_dependencies()
        scroll_area = self.widget.findChild(QtWidgets.QScrollArea, "scrollArea")
        layout = scroll_area.widget().layout()

        for button in self.attributeButtons:
            button.setEnabled(False)
            button.clicked.connect(lambda _: self.change_attributes())

        for group in self.attribute_groups:
            scroll_area = QtWidgets.QScrollArea(None)

            # scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            widget = QtWidgets.QWidget(None)
            v_box = QtWidgets.QVBoxLayout()
            for attr in group:
                v_box.addWidget(self.attributeButtons[attr])

            widget.setLayout(v_box)
            scroll_area.setWidget(widget)
            layout.addWidget(scroll_area)

        # ----Class graph-----------
        self.class_graph = self.widget.findChild(pg.PlotWidget, 'lc_classGraph')

        # ----Status windows-------
        self.status_window = self.widget.findChild(QtWidgets.QTextEdit, 'lc_statusWindow')
        self.add_status_message("Here you can correct wrong Labels.")

    def enable_widgets(self):
        """"""

        if not self.was_enabled_once:
            self.class_graph = Graph(self.class_graph, 'class', interval_lines=False,
                                     x_range=(0, g.videos.video_length))
            self.was_enabled_once = True

        self.split_at_lineEdit.setValidator(QtGui.QIntValidator(0, g.videos.video_length + 1))
        self.move_start_lineEdit.setValidator(QtGui.QIntValidator(0, g.videos.video_length + 1))
        self.move_end_lineEdit.setValidator(QtGui.QIntValidator(0, g.videos.video_length + 1))

        self.class_graph.setup()
        self.class_graph.reload_classes(g.windows.windows)

        self.reload()

    def reload(self):
        """reloads all window information

        called when switching to label correction mode
        """
        # print("reloading LCC")
        self.class_graph.reload_classes(g.windows.windows)

        self.update_frame_lines(self.gui.get_current_frame())

        if g.windows is not None and len(g.windows.windows) > 0:
            self.select_window_by_frame()
            self.select_window(self.current_window)
            self.set_enabled(True)

        else:
            self.set_enabled(False)

    def set_enabled(self, enable: bool):
        """Turns the Widgets of Label Correction Mode on or off based on the enable parameter

        Arguments:
        ----------
        enable : bool
            If True and widgets were disabled, the widgets get enabled.
            If False and widgets were enabled, the widgets get disabled.
            Otherwise does nothing.
        ----------

        """
        # print("lcm.set_enabled:",\
        #      "\n\t self.enabled:",self.enabled,\
        #      "\n\t enable:",enable,\
        #      "\n\t revision:",self.fixed_window_mode_enabled)
        if not (self.fixed_window_mode_enabled is None or self.fixed_window_mode_enabled == "none"):
            self.split_at_lineEdit.setEnabled(False)
            self.move_start_lineEdit.setEnabled(False)
            self.move_end_lineEdit.setEnabled(False)

            self.merge_previous_button.setEnabled(False)
            self.merge_next_button.setEnabled(False)
            self.merge_all_button.setEnabled(False)

            self.split_at_button.setEnabled(False)
            self.move_start_button.setEnabled(False)
            self.move_end_button.setEnabled(False)

            self.set_to_frame_split_button.setEnabled(False)
            self.set_to_frame_start_button.setEnabled(False)
            self.set_to_frame_end_button.setEnabled(False)
            self.set_to_start_button.setEnabled(False)
            self.set_to_end_button.setEnabled(False)
        else:
            self.split_at_lineEdit.setEnabled(enable)
            self.move_start_lineEdit.setEnabled(enable)
            self.move_end_lineEdit.setEnabled(enable)

            self.merge_previous_button.setEnabled(enable)
            self.merge_next_button.setEnabled(enable)
            self.merge_all_button.setEnabled(enable)

            self.split_at_button.setEnabled(enable)
            self.move_start_button.setEnabled(enable)
            self.move_end_button.setEnabled(enable)

            self.set_to_frame_split_button.setEnabled(enable)
            self.set_to_frame_start_button.setEnabled(enable)
            self.set_to_frame_end_button.setEnabled(enable)
            self.set_to_start_button.setEnabled(enable)
            self.set_to_end_button.setEnabled(enable)

        if not (self.enabled == enable):
            # Only reason why it might be disabled is that there were no windows
            # Therefore setting the current window to 0 as this mode is enabled
            # as soon as there is at least one window
            self.enabled = enable
            for button in self.attributeButtons:
                button.setEnabled(False)
            for i in self.attribute_groups[0]:
                self.attributeButtons[i].setEnabled(True)
            for i in [i for i, button in enumerate(self.attributeButtons) if button.isChecked()]:
                self.attributeButtons[i].setEnabled(True)

                for j in self.dependencies[i]:
                    self.attributeButtons[j].setEnabled(True)

            self.window_by_frame_button.setEnabled(enable)

            self.scrollBar.setEnabled(enable)

    def select_window(self, window_index: int):
        """Selects the window at window_index"""
        if window_index >= 0:
            self.current_window = window_index
        else:
            self.current_window = len(g.windows.windows) + window_index

        self.scrollBar.setRange(0, len(g.windows.windows) - 1)
        self.scrollBar.setValue(self.current_window)

        window = g.windows.windows[self.current_window]
        self.current_window_label.setText("Current Window: " +
                                          str(self.current_window + 1) + "/" + str(len(g.windows.windows)))
        self.start_lineEdit.setText(str(window[0] + 1))
        self.end_lineEdit.setText(str(window[1] + 1))

        for button, checked in zip(self.attributeButtons, window[3]):
            button.setChecked(checked)

        if self.fixed_window_mode_enabled == "prediction_revision":
            pass
        self.highlight_class_bar(window_index, )

    def highlight_class_bar(self, bar_index, **kwargs):
        colors = Controller.highlight_class_bar(self, bar_index,
                                                error_function=lambda window: window[2])

        self.class_graph.color_class_bars(colors)

    def new_frame(self, frame):
        self.update_frame_lines(frame)
        window_index = self.class_window_index(frame)
        if self.enabled and (self.current_window != window_index):
            self.current_window = window_index
            self.highlight_class_bar(window_index, )
            self.select_window(window_index)

    def update_frame_lines(self, play=None):
        self.class_graph.update_frame_lines(play=play)

    def select_window_by_frame(self, frame=None):
        """Selects the Window around based on the current Frame shown

        """
        if frame is None:
            frame = self.gui.get_current_frame()
        window_index = self.class_window_index(frame)
        if window_index is None:
            window_index = -1
        # if the old and new index is the same do nothing.
        if self.current_window != window_index:
            self.current_window = window_index
            # self.reload()
            self.select_window(window_index)
        else:
            self.current_window = window_index

    def merge(self, window_index_a: int, window_index_b: int, check_mergeable=True, reload=True):
        """Tries to merge two windows"""
        if not check_mergeable or mergeable(window_index_a, window_index_b):
            window_b = g.windows.windows[window_index_b]
            g.windows.change_window(window_index_a, end=window_b[1], save=False)
            g.windows.delete_window(window_index_b, save=True)
            if self.current_window == len(g.windows.windows):
                self.current_window -= 1

            if reload:
                self.reload()

    def merge_all_adjacent(self):
        """Tries to merge all mergeable adjacent windows"""
        for i in range(len(g.windows.windows)):
            while mergeable(i, i + 1):
                self.merge(i, i + 1, False, False)
        self.reload()

    def merge_previous(self):
        """Tries to merge the current window with the previous"""

        if self.current_window == 0:
            self.add_status_message("Can't merge the first window with a previous window.")
        else:
            self.merge(self.current_window - 1, self.current_window)

    def merge_next(self):
        """Tries to merge the current window with the next"""

        if self.current_window == len(g.windows.windows) - 1:
            self.add_status_message("Can't merge the last window with a following window.")
        else:
            self.merge(self.current_window, self.current_window + 1)

    def split(self):
        """Splits the current window into two windows at a specified frame"""
        split_point = self.split_at_lineEdit.text()
        if split_point != '':
            split_point = int(self.split_at_lineEdit.text()) - 1
            window = g.windows.windows[self.current_window]
            if window[0] + 25 < split_point < window[1] - 25:
                g.windows.insert_window(self.current_window, window[0], split_point, window[2], window[3], False)
                g.windows.change_window(self.current_window + 1, start=split_point, save=True)
                # self.gui.reloadClasses()
                self.reload()
            else:
                self.add_status_message("The splitting point should be inside the current window")

    def move_start(self):
        """Moves the start frame of the current window to a specified frame

        Moves the end of the previous window too.
        """
        start_new = self.move_start_lineEdit.text()
        if start_new != '':
            if self.current_window > 0:
                window_previous = g.windows.windows[self.current_window - 1]
                window_current = g.windows.windows[self.current_window]
                start_new = int(self.move_start_lineEdit.text()) - 1
                if window_previous[0] + 50 < start_new:
                    if start_new < window_current[1] - 50:
                        g.windows.change_window(self.current_window - 1, end=start_new, save=False)
                        g.windows.change_window(self.current_window, start=start_new, save=True)
                        # self.gui.reloadClasses()
                        self.reload()
                    else:
                        self.add_status_message("A window can't start after it ended.")
                else:
                    self.add_status_message("A window can't start before a previous window.")
            else:
                self.add_status_message("You can't move the start point of the first window.")

    def move_end(self):
        """Moves the end frame of the current window to a specified frame

        Moves the start of the next window too.
        """
        end_new = self.move_end_lineEdit.text()
        if end_new != '':

            window_current = g.windows.windows[self.current_window]
            end_new = int(self.move_end_lineEdit.text())

            if window_current[0] + 50 < end_new:
                if self.current_window < len(g.windows.windows) - 1:
                    window_next = g.windows.windows[self.current_window + 1]
                    if end_new < window_next[1] - 50:
                        g.windows.change_window(self.current_window, end=end_new, save=False)
                        g.windows.change_window(self.current_window + 1, start=end_new, save=True)
                        # self.gui.reloadClasses()
                        self.reload()
                    else:
                        self.add_status_message("A window can't end after a following window ends.")
                else:
                    if end_new <= g.data.number_samples:
                        g.windows.change_window(self.current_window, end=end_new, save=True)
                        # self.gui.reloadClasses()
                        self.reload()
                    else:
                        self.add_status_message("A window can't end after the end of the data.")
            else:
                self.add_status_message("A window can't end before if started.")

    def change_attributes(self):
        """Looks which Attribute buttons are checked and saves that to the current window"""

        attributes = []
        for button in self.attributeButtons:
            attributes.append(button.isChecked() + 0)

        g.windows.change_window(self.current_window, attributes=attributes, save=True)
        # self.reload()
        self.class_graph.reload_classes(g.windows.windows)
        self.highlight_class_bar(self.current_window)

    def get_start_frame(self) -> int:
        """returns the start of the current window"""
        if len(g.windows.windows) > 0:
            return g.windows.windows[self.current_window][0] + 1
        return 1

    def fixed_windows_mode(self, mode: str):
        self.fixed_window_mode_enabled = mode
        if mode is None or mode == "none":
            pass
        self.reload()

    def attribute_groups_and_dependencies(self):
        class_indexes = [i for i in range(len(g.attributes)) if "C_" in g.attributes[i]]
        akkusativ_indexes = [i for i in range(len(g.attributes)) if "A_" in g.attributes[i]]
        dativ_indexes = [i for i in range(len(g.attributes)) if "D_" in g.attributes[i]]
        dativ2_indexes = [i for i in range(len(g.attributes)) if "D2_" in g.attributes[i]]
        frequency_indexes = [i for i in range(len(g.attributes)) if "F_" in g.attributes[i]]
        self.attribute_groups = [class_indexes, akkusativ_indexes, dativ_indexes, dativ2_indexes, frequency_indexes]
        self.dependencies = {}
        for attributes1, attributes2 in [(class_indexes, akkusativ_indexes), (class_indexes, frequency_indexes),
                                         (akkusativ_indexes, dativ_indexes), (akkusativ_indexes, frequency_indexes),
                                         (dativ_indexes, dativ2_indexes), (dativ_indexes, frequency_indexes),
                                         (dativ2_indexes, frequency_indexes), (frequency_indexes, [])]:
            for attr_k in attributes1:
                if attr_k not in self.dependencies.keys():
                    self.dependencies[attr_k] = []
                for attr_v in attributes2:
                    if g.attribute_rep[attr_k, attr_v] > 0:
                        self.dependencies[attr_k].append(attr_v)

    def setup_dependencies(self):
        for group in self.attribute_groups[1:]:
            for j in group:
                self.attributeButtons[j].setEnabled(False)
        for i, group in enumerate(self.attribute_groups):
            for j in group:
                self.attributeButtons[j].clicked.connect(lambda _, g=i, b=j: self.update_dependencies(g, b))

    def update_dependencies(self, group_id, button_id):
        print(group_id, button_id)
        # print(g.windows.dataset)
        for i in self.attribute_groups[group_id]:  # Modify buttons in same Group
            if i == button_id:
                continue
            elif g.windows.dataset == "Brownie":  # Consider exceptions because of doubled attributes
                if button_id in [34, 35] and i in [34, 35]:
                    continue
                elif button_id in [53, 54] and i in [53, 54]:
                    continue
            elif g.windows.dataset == "Eggs":
                if button_id in [27, 28] and i in [27, 28]:
                    continue
                elif button_id in [29, 30] and i in [29, 30]:
                    continue
            elif g.windows.dataset == "Sandwich":
                if button_id in [10, 11] and i in [10, 11]:
                    continue

            self.attributeButtons[i].setChecked(False)

        if group_id + 1 == len(self.attribute_groups):
            return  # If group_id is the last group there is no other group that is dependent on it

        for group in self.attribute_groups[(group_id + 1):]:  # Modify buttons in next Groups
            # print(group)
            for i in group:
                button = self.attributeButtons[i]
                button.setEnabled(False)
                button.setChecked(False)

        for i in self.attribute_groups[group_id]:  # Enable dependencies
            if self.attributeButtons[i].isChecked():
                for j in self.dependencies[i]:
                    self.attributeButtons[j].setEnabled(True)
