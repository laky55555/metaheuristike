from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QSpinBox, QDoubleSpinBox
from robot import Robot


class RunRobotWidget(QWidget):
    """
    Widget for displaying robot moving through room.
    Include Room widget for drawing room and movement.
    """

    def __init__(self, parent=None, room_widget=None):
        """
        Initializing room_widget and buttons for movement.

        Parameters
        ----------
        parent : QWidget
            Widget in which we will draw buttons and room.
        room_widget : Room
            Widget that has all information about room and robot inside.

        """
        super().__init__(parent)

        self.parent = parent
        self.room_widget = room_widget
        self.robot = Robot(self.room_widget)

        self.preferences = QLabel('Preferences:')
        self.initialize_robot_buttons()
        self.initialize_genetic_buttons()
        self.initialize_robot_statistic()
        self.set_shortcuts()
        self.set_layout_positions()
        self.set_range_step_for_variables()
        self.set_default_genetic_parameters()
        self.initialize_on_click_buttons()

    def initialize_robot_buttons(self):
        self.button_move_one = QPushButton('Next move')
        self.button_move_one.setStatusTip('Make next move')
        self.button_move_all = QPushButton('Do all moves')
        self.button_move_all.setStatusTip('Make moves until end')
        self.button_back_one = QPushButton('Go back')
        self.button_back_one.setStatusTip('Undo move')
        self.button_restart = QPushButton('Restart')
        self.button_restart.setStatusTip('Restart map')

    def initialize_genetic_buttons(self):
        self.population = QSpinBox(self)
        self.population.setPrefix("Population size ")
        self.iterations = QSpinBox(self)
        self.iterations.setPrefix("Number of iterations ")
        self.mutation = QDoubleSpinBox(self)
        self.mutation.setPrefix("Mutation probability ")
        self.crossover = QDoubleSpinBox(self)
        self.crossover.setPrefix("Crossover probability ")

    def initialize_robot_statistic(self):
        self.number_of_moves = QLabel('Number of moves = 0')
        self.passed_distance = QLabel('Passed distance = 0')
        self.number_of_turns = QLabel('Number of turns = 0')
        self.number_of_multiple_visited = QLabel('Multiple visited = 0')

    def set_layout_positions(self):
        layout = QGridLayout()
        layout.addWidget(self.button_move_one, 1, 0)
        layout.addWidget(self.button_move_all, 1, 1)
        layout.addWidget(self.button_back_one, 1, 2)
        layout.addWidget(self.button_restart, 1, 3)
        layout.addWidget(self.preferences, 2, 0)
        layout.addWidget(self.population, 3, 0)
        layout.addWidget(self.iterations, 3, 1)
        layout.addWidget(self.mutation, 3, 2)
        layout.addWidget(self.crossover, 3, 3)
        layout.addWidget(self.robot.room_widget, 4, 0, 11, 3)
        layout.addWidget(self.number_of_moves, 4, 3)
        layout.addWidget(self.passed_distance, 6, 3)
        layout.addWidget(self.number_of_turns, 8, 3)
        layout.addWidget(self.number_of_multiple_visited, 10, 3)
        self.setLayout(layout)

    def set_range_step_for_variables(self):
        self.population.setRange(10, 500)
        self.iterations.setRange(1, 1000)
        self.mutation.setRange(0, 1)
        self.crossover.setRange(0, 1)
        self.mutation.setSingleStep(0.01)
        self.mutation.setDecimals(2)
        self.crossover.setSingleStep(0.01)
        self.crossover.setDecimals(2)

    def initialize_on_click_buttons(self):
        self.button_move_one.clicked.connect(self.make_one_move)
        self.button_move_all.clicked.connect(self.make_all_moves)
        self.button_back_one.clicked.connect(self.move_back)
        self.button_restart.clicked.connect(self.restart)

    def set_default_genetic_parameters(self):
        parameters = self.robot.get_default_genetic_parameters()
        self.population.setValue(parameters[0])
        self.iterations.setValue(parameters[1])
        self.mutation.setValue(parameters[2])
        self.crossover.setValue(parameters[3])

    def set_shortcuts(self):
        self.button_move_one.setShortcut('Ctrl+D')
        self.button_move_all.setShortcut('Ctrl+A')
        self.button_back_one.setShortcut('Ctrl+B')
        self.button_restart.setShortcut('Ctrl+R')

    def get_values(self):
        return ("genetic", self.population.value(), self.iterations.value(),
                self.mutation.value(), self.crossover.value())

    def update_robot_stats(self):
        self.number_of_moves.setText('Number of moves = ' + str(len(self.robot.room_widget.robot)-1))
        self.passed_distance.setText('Passed distance = ' + str(self.robot.room_widget.passed_distance))
        self.number_of_turns.setText('Number of turns = ' + str(self.robot.room_widget.number_of_turns))
        self.number_of_multiple_visited.setText('Multiple visited = ' + str(self.robot.room_widget.multiple_visits))

    def make_one_move(self):
        self.robot.move_one(self.get_values())
        self.update_robot_stats()

    def make_all_moves(self):
        self.robot.move_all(self.get_values())
        self.update_robot_stats()

    def move_back(self):
        self.robot.move_back()
        self.update_robot_stats()

    def restart(self):
        self.robot.restart()
        self.update_robot_stats()
