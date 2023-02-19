from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime

from database.bd import selectMax


a = QApplication([])

high = QBarSet("Maxima")
umidade = selectMax('umidade')
temperatura = selectMax('temperatura')
indice = selectMax('indice')


if umidade[0]:
    high << float(umidade[0]) << float(temperatura[0]) << float(indice[0])
else:
    high << 0 << 0 << 0
    

series = QStackedBarSeries()
series.append(high)

chart = QChart()
chart.addSeries(series)
chart.setTitle("Registros de temperatura em celcius")
chart.setAnimationOptions(QChart.SeriesAnimations)

categories = ["Umidade", "Temperatura","Indice de Calor"]

axis = QBarCategoryAxis()
axis.append(categories)
axis.setTitleText("unidades")
chart.createDefaultAxes()
chart.setAxisX(axis, series)
chart.axisY(series).setRange(0, 70)
chart.axisY(series).setTitleText("Temperature ºC - umi %")

chart.legend().setVisible(True)
chart.legend().setAlignment(Qt.AlignBottom)

chartView = QChartView(chart)
chartView.setRenderHint(QPainter.Antialiasing)

window = QMainWindow()
window.setCentralWidget(chartView)
window.resize(900, 600)

