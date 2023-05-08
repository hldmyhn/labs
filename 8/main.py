import sys
import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QTableWidget, QTableWidgetItem, QTabWidget,
                             QPushButton, QHBoxLayout, QDialog,
                             QLabel, QLineEdit, QVBoxLayout,
                             QDialogButtonBox, QSizePolicy, QAbstractScrollArea,
                             QHeaderView, QMessageBox, QFormLayout, QComboBox,
                             QInputDialog, QTimeEdit)

from PyQt5.QtCore import Qt, QTime

from PyQt5.QtGui import QIcon, QPixmap
from style import stylesheet


class MyMainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class InputDialog(QDialog):
    def __init__(self, title, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.fields = fields
        self.line_edits = {}

        layout = QFormLayout()

        for field in fields:
            line_edit = QLineEdit()
            self.line_edits[field] = line_edit
            layout.addRow(field, line_edit)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_values(self):
        values = {}
        for field, line_edit in self.line_edits.items():
            current_text = line_edit.text()
            if current_text:
                values[field] = current_text
        return values


class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расписание")
        self.setGeometry(100, 100, 800, 400)
        self.connection = psycopg2.connect(database="new_v1",
                                           user="postgres",
                                           password="12345",
                                           host="localhost")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        self.subjects_widget = QWidget()
        self.teachers_widget = QWidget()
        self.schedule_widget = QWidget()

        tab_widget.addTab(self.subjects_widget, "Предметы")
        tab_widget.addTab(self.teachers_widget, "Преподаватели")
        tab_widget.addTab(self.schedule_widget, "Расписание")

        self.subjects_table = QTableWidget()
        self.subjects_table.setColumnCount(3)
        self.subjects_table.setHorizontalHeaderLabels(["ID", "Название", "Тип"])

        self.subjects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.subjects_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.subjects_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.subjects_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.teachers_table = QTableWidget()
        self.teachers_table.setColumnCount(2)
        self.teachers_table.setHorizontalHeaderLabels(["ID", "Имя"])

        self.teachers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.teachers_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.teachers_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.teachers_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.schedule_day_tabs = QTabWidget()
        self.monday_table = QTableWidget()
        self.tuesday_table = QTableWidget()
        self.wednesday_table = QTableWidget()
        self.thursday_table = QTableWidget()
        self.friday_table = QTableWidget()
        self.saturday_table = QTableWidget()

        day_tables = [self.monday_table, self.tuesday_table, self.wednesday_table,
                      self.thursday_table, self.friday_table, self.saturday_table]

        for table in day_tables:
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(
                ['ID', 'Предмет', 'Преподаватель', 'Начало пары', 'Конец пары', 'Аудитория', 'Тип недели'])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.schedule_day_tabs.addTab(self.monday_table, 'Понедельник')
        self.schedule_day_tabs.addTab(self.tuesday_table, 'Вторник')
        self.schedule_day_tabs.addTab(self.wednesday_table, 'Среда')
        self.schedule_day_tabs.addTab(self.thursday_table, 'Четверг')
        self.schedule_day_tabs.addTab(self.friday_table, 'Пятница')
        self.schedule_day_tabs.addTab(self.saturday_table, 'Суббота')

        self.subjects_layout = QVBoxLayout()
        self.subjects_layout.addWidget(self.subjects_table)

        self.teachers_layout = QVBoxLayout()
        self.teachers_layout.addWidget(self.teachers_table)

        self.schedule_layout = QVBoxLayout()
        self.schedule_layout.addWidget(self.schedule_day_tabs)

        self.subjects_widget.setLayout(self.subjects_layout)
        self.teachers_widget.setLayout(self.teachers_layout)
        self.schedule_widget.setLayout(self.schedule_layout)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_subjects)

        self.update_btn = QPushButton("Обновить")
        self.update_btn.clicked.connect(self.update_subjects)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_subjects)

        self.edit_btn = QPushButton("Изменить")
        self.edit_btn.clicked.connect(self.edit_subjects)

        subjects_btn_layout = QHBoxLayout()
        subjects_btn_layout.addWidget(self.add_btn)
        subjects_btn_layout.addWidget(self.update_btn)
        subjects_btn_layout.addWidget(self.delete_btn)
        subjects_btn_layout.addWidget(self.edit_btn)

        self.subjects_layout.addLayout(subjects_btn_layout)

        self.add_teachers_btn = QPushButton("Добавить")
        self.add_teachers_btn.clicked.connect(self.add_teachers)

        self.update_teachers_btn = QPushButton("Обновить")
        self.update_teachers_btn.clicked.connect(self.update_teachers)

        self.delete_teachers_btn = QPushButton("Удалить")
        self.delete_teachers_btn.clicked.connect(self.delete_teachers)

        self.edit_teachers_btn = QPushButton("Изменить")
        self.edit_teachers_btn.clicked.connect(self.edit_teachers)

        teachers_btn_layout = QHBoxLayout()
        teachers_btn_layout.addWidget(self.add_teachers_btn)
        teachers_btn_layout.addWidget(self.update_teachers_btn)
        teachers_btn_layout.addWidget(self.delete_teachers_btn)
        teachers_btn_layout.addWidget(self.edit_teachers_btn)

        self.teachers_layout.addLayout(teachers_btn_layout)

        self.add_schedule_btn = QPushButton("Добавить")
        self.add_schedule_btn.clicked.connect(self.add_schedule_item)

        self.update_schedule_btn = QPushButton("Обновить")
        self.update_schedule_btn.clicked.connect(self.update_schedule)

        self.delete_schedule_btn = QPushButton("Удалить")
        self.delete_schedule_btn.clicked.connect(self.delete_schedule)

        self.edit_schedule_btn = QPushButton("Изменить")
        self.edit_schedule_btn.clicked.connect(self.edit_schedule)

        schedule_btn_layout = QHBoxLayout()
        schedule_btn_layout.addWidget(self.add_schedule_btn)
        schedule_btn_layout.addWidget(self.update_schedule_btn)
        schedule_btn_layout.addWidget(self.delete_schedule_btn)
        schedule_btn_layout.addWidget(self.edit_schedule_btn)

        self.schedule_layout.addLayout(schedule_btn_layout)

        self.setLayout(layout)

        self.update_subjects()
        self.update_teachers()
        self.update_schedule()

    def execute_query(self, query, values=None):
        cursor = self.connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        self.connection.commit()

    # Предметы

    def update_subjects(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, type FROM subject ORDER BY id;")
        subjects = cursor.fetchall()
        self.subjects_table.setRowCount(len(subjects))

        for i, subject in enumerate(subjects):
            for j, value in enumerate(subject):
                item = QTableWidgetItem(str(value))
                self.subjects_table.setItem(i, j, item)

    def add_subjects(self):
        dialog = InputDialog("Добавить предмет", ["Название", "Тип"], self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            values = dialog.get_values()
            self.safe_execute_query("INSERT INTO subject (name, type) VALUES (%s, %s);",
                                    (values["Название"], values["Тип"]))
            self.update_subjects()

    def delete_subjects(self):
        selected_rows = self.subjects_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        subject_id = self.subjects_table.item(row, 0).text()

        self.safe_execute_query("DELETE FROM subject WHERE id = %s;", (subject_id,))
        self.update_subjects()

    def edit_subjects(self):
        selected_rows = self.subjects_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        subject_id = self.subjects_table.item(row, 0).text()

        dialog = InputDialog("Изменить предмет", ["Название", "Тип"], self)

        dialog.line_edits["Название"].setText(self.subjects_table.item(row, 1).text())
        dialog.line_edits["Тип"].setText(self.subjects_table.item(row, 2).text())

        result = dialog.exec_()

        if result == QDialog.Accepted:
            values = dialog.get_values()
            self.safe_execute_query("UPDATE subject SET name = %s, type = %s WHERE id = %s;",
                                    (values["Название"], values["Тип"], subject_id))
            self.update_subjects()

    # Предметы

    # Преподаватели

    def update_teachers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM teacher ORDER BY id;")
        teachers = cursor.fetchall()
        self.teachers_table.setRowCount(len(teachers))

        for i, teacher in enumerate(teachers):
            for j, value in enumerate(teacher):
                item = QTableWidgetItem(str(value))
                self.teachers_table.setItem(i, j, item)

    def add_teachers(self):
        dialog = InputDialog("Добавить преподавателя", ["Имя"], self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            values = dialog.get_values()
            self.safe_execute_query("INSERT INTO teacher (name) VALUES (%s);", (values["Имя"],))
            self.update_teachers()

    def delete_teachers(self):
        selected_rows = self.teachers_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        teacher_id = self.teachers_table.item(row, 0).text()

        self.safe_execute_query("DELETE FROM teacher WHERE id = %s;", (teacher_id,))
        self.update_teachers()

    def edit_teachers(self):
        selected_rows = self.teachers_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        teacher_id = self.teachers_table.item(row, 0).text()

        dialog = InputDialog("Изменить преподавателя", ["Имя"], self)
        dialog.line_edits["Имя"].setText(self.teachers_table.item(row, 1).text())
        result = dialog.exec_()

        if result == QDialog.Accepted:
            values = dialog.get_values()
            self.safe_execute_query("UPDATE teacher SET name = %s WHERE id = %s;",
                                    (values["Имя"], teacher_id))
            self.update_teachers()

    # Преподаватели

    def safe_execute_query(self, query, data):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, data)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Ошибка выполнения запроса:", e)
            QMessageBox.critical(self, "Ошибка",
                                 "Не удалось выполнить запрос. Проверьте правильность ввода данных.")
            return False
        return True

    # Расписание

    def add_schedule_item(self):
        try:
            dialog = InputDialog("Добавить расписание",
                                 ["ID предмета", "ID преподавателя", "ID аудитории", "Тип недели"], self)

            start_time_edit = QTimeEdit()
            end_time_edit = QTimeEdit()
            start_time_edit.setDisplayFormat("HH:mm")
            end_time_edit.setDisplayFormat("HH:mm")
            start_time_edit.setTime(QTime(0, 0))
            end_time_edit.setTime(QTime(0, 0))
            dialog.layout().addRow("Начало пары", start_time_edit)
            dialog.layout().addRow("Конец пары", end_time_edit)

            result = dialog.exec_()

            if result == QDialog.Accepted:
                values = dialog.get_values()
                day_of_week = self.schedule_day_tabs.tabText(self.schedule_day_tabs.currentIndex())

                start_time = start_time_edit.time()
                end_time = end_time_edit.time()

                teacher_id = int(values["ID преподавателя"])
                self.safe_execute_query(
                    "INSERT INTO schedule (item_id, teacher_id, day_of_week, start_time, end_time, room_id, week_type) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                    (int(values["ID предмета"]), teacher_id, day_of_week,
                     start_time.toString("HH:mm"),
                     end_time.toString("HH:mm"), int(values["ID аудитории"]), values['Тип недели']))

                self.update_schedule()
        except Exception as e:
            print("Ошибка выполнения запроса:", e)
            QMessageBox.critical(self, "Ошибка",
                                 "Не удалось добавить расписание. Проверьте правильность ввода данных.")

    def delete_schedule(self):
        current_day_table = self.schedule_day_tabs.currentWidget()
        selected_rows = current_day_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row() if selected_rows else -1
        if row == -1:
            return

        schedule_id = current_day_table.item(row, 0).text()

        self.safe_execute_query(
            "DELETE FROM schedule WHERE id = %s;",
            (schedule_id,))
        self.update_schedule()

    def edit_schedule(self):
        current_day_table = self.schedule_day_tabs.currentWidget()
        selected_items = current_day_table.selectedItems()
        if not selected_items:
            return

        row = selected_items[0].row()
        schedule_id = current_day_table.item(row, 0).text()

        dialog = InputDialog("Изменить расписание",
                             ["ID предмета", "ID преподавателя", "ID аудитории", "Тип недели"], self)

        start_time_edit = QTimeEdit()
        end_time_edit = QTimeEdit()
        start_time_edit.setDisplayFormat("HH:mm")
        end_time_edit.setDisplayFormat("HH:mm")

        start_time_edit.setTime(QTime.fromString(current_day_table.item(row, 3).text(), "HH:mm"))
        end_time_edit.setTime(QTime.fromString(current_day_table.item(row, 4).text(), "HH:mm"))

        dialog.layout().addRow("Начало пары", start_time_edit)
        dialog.layout().addRow("Конец пары", end_time_edit)

        dialog.line_edits["ID предмета"].setText(current_day_table.item(row, 1).text())
        dialog.line_edits["ID преподавателя"].setText(current_day_table.item(row, 2).text())
        dialog.line_edits["ID аудитории"].setText(current_day_table.item(row, 5).text())
        dialog.line_edits["Тип недели"].setText(current_day_table.item(row, 6).text())

        result = dialog.exec_()

        if result == QDialog.Accepted:
            values = dialog.get_values()
            day_of_week = self.schedule_day_tabs.tabText(self.schedule_day_tabs.currentIndex())

            start_time = start_time_edit.time()
            end_time = end_time_edit.time()

            teacher_id = int(values["ID преподавателя"])
            week_type = values['Тип недели']
            if self.safe_execute_query(
                    "UPDATE schedule SET item_id = %s, teacher_id = %s, day_of_week = %s, start_time = %s, end_time = %s, room_id = %s, week_type = %s WHERE id = %s;",
                    (int(values["ID предмета"]), teacher_id, day_of_week,
                     start_time.toString("HH:mm"),
                     end_time.toString("HH:mm"), int(values["ID аудитории"]), week_type, schedule_id)):
                self.update_schedule()

    def update_schedule(self):
        for table, day_of_week in zip([self.monday_table, self.tuesday_table, self.wednesday_table, self.thursday_table,
                                       self.friday_table, self.saturday_table],
                                      ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]):
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT schedule.id, subject.name, teacher.name, schedule.start_time, schedule.end_time, schedule.room_id, schedule.week_type FROM schedule LEFT JOIN subject ON schedule.item_id = subject.id LEFT JOIN teacher ON schedule.teacher_id = teacher.id WHERE schedule.day_of_week = %s ORDER BY schedule.start_time;",
                (day_of_week,))

            schedule_items = cursor.fetchall()
            table.setRowCount(0)

            for i, schedule_item in enumerate(schedule_items):
                table.insertRow(table.rowCount())
                for col, value in enumerate(schedule_item):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    table.setItem(i, col, item)

    # Расписание

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())