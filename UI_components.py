from PyQt5 import QtCore, QtGui, QtWidgets

def render_grid(window, parent, x, y):
    window.sub_grid = QtWidgets.QFrame(parent)
    window.sub_grid.setGeometry(QtCore.QRect(x, y, 540, 540))
    font = QtGui.QFont()
    font.setPointSize(24)
    window.sub_grid.setFont(font)

    for row in range(9):
        for col in range(9):
            window.field[row][col] = QtWidgets.QLineEdit(window.sub_grid)
            window.field[row][col].setGeometry(QtCore.QRect(60*col, 60*row, 60, 60))
            font = QtGui.QFont()
            font.setPointSize(28)
            window.field[row][col].setFont(font)
            window.field[row][col].setMaxLength(1)
            window.field[row][col].setAlignment(QtCore.Qt.AlignCenter)
            window.field[row][col].returnPressed.connect(window.validate_answers)
            window.field[row][col].textEdited.connect(lambda text, r=row, c=col: window.validate_field(text, r, c))
    
    for row in range(3,6):
        for col in range(3):
            window.field[row][col].setStyleSheet("background-color: rgb(225, 225, 225);")

    for row in range(3):
        for col in range(3,6):
            window.field[row][col].setStyleSheet("background-color: rgb(225, 225, 225);")

    for row in range(6,9):
        for col in range(3,6):
            window.field[row][col].setStyleSheet("background-color: rgb(225, 225, 225);")

    for row in range(3,6):
        for col in range(6,9):
            window.field[row][col].setStyleSheet("background-color: rgb(225, 225, 225);") 

    for row, column in window.empty_fields:
        window.field[row][column].setStyleSheet(
                window.field[row][column].styleSheet() +
                '\n' + "color: rgb(0, 170, 255);")

def render_footer(window, parent, x, y):
    window.info = QtWidgets.QFrame(parent)
    window.info.setGeometry(QtCore.QRect(x, y, 540, 90))
    window.info.setStyleSheet("background-color: rgb(170, 170, 255);")
    window.info.setFrameShape(QtWidgets.QFrame.StyledPanel)
    window.info.setFrameShadow(QtWidgets.QFrame.Raised)
    window.info.setObjectName("info")

    window.wrong_moves_label = QtWidgets.QLabel(window.info)
    window.wrong_moves_label.setGeometry(QtCore.QRect(10, 30, 145, 28))
    font = QtGui.QFont()
    font.setPointSize(14)
    window.wrong_moves_label.setFont(font)
    window.wrong_moves_label.setObjectName("wrong_moves_label")
    window.wrong_moves_count = QtWidgets.QLabel(window.info)
    window.wrong_moves_count.setGeometry(QtCore.QRect(170, 30, 35, 28))
    font = QtGui.QFont()
    font.setPointSize(14)
    window.wrong_moves_count.setFont(font)
    window.wrong_moves_count.setObjectName("wrong_moves_count")
    window.timer = QtWidgets.QLabel(window.info)
    window.timer.setGeometry(QtCore.QRect(440, 30, 60, 28))
    font = QtGui.QFont()
    font.setPointSize(14)
    window.timer.setFont(font)
    window.timer.setObjectName("timer")

