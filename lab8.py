import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(lambda _: self._update())
        self.updatebtn_lay = QHBoxLayout()
        self.vbox.addLayout(self.updatebtn_lay)
        self.updatebtn_lay.addWidget(self.update_button)

        self._create_shedule_tab()
        self._create_teachers_tab()
        self._create_subjects_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="shedule",
                                     user="postgres",
                                     password="0000",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Расписание")
        days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА']

        day_tab = QTabWidget(self)

        for i in days:
            day_tab.addTab(self._create_day_table(i), i)
        day_tab_layout = QVBoxLayout()
        day_tab_layout.addWidget(day_tab)
        self.shedule_tab.setLayout(day_tab_layout)

    def _create_day_table(self, day):
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["id_timetable", "day", "subject", "room_numb", "start_time", "week", "", ""])
        self._update_day_table(table, day)
        return table

    def _update_day_table(self, table, day):
        self.cursor.execute(f"SELECT * FROM timetable JOIN subject ON timetable.subject = subject.id_subject WHERE day='{day}' ORDER BY id_timetable")
        records = list(self.cursor.fetchall())
        table.setRowCount(len(records) + 1)

        for i, j in enumerate(records):
            j = list(j)
            editButton = QPushButton("EDIT")
            delButton = QPushButton("DELETE")
            table.setItem(i, 0, QTableWidgetItem(str(j[0])))
            table.setItem(i, 1, QTableWidgetItem(str(j[1])))
            table.setItem(i, 2, QTableWidgetItem(str(j[7])))
            table.setItem(i, 3, QTableWidgetItem(str(j[3])))
            table.setItem(i, 4, QTableWidgetItem(str(j[4])))
            table.setItem(i, 5, QTableWidgetItem(str(j[5])))
            table.setCellWidget(i, 6, editButton)
            table.setCellWidget(i, 7, delButton)

            editButton.clicked.connect(lambda _, rowNum=i, table=table: self._change_from_timetable(rowNum, table))
            delButton.clicked.connect(lambda _, rowNum=i, table=table: self._delete_from_timetable(rowNum, table))

        addButton = QPushButton("ADD")
        addButton.clicked.connect(lambda _, rowNum=len(records), table=table: self._add_row_timetable(rowNum, table))
        table.setCellWidget(len(records), 6, addButton)
        table.resizeRowsToContents()

    def _change_from_timetable(self, rowNum, table):
        row = list()
        for i in range(table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("SELECT id_subject FROM subject WHERE name=%s", (row[2],))
            subject = self.cursor.fetchone()
            row[2] = subject[0]
            row.append(row[0])
            row = row[1:]
            self.cursor.execute("UPDATE timetable SET day=%s, subject=%s, room_numb=%s, start_time=%s, week=%s WHERE id_timetable=%s", tuple(row))
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _delete_from_timetable(self, rowNum, table):
        try:
            id = table.item(rowNum, 0).text()
            day = table.item(rowNum, 1).text()
            self.cursor.execute("DELETE FROM timetable WHERE id_timetable=%s", (id,))
            self.conn.commit()
            table.setRowCount(0)
            self._update_day_table(table, day)
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _add_row_timetable(self, rowNum, table):
        row = list()
        for i in range(1, table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("SELECT id_subject FROM subject WHERE name=%s", (row[1],))
            subject = self.cursor.fetchone()
            row[1] = subject[0]
            self.cursor.execute("SELECT MAX(id_timetable)+1 FROM timetable")
            new_id_timetable = self.cursor.fetchone()
            row.append(new_id_timetable)
            self.cursor.execute("INSERT INTO timetable (day, subject, room_numb, start_time, week, id_timetable) VALUES(%s, %s, %s, %s, %s, %s)",(tuple(row)))
            self.conn.commit()
            table.setRowCount(0)
            self._update_day_table(table, row[0])
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _create_teachers_tab(self):
        self.teachers = QWidget()
        self.tabs.addTab(self.teachers, "Преподаватели")
        table = QTableWidget(self)
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["id_teacher", "Имя", "Предмет", "", ""])

        teachers_tab_layout = QVBoxLayout()
        teachers_tab_layout.addWidget(table)

        self._update_teachers_tab(table)
        self.teachers.setLayout(teachers_tab_layout)

    def _update_teachers_tab(self, table):
        self.cursor.execute("SELECT * FROM teacher JOIN subject ON teacher.subject=subject.id_subject ORDER BY id_teacher")
        records = list(self.cursor.fetchall())
        table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            editButton = QPushButton("EDIT")
            delButton = QPushButton("DELETE")
            table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            table.setItem(i, 2, QTableWidgetItem(str(r[4])))
            table.setCellWidget(i, 3, editButton)
            table.setCellWidget(i, 4, delButton)

            editButton.clicked.connect(lambda _, rowNum=i, tabl=table: self._change_from_teacher(rowNum, table))
            delButton.clicked.connect(lambda _, rowNum=i, tabl=table: self._delete_from_teacher(rowNum, table))
        addButton = QPushButton("ADD")
        addButton.clicked.connect(lambda _, rowNum=len(records), table=table: self._add_row_teacher(rowNum, table))
        table.setCellWidget(len(records), 3, addButton)
        table.resizeRowsToContents()

    def _change_from_teacher(self, rowNum, table):
        row = list()

        for i in range(table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("SELECT id_subject FROM subject WHERE name=%s", (row[2],))
            subject = self.cursor.fetchone()
            row[2] = subject[0]
            row.append(row[0])
            row = row[1:]
            self.cursor.execute("UPDATE teacher SET full_name=%s, subject=%s WHERE id_teacher=%s", tuple(row))
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _delete_from_teacher(self, rowNum, table):
        try:
            id = table.item(rowNum, 0).text()
            self.cursor.execute("DELETE FROM teacher WHERE id_teacher=%s", (id,))
            self.conn.commit()
            table.setRowCount(0)
            self._update_teachers_tab(table)
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _add_row_teacher(self, rowNum, table):
        row = list()
        for i in range(1, table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        self.cursor.execute("SELECT id_subject FROM subject WHERE name=%s", (row[1],))
        subject = self.cursor.fetchone()
        row[1] = subject[0]
        self.cursor.execute("SELECT MAX(id_teacher)+1 FROM teacher")
        new_id_teacher = self.cursor.fetchone()
        row.append(new_id_teacher)
        try:
            self.cursor.execute("INSERT INTO teacher (full_name, subject, id_teacher) VALUES(%s, %s, %s)", (tuple(row)))
            self.conn.commit()
            table.setRowCount(0)
            self._update_teachers_tab(table)
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _create_subjects_tab(self):
        self.subjects = QWidget()
        self.tabs.addTab(self.subjects, "Предметы")
        table = QTableWidget(self)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["id_subject", "Предмет", "", ""])

        subjects_tab_layout = QVBoxLayout()
        subjects_tab_layout.addWidget(table)

        self._update_subjects_tab(table)
        self.subjects.setLayout(subjects_tab_layout)

    def _update_subjects_tab(self, table):
        self.cursor.execute("SELECT * FROM subject ORDER BY id_subject")
        records = list(self.cursor.fetchall())
        table.setRowCount(len(records) + 1)
        for i, j in enumerate(records):
            j = list(j)
            editButton = QPushButton("EDIT")
            delButton = QPushButton("DELETE")
            table.setItem(i, 0, QTableWidgetItem(str(j[0])))
            table.setItem(i, 1, QTableWidgetItem(str(j[1])))
            table.setCellWidget(i, 2, editButton)
            table.setCellWidget(i, 3, delButton)

            editButton.clicked.connect(lambda _, rowNum=i, table=table: self._change_from_subjects(rowNum, table))
            delButton.clicked.connect(lambda _, rowNum=i, table=table: self._delete_from_subjects(rowNum, table))

        addButton = QPushButton("ADD")
        addButton.clicked.connect(lambda _, rowNum=len(records), table=table: self._add_row_subject(rowNum, table))
        table.setCellWidget(len(records), 2, addButton)
        table.resizeRowsToContents()

    def _change_from_subjects(self, rowNum, table):
        row = list()

        for i in range(table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            row.append(row[0])
            row = row[1:]
            self.cursor.execute("UPDATE subject SET name=%s WHERE id_subject=%s", tuple(row))
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _delete_from_subjects(self, rowNum, table):
        try:
            id = table.item(rowNum, 0).text()
            self.cursor.execute("DELETE FROM teacher WHERE subject=%s", (id,))
            self.cursor.execute("DELETE FROM timetable WHERE subject=%s", (id,))
            self.cursor.execute("DELETE FROM subject WHERE id_subject=%s", (id,))
            self.conn.commit()
            table.setRowCount(0)
            self._update_subjects_tab(table)
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _add_row_subject(self, rowNum, table):
        subject = table.item(rowNum, 1).text()
        self.cursor.execute("SELECT MAX(id_subject)+1 FROM subject")
        id_subject = self.cursor.fetchone()
        try:
            self.cursor.execute("INSERT INTO subject (id_subject, name) VALUES(%s, %s)", (id_subject, subject))
            self.conn.commit()
            table.setRowCount(0)
            self._update_subjects_tab(table)
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _update(self):
        self.tabs.removeTab(0)
        self.tabs.removeTab(0)
        self.tabs.removeTab(0)
        self._create_shedule_tab()
        self._create_teachers_tab()
        self._create_subjects_tab()


app = QApplication(sys.argv)
win = MainWindow()
win.showMaximized()
sys.exit(app.exec_())
