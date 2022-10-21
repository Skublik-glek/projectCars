import sys

from main import Car, Tools, cars_dict

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis/main.ui', self)
        self.createColorDialog = QColorDialog(self)
        self.color = QColor("#ffffff")
        self.edit_color = QColor("#ffffff")
        self.createColor.clicked.connect(self.create_color)
        self.create_b.clicked.connect(self.create_car)
        self.findCar.clicked.connect(self.get_car_info)
        self.editNameB.clicked.connect(self.edit_name)
        self.moveRight.clicked.connect(self.move_door)
        self.moveLeft.clicked.connect(self.move_door)
        self.turnRight.clicked.connect(self.turner)
        self.turnLeft.clicked.connect(self.turner)

        self.vEngineEditB.clicked.connect(self.changer)
        self.carTypeEditB.clicked.connect(self.changer)
        self.privodEditB.clicked.connect(self.changer)
        self.boxTypeEditB.clicked.connect(self.changer)
        self.creatorEditB.clicked.connect(self.changer)
        self.colorEdit.clicked.connect(self.changer)
        self.deleteB.clicked.connect(self.delete)

        self.update_car_list()
        self.carsList.clicked.connect(self.paster)
        self.old_name = ""

    def create_car(self):
        if self.carName.text() != "":
            if Tools.check_name(self.carName.text()):
                new_car = Car(self.carName.text(), self.carType.currentText(), self.creator.text(),
                            str(self.color.name()), self.privod.currentText(), self.boxType.currentText(), self.vEngine.value())
                self.update_car_list()
            else:
                self.carName.setText("Такая машина уже есть!!!")

    def create_color(self, edit=False):
        if not edit:
            self.createColorDialog.exec_()
            self.color = self.createColorDialog.selectedColor()
        else:
            if self.old_name != "":
                self.createColorDialog.exec_()
                self.edit_color = self.createColorDialog.selectedColor()

    def update_car_list(self):
        self.carsList.clear()
        if Tools.get_cars_list() != []:
            for elem in Tools.get_cars_list():
                self.carsList.addItem(elem)
    
    def paster(self):
        self.carsInput.setText(self.sender().currentItem().text())
    
    def get_car_info(self, name=False):
        if not name:
            if not Tools.check_name(self.carsInput.text()):
                if self.carsInput.text() not in cars_dict.keys():
                    car = Car()
                    car.restore(self.carsInput.text())
                else:
                    car = cars_dict[self.carsInput.text()]
                self.infoBrowser.setFont(QFont('Arial', 18))
                self.infoBrowser.setText(car.get_info()[0])
                self.colorBrowser.setHtml(car.get_info()[1])
                self.old_name = self.carsInput.text()
            else:
                self.carsInput.setText("Неверная машина")
        else:
            car = cars_dict[name]
            self.infoBrowser.setFont(QFont('Arial', 18))
            self.infoBrowser.setText(car.get_info()[0])
            self.colorBrowser.setHtml(car.get_info()[1])
            self.old_name = self.carsInput.text()

    def edit_name(self):
        if self.old_name != "" and self.editName.text() != "":
            if Tools.check_name(self.editName.text()):
                if self.old_name in cars_dict.keys():
                    car = cars_dict[self.old_name]
                else:
                    car = Car()
                    car.restore(self.old_name)
                new_car = Car(self.editName.text(), car.type, car.creator,
                              car.color, car.privod, car.box_type, car.v_engine)
                new_car.rotators_status = car.rotators_status
                new_car.door_status = car.door_status
                cars_dict[self.editName.text()] = new_car
                self.update_car_list()
                car.delete_data()
                car = None
                self.update_car_list()
                self.get_car_info(self.editName.text())
                self.old_name = self.editName.text()
                self.carsInput.setText(self.editName.text())
            else:
                self.editName.setText("Такая машина уже есть")

    def move_door(self):
        if self.old_name != "":
            if self.sender().text() == "Открыть/закрыть правую":
                index = 1
            else:
                index = 0
            car = Tools.get_correct_car_object(self.old_name)
            car.open_door(index)
            self.get_car_info(self.old_name)

    def turner(self):
        if self.old_name != "":
            if self.sender().text() == "Включить/выключить правый":
                index = 1
            else:
                index = 0
            car = Tools.get_correct_car_object(self.old_name)
            car.activate_rotator(index)
            self.get_car_info(self.old_name)

    def changer(self):
        if self.old_name != "":
            if self.sender().text() == "Изменить литраж":
                car: Car = Tools.get_correct_car_object(self.old_name)
                car.v_engine = self.vEngineEdit.value()
            elif self.sender().text() == "Изменить тип":
                car: Car = Tools.get_correct_car_object(self.old_name)
                car.privod = self.carTypeEdit.currentText()
            elif self.sender().text() == "Изменить привод":
                car: Car = Tools.get_correct_car_object(self.old_name)
                car.privod = self.privodEdit.currentText()
            elif self.sender().text() == "Изменить коробку":
                car: Car = Tools.get_correct_car_object(self.old_name)
                car.box_type = self.boxTypeEdit.currentText()
            elif self.sender().text() == "Изменить производителя":
                car: Car = Tools.get_correct_car_object(self.old_name)
                car.creator = self.creatorEdit.text()
            elif self.sender().text() == "Изменить цвет":
                car: Car = Tools.get_correct_car_object(self.old_name)
                self.create_color(edit=True)
                car.color = self.edit_color.name()
            car.save()
            self.get_car_info(self.old_name)

    def delete(self):
        if self.old_name != "":
            car = Tools.get_correct_car_object(self.old_name)
            car.delete_data()
            car = None
            self.update_car_list()
            self.infoBrowser.clear()
            self.colorBrowser.clear()
            self.old_name = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon('files/logo.png'))
    # app.setStyleSheet(styleSheet)
    ex = Main()
    # ex.setWindowIcon(QtGui.QIcon('files/logo.png'))
    ex.show()
    sys.exit(app.exec())