def render_menu(window, parent, x, y):
    window.frame_left_menu = QtWidgets.QFrame(parent)
    window.frame_left_menu.setGeometry(QtCore.QRect(x, y, 50, 650))
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(window.frame_left_menu.sizePolicy().hasHeightForWidth())
    window.frame_left_menu.setSizePolicy(sizePolicy)
    window.frame_left_menu.setMinimumSize(QtCore.QSize(50, 241))
    window.frame_left_menu.setMaximumSize(QtCore.QSize(260, 16777215))
    window.frame_left_menu.setLayoutDirection(QtCore.Qt.LeftToRight)
    window.frame_left_menu.setStyleSheet("background-color: rgb(170, 170, 255);")
    window.frame_left_menu.setFrameShape(QtWidgets.QFrame.NoFrame)
    window.frame_left_menu.setFrameShadow(QtWidgets.QFrame.Raised)
    window.frame_left_menu.setObjectName("frame_left_menu")
    window.verticalLayout_5 = QtWidgets.QVBoxLayout(window.frame_left_menu)
    window.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
    window.verticalLayout_5.setSpacing(1)
    window.verticalLayout_5.setObjectName("verticalLayout_5")
    window.frame_menus = QtWidgets.QFrame(window.frame_left_menu)
    window.frame_menus.setStyleSheet("")
    window.frame_menus.setFrameShape(QtWidgets.QFrame.NoFrame)
    window.frame_menus.setFrameShadow(QtWidgets.QFrame.Raised)
    window.frame_menus.setObjectName("frame_menus")
    window.layout_menus = QtWidgets.QVBoxLayout(window.frame_menus)
    window.layout_menus.setContentsMargins(0, 0, 0, 0)
    window.layout_menus.setSpacing(0)
    window.layout_menus.setObjectName("layout_menus")
    window.btn_toggle_menu = QtWidgets.QPushButton(window.frame_menus)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(window.btn_toggle_menu.sizePolicy().hasHeightForWidth())
    window.btn_toggle_menu.setSizePolicy(sizePolicy)
    window.btn_toggle_menu.setMinimumSize(QtCore.QSize(50, 50))
    window.btn_toggle_menu.setMaximumSize(QtCore.QSize(50, 16777215))
    window.btn_toggle_menu.setStyleSheet("QPushButton {\n"
		"    \n"
		"    background-color: rgb(170, 170, 255);\n"
		"    background-image: url(icons/24x24/cil-menu.png);\n"
		"    background-position: center;\n"
		"    background-repeat: no-reperat;\n"
		"    border: none;\n"
		"}\n"
		"QPushButton:hover {\n"
		"    background-color: rgb(132, 132, 198);\n"
		"}\n"
		"QPushButton:pressed {    \n"
		"    background-color: rgb(132, 132, 198);\n"
		"}")
    window.btn_toggle_menu.setText("")
    window.btn_toggle_menu.setObjectName("btn_toggle_menu")
    window.layout_menus.addWidget(window.btn_toggle_menu)
    window.solve_animation = QtWidgets.QPushButton(window.frame_menus)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(window.solve_animation.sizePolicy().hasHeightForWidth())
    window.solve_animation.setSizePolicy(sizePolicy)
    window.solve_animation.setMinimumSize(QtCore.QSize(0, 60))
    font = QtGui.QFont()
    font.setFamily("Segoe UI")
    window.solve_animation.setFont(font)
    window.solve_animation.setLayoutDirection(QtCore.Qt.LeftToRight)
    window.solve_animation.setStyleSheet("QPushButton {    \n"
		"    background-image: url(icons/24x24/cil-media-play.png);\n"
		"    background-position: left center;\n"
		"    background-repeat: no-repeat;\n"
		"    border: none;\n"
		"    border-left: 18px solid rgb(170, 170, 255);\n"
		"    border-right: 5px solid rgb(170, 170, 255);\n"
		"    background-color: rgb(170, 170, 255);\n"
		"    text-align: left;\n"
		"    padding-left: 45px;\n"
		"}\n"
		"QPushButton:hover {\n"
		"    background-color: rgb(124, 124, 186);\n"
		"    border-left: 18px solid rgb(124, 124, 186);\n"
		"}\n"
		"QPushButton:pressed {    \n"
		"    background-color: rgb(85, 170, 255);\n"
		"    border-left: 18px solid rgb(85, 170, 255);\n"
		"}")
    window.solve_animation.setObjectName("solve_animation")
    window.layout_menus.addWidget(window.solve_animation)
    window.auto_solve = QtWidgets.QPushButton(window.frame_menus)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(window.auto_solve.sizePolicy().hasHeightForWidth())
    window.auto_solve.setSizePolicy(sizePolicy)
    window.auto_solve.setMinimumSize(QtCore.QSize(0, 60))
    font = QtGui.QFont()
    font.setFamily("Segoe UI")
    window.auto_solve.setFont(font)
    window.auto_solve.setLayoutDirection(QtCore.Qt.LeftToRight)
    window.auto_solve.setStyleSheet("QPushButton {    \n"
		"    background-image: url(icons/24x24/cil-check.png);\n"
		"    background-position: left center;\n"
		"    background-repeat: no-repeat;\n"
		"    border: none;\n"
		"    border-left: 18px solid rgb(170, 170, 255);\n"
		"    border-right: 5px solid rgb(170, 170, 255);\n"
		"    background-color: rgb(170, 170, 255);\n"
		"    text-align: left;\n"
		"    padding-left: 45px;\n"
		"}\n"
		"QPushButton:hover {\n"
		"    background-color: rgb(124, 124, 186);\n"
		"    border-left: 18px solid rgb(124, 124, 186);\n"
		"}\n"
		"QPushButton:pressed {    \n"
		"    background-color: rgb(85, 170, 255);\n"
		"    border-left: 18px solid rgb(85, 170, 255);\n"
		"}")
    window.auto_solve.setObjectName("auto_solve")
    window.layout_menus.addWidget(window.auto_solve)
    window.pause_run_timer = QtWidgets.QPushButton(window.frame_menus)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(window.pause_run_timer.sizePolicy().hasHeightForWidth())
    window.pause_run_timer.setSizePolicy(sizePolicy)
    window.pause_run_timer.setMinimumSize(QtCore.QSize(0, 60))
    font = QtGui.QFont()
    font.setFamily("Segoe UI")
    window.pause_run_timer.setFont(font)
    window.pause_run_timer.setLayoutDirection(QtCore.Qt.LeftToRight)
    window.pause_run_timer.setStyleSheet("QPushButton {    \n"
		"    background-image: url(icons/24x24/cil-watch);\n"
		"    background-position: left center;\n"
		"    background-repeat: no-repeat;\n"
		"    border: none;\n"
		"    border-left: 18px solid rgb(170, 170, 255);\n"
		"    border-right: 5px solid rgb(170, 170, 255);\n"
		"    background-color: rgb(170, 170, 255);\n"
		"    text-align: left;\n"
		"    padding-left: 45px;\n"
		"}\n"
		"QPushButton:hover {\n"
		"    background-color: rgb(124, 124, 186);\n"
		"    border-left: 18px solid rgb(124, 124, 186);\n"
		"}\n"
		"QPushButton:pressed {    \n"
		"    background-color: rgb(85, 170, 255);\n"
		"    border-left: 18px solid rgb(85, 170, 255);\n"
		"}")
    window.pause_run_timer.setObjectName("pause_run_timer")
    window.layout_menus.addWidget(window.pause_run_timer)
    window.speed_control_header = QtWidgets.QFrame(window.frame_menus)
    window.speed_control_header.setMinimumSize(QtCore.QSize(0, 60))
    window.speed_control_header.setStyleSheet("QFrame{\n"
		"background-image: url(icons/24x24/cil-speedometer.png);\n"
		"background-position: left center;\n"
		"background-repeat: no-repeat;\n"
		"border: none;\n"
		"border-left: 18px solid rgb(170, 170, 255);\n"
		"border-top: 1px solid black;\n"
		"background-color: rgb(170, 170, 255);\n"
		"text-align: left;\n"
		"}")
    window.speed_control_header.setFrameShape(QtWidgets.QFrame.StyledPanel)
    window.speed_control_header.setFrameShadow(QtWidgets.QFrame.Raised)
    window.speed_control_header.setObjectName("speed_control_header")
    window.speed_label = QtWidgets.QLabel(window.speed_control_header)
    window.speed_label.setGeometry(QtCore.QRect(60, 20, 111, 20))
    window.speed_label.setStyleSheet("border: none;\n"
			"background: none;\n"
			"margin: 0;")
    window.speed_label.setObjectName("speed_label")
    window.layout_menus.addWidget(window.speed_control_header)
    window.speed_control_frame = QtWidgets.QFrame(window.frame_menus)
    window.speed_control_frame.setMinimumSize(QtCore.QSize(0, 25))
    window.speed_control_frame.setStyleSheet("QFrame{\n"
		"border: none;\n"
		"background-color: rgb(170, 170, 255);\n"
		"text-align: left;\n"
		"}")
    window.speed_control_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    window.speed_control_frame.setFrameShadow(QtWidgets.QFrame.Raised)
    window.speed_control_frame.setObjectName("speed_control_frame")
    window.speed_slider = QtWidgets.QSlider(window.speed_control_frame)
    window.speed_slider.setGeometry(QtCore.QRect(50, 0, 160, 22))
    window.speed_slider.setStyleSheet("QSlider::groove:horizontal {\n"
        "border: 1px solid #bbb;\n"
        "background: white;\n"
        "height: 10px;\n"
        "border-radius: 4px;\n"
        "}\n"
        "\n"
        "QSlider::sub-page:horizontal {\n"
        "background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
        "    stop: 0 #66e, stop: 1 #bbf);\n"
        "background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
        "    stop: 0 #bbf, stop: 1 #55f);\n"
        "border: 1px solid #777;\n"
        "height: 10px;\n"
        "border-radius: 4px;\n"
        "}\n"
        "\n"
        "QSlider::add-page:horizontal {\n"
        "background: #fff;\n"
        "border: 1px solid #777;\n"
        "height: 10px;\n"
        "border-radius: 4px;\n"
        "}\n"
        "\n"
        "QSlider::handle:horizontal {\n"
        "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
        "    stop:0 #eee, stop:1 #ccc);\n"
        "border: 1px solid #777;\n"
        "width: 13px;\n"
        "margin-top: -2px;\n"
        "margin-bottom: -2px;\n"
        "border-radius: 4px;\n"
        "}\n"
        "\n"
        "QSlider::handle:horizontal:hover {\n"
        "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
        "    stop:0 #fff, stop:1 #ddd);\n"
        "border: 1px solid #444;\n"
        "border-radius: 4px;\n"
        "}\n"
        "\n"
        "QSlider::sub-page:horizontal:disabled {\n"
        "background: #bbb;\n"
        "border-color: #999;\n"
        "}\n"
        "\n"
        "QSlider::add-page:horizontal:disabled {\n"
        "background: #eee;\n"
        "border-color: #999;\n"
        "}\n"
        "\n"
        "QSlider::handle:horizontal:disabled {\n"
        "background: #eee;\n"
        "border: 1px solid #aaa;\n"
        "border-radius: 4px;\n"
        "}")
    window.speed_slider.setMaximum(100)
    window.speed_slider.setOrientation(QtCore.Qt.Horizontal)
    window.speed_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
    window.speed_slider.setTickInterval(10)
    window.speed_slider.setObjectName("speed_slider")
    window.speed_value = QtWidgets.QLabel(window.speed_control_frame)
    window.speed_value.setGeometry(QtCore.QRect(215, 2, 21, 16))
    window.speed_value.setObjectName("speed_value")
    window.layout_menus.addWidget(window.speed_control_frame)
    window.verticalLayout_5.addWidget(window.frame_menus, 0, QtCore.Qt.AlignTop)