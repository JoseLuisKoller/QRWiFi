import os
import sys
import wifi_qrcode_generator
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QStatusBar, QVBoxLayout, QHBoxLayout, QCheckBox, QMessageBox
from PyQt5.QtGui import QFont, QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt

class QRCodeApplication(QWidget):
	
	def __init__(self):
		super().__init__()
		self.setFixedSize(700, 550)
		self.setWindowTitle('Generador QR WiFi - @Kolleermaann')
		self.initUI()

	def initUI(self):

		#Configs y Fuentes
		self.setWindowIcon(QIcon('yo.png'))
		mainLayout = QVBoxLayout()
		entryLayout_Name = QHBoxLayout()
		entryLayout_Pass = QHBoxLayout()
		buttonLayout = QHBoxLayout()
		imageLayout = QVBoxLayout()
		imageLayout.addStretch()
		encabezadoLayout = QHBoxLayout()
		fuenteDef = QFont('Open Sans', 10)
		fuente = QFont('Open Sans', 15)

		#Encabezado para advertencias y ayuda
		label_Recommend = QLabel('IMPORTANTE: Escriba el nombre de la red con sus mayusuculas y espacios si es que los tiene.')
		label_Recommend.setFont(fuenteDef)
		self.help = QPushButton('Ayuda')
		self.help.setStyleSheet('Height: 20px; font-family: Times; font: bold italic 15px; background-color: #3B83BD; color: white')
		self.help.clicked.connect(self.aiuda)
		encabezadoLayout.addWidget(label_Recommend)
		encabezadoLayout.addWidget(self.help)
		mainLayout.addLayout(encabezadoLayout)

		#Creacion de label e input para el SSID
		label_Wifi = QLabel('WiFi:')
		label_Wifi.setFont(fuente)
		self.chkhidden = QCheckBox('¿Oculta?')
		self.chkhidden.setChecked(False)
		self.chkhidden.stateChanged.connect(lambda:self.estado(self.chkhidden))
		self.textEntryNombre = QLineEdit()
		entryLayout_Name.addWidget(label_Wifi)
		entryLayout_Name.addWidget(self.textEntryNombre)
		entryLayout_Name.addWidget(self.chkhidden)
		mainLayout.addLayout(entryLayout_Name)

		#Creacion de label e input para la PASSWORD
		label_Pass = QLabel('Contraseña:')
		label_Pass.setFont(fuente)
		self.textEntryContra = QLineEdit()
		entryLayout_Pass.addWidget(label_Pass)
		entryLayout_Pass.addWidget(self.textEntryContra)
		mainLayout.addLayout(entryLayout_Pass)

		#Creacion de botones y agregacion al Layout
		botonesStyle = 'Height:50px; font-size:25px'
		self.generar = QPushButton('¡Generar!')
		self.generar.setStyleSheet(botonesStyle)
		self.generar.clicked.connect(self.generarQR)
		self.guardar = QPushButton('Guardar')
		self.guardar.setStyleSheet(botonesStyle)
		self.guardar.clicked.connect(self.guardarQR)
		self.limpiar = QPushButton('Limpiar')
		self.limpiar.setStyleSheet(botonesStyle)
		self.limpiar.clicked.connect(self.limpiar_campos)
		buttonLayout.addWidget(self.generar)
		buttonLayout.addWidget(self.guardar)
		buttonLayout.addWidget(self.limpiar)
		mainLayout.addLayout(buttonLayout)

		#Display de codigo generado
		self.imageLabel = QLabel()
		self.imageLabel.setAlignment(Qt.AlignCenter)
		imageLayout.addWidget(self.imageLabel)
		mainLayout.addLayout(imageLayout)		

		#Barra de mensajes
		self.statusBar = QStatusBar()
		mainLayout.addWidget(self.statusBar)

		self.setLayout(mainLayout)

	#Funcion para limpiar los campos y el codigo generado
	def limpiar_campos(self):
		self.textEntryNombre.clear()
		self.textEntryContra.clear()
		self.imageLabel.clear()
		self.chkhidden.setChecked(False)
		self.generar.setStyleSheet('')
		self.guardar.setStyleSheet('')

	#Funcion para generar el codigo QR
	def generarQR(self):
		SSID = self.textEntryNombre.text()
		PASSWORD = self.textEntryContra.text()
		if SSID:
			if self.chkhidden.isChecked() == True:
				img = wifi_qrcode_generator.wifi_qrcode(SSID, True, 'WPA', PASSWORD)
			else:
				img = wifi_qrcode_generator.wifi_qrcode(SSID, False, 'WPA', PASSWORD)
			self.generar.setStyleSheet('background-color: #008F39')
			qr = ImageQt(img)
			pix = QPixmap.fromImage(qr)
			self.imageLabel.setPixmap(pix)
		
	#Funcion para guardar el QR generado
	def guardarQR(self):
		current_dir = os.getcwd()
		archivo = self.textEntryNombre.text()
		if archivo:
			self.guardar.setStyleSheet('background-color: #008F39')
			self.imageLabel.pixmap().save(os.path.join(current_dir, archivo + '.png'))
			self.statusBar.showMessage('Se guardo correctamente el codigo en {0}'.format(os.path.join(current_dir, archivo + '.png')))

	#Verifica el estado del chkbox de oculto
	def estado(self, box):
		flag = False
		if box.isChecked() == True:
			flag = True
		return flag

	#Mensaje de ayuda
	def aiuda(self):
		QMessageBox.about(self, '¿Necesitas ayuda?', '¡Hola! Si llegaste aca es porque necesitas ayuda o queres realizar alguna recomendación.\nEscanea el codigo QR para ir a mi Instagram.')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = QRCodeApplication()
	demo.show()
	sys.exit(app.exec_())
