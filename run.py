import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox, QGroupBox, QTabWidget,\
	 QTextEdit, QTableWidget, QCheckBox, QLineEdit, QSlider, QTableWidget, QTableWidgetItem, QMenu, QAction, QSizePolicy
from PyQt5.QtCore import QObject, Qt, QEvent, QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtGui import *

from pywinauto import application , findwindows, win32_element_info

import win32clipboard

import image_scan

class OptionWidget(QWidget):
	def __init__(self):
		super().__init__()

		# 0 = startX  , 1 = startY , 2 = sizeX , 3 = sizeY 
		self.image_scan_team1 = [330, 212 , 315,23]
		self.image_scan_team2 = [1210, 212 , 315,23]

		self.title = 'Option'
		self.setWindowTitle(self.title)
		self.resize( 20, 20)

	def initUI(self):		
		self.all_layout = QVBoxLayout()

		hbox = QHBoxLayout()

		self.image_scan_team1_lineedit = []
		self.image_scan_team2_lineedit = []

		def image_point(image_p, point, box, teamName):
			box_g = QGroupBox(teamName)
			vbox_g = QHBoxLayout()
			for r in range(4) :
				vbox = QVBoxLayout()
				label_text = ''
				if r == 0 :
					label_text = 'startX'
				if r == 1 :
					label_text = 'startY'
				if r == 2 :
					label_text = 'sizeX'
				if r == 3 :
					label_text = 'sizeY'
				label_t = QLabel(label_text)
				vbox.addWidget(label_t)
				image_p.append( QLineEdit() )
				image_p[r].setValidator(QIntValidator())
				image_p[r].setText( str(point[r]) )
				image_p[r].textEdited.connect( self.p_textEdited )
				vbox.addWidget(image_p[r])
				vbox_g.addLayout(vbox)
			
			box_g.setLayout(vbox_g)
			box.addWidget(box_g)

		image_point(self.image_scan_team1_lineedit , self.image_scan_team1 , hbox, 'team1' )
		image_point(self.image_scan_team2_lineedit , self.image_scan_team2 , hbox, 'team2' )


		self.all_layout.addLayout(hbox)

		self.setLayout(self.all_layout)

	def p_textEdited(self, text):
		for r in range(4):
			self.image_scan_team1[r] = int(self.image_scan_team1_lineedit[r].text())
			self.image_scan_team2[r] = int(self.image_scan_team2_lineedit[r].text())


class myQTableWidget(QTableWidget):
	def __init__(self, *args, **kwargs):
		super(myQTableWidget, self).__init__(*args, **kwargs)
		 
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.contextMenu)
		 
	def contextMenu(self, point):
		menu = QMenu(self)
		 
		#for i in range(5):
		action = QAction('copy', self)

		action.triggered.connect(self.buttonClicked)
		menu.addAction(action)
		 
		menu.exec_(self.mapToGlobal(point))

	def buttonClicked(self):
		nametext = ''
		items = self.selectedItems()
		num = 0
		#print(len(items))
		for item in items :
			nametext = nametext + item.text()
			if len(items)-1 != num :
				nametext = nametext + '\n'
			num = num + 1

		#print(nametext)

		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardText(nametext)
		win32clipboard.CloseClipboard()


class MainWidget(QWidget):

	def __init__(self):
		super().__init__()

		self.OWidget = OptionWidget()

		self.initUI()
		self.show()

	def initUI(self):
		self.all_layout = QVBoxLayout()

		# SoftListComboBox Box -----------------------------
		self.f_SoftListComboBox()

		# Buttons Box --------------------------------------
		self.f_buttons()

		# Output Box ---------------------------------------
		self.f_Output()


		# option box ---------------------------------------
		self.f_optionBox()


		self.setLayout(self.all_layout)


	def f_SoftListComboBox(self):
		hbox_SoftListComboBox = QHBoxLayout()
			
		# 現在起動中ソフト確認
		self.sNamelist, self.sHandlelist = self.getSoftwareList()
		# コンボボックス設定
		label_SoftListComboBox = QLabel("対象ソフト:")
		self.SoftListComboBox = QComboBox()
		for Name in self.sNamelist:
			self.SoftListComboBox.addItem(Name)
		
		hbox_SoftListComboBox.addWidget(label_SoftListComboBox)
		hbox_SoftListComboBox.addWidget(self.SoftListComboBox)
		self.all_layout.addLayout(hbox_SoftListComboBox)


	def f_buttons(self):
		hbox = QHBoxLayout()

		#self.label = QLabel("label test")
		btn2 = QPushButton("スキャン")
		
		self.BFV_checkbox = QCheckBox("BFVスキャンモード")
		self.BFV_checkbox.setChecked(True)

		# クリックされたらbuttonClickedの呼び出し       
		btn2.clicked.connect(self.scan_buttonClicked)

		hbox.addWidget(self.BFV_checkbox)
		hbox.addStretch(1)
		hbox.addWidget(btn2)

		vbox = QVBoxLayout()
		self.TestMode_checkbox = QCheckBox("テストモード")
		self.Tesseract_lineedit = QLineEdit()
		self.Tesseract_lineedit.setText('C:\\Program Files\\Tesseract-OCR')
		self.Tesseracttessdata_lineedit = QLineEdit()
		self.Tesseracttessdata_lineedit.setText('C:\\Program Files\\Tesseract-OCR\\tessdata')
		
		self.matchnum_slider = QSlider(Qt.Horizontal)
		self.matchnum_slider.setMinimum(100)
		self.matchnum_slider.setMinimum(0)
		self.matchnum_slider.setValue(95)
		
		self.matchnum_label = QLabel("類似度判定  " + str(self.matchnum_slider.value()) + "%")
		self.matchnum_slider.valueChanged.connect(self.matchnum_mouseMoveEvent)

		vbox.addWidget(self.TestMode_checkbox)
		vbox.addWidget(self.Tesseract_lineedit)
		vbox.addWidget(self.Tesseracttessdata_lineedit)
		vbox.addWidget(self.matchnum_label)
		vbox.addWidget(self.matchnum_slider)


		self.all_layout.addLayout(hbox)
		self.all_layout.addLayout(vbox)

	def f_Output(self):
		Groupbox_Output = QGroupBox("出力結果")

		Layout_Output = QVBoxLayout()
	
		team1_Output = QGroupBox("team1 [左側]")
		team1_list = QHBoxLayout()

		self.team1_Textbox_Output_User = myQTableWidget(1,1)
		self.team1_Textbox_Output_Black = myQTableWidget(1,1)

		tab1 = QTabWidget()
		tab1.addTab(self.team1_Textbox_Output_User, "Player List")
		tab1.addTab(self.team1_Textbox_Output_Black, "Black User")

		team1_list.addWidget(tab1)		
		team1_Output.setLayout(team1_list)



		team2_Output = QGroupBox("team2 [右側]")		
		team2_list = QHBoxLayout()
		
		self.team2_Textbox_Output_User = myQTableWidget(1,1)
		self.team2_Textbox_Output_Black = myQTableWidget(1,1)

		tab2 = QTabWidget()
		tab2.addTab(self.team2_Textbox_Output_User, "Player List")
		tab2.addTab(self.team2_Textbox_Output_Black, "Black User")
		
		team2_list.addWidget(tab2)
		team2_Output.setLayout(team2_list)

		Layout_Output.addWidget(team1_Output)
		Layout_Output.addWidget(team2_Output)
		#Layout_Output.addWidget(tab2)

		Groupbox_Output.setLayout(Layout_Output)

		self.all_layout.addWidget(Groupbox_Output)


	def scan_buttonClicked(self):		
		print("scan")

		self.app = application.Application()
		self.app = self.app.connect(handle=self.sHandlelist[ self.SoftListComboBox.currentIndex() ])

		title = ''
		hit = False
		for soft in findwindows.find_elements():
			if soft.handle == self.sHandlelist[ self.SoftListComboBox.currentIndex() ]:
				title = soft.class_name
				hit = True
				break
		
		if hit == True:
			self.app[title].CaptureAsImage().save('game_window.png')
			
			if self.BFV_checkbox.isChecked() == False:
				return

			scan = image_scan.image_scan()

			size_team1 = self.OWidget.image_scan_team1
			print(size_team1)
			size_team2 = self.OWidget.image_scan_team2

			scan.team1_box_point = [size_team1[0], size_team1[1]]
			scan.team2_box_point = [size_team2[0], size_team2[1]]
			scan.team1_box_size = [size_team1[2],size_team1[3]]
			scan.team2_box_size = [size_team2[2],size_team2[3]]

			scan.path = self.Tesseract_lineedit.text
			scan.tessdata_path = self.Tesseracttessdata_lineedit.text

			scan.matchNum = self.matchnum_slider.value() / 100

			pfileName = 'game_window.png'
			if self.TestMode_checkbox.isChecked() == True:
				pfileName = 'window_test.png'
			NameList1, NameList2, b_team1, b_team2 = scan.run(pfileName)

			#NameList1 = ["test1","test2"]
			#NameList2 = ["test3","test4"]
			#b_team1 = ['OUT_1','OUT_2']
			#b_team2 = ['OUT_3','OUT_4']

			def Table_addItem(NameList,team_Textbox_Output):
				num = 0
				#print(NameList)
				team_Textbox_Output.setRowCount(len(NameList))
				for i in NameList:
					cubesHeaderItem = QTableWidgetItem(str(i))
					team_Textbox_Output.setItem(0,num,cubesHeaderItem)
					#print(NameList)
					num = num + 1

			Table_addItem(NameList1, self.team1_Textbox_Output_User)
			Table_addItem(b_team1, self.team1_Textbox_Output_Black)
			Table_addItem(NameList2, self.team2_Textbox_Output_User)
			Table_addItem(b_team2, self.team2_Textbox_Output_Black)
		

	def matchnum_mouseMoveEvent(self, event):
		self.matchnum_label.setText("類似度判定  " + str(self.matchnum_slider.value()) + "%")


	def getSoftwareList(self):
		sNamelist=[]
		sHandlelist=[]

		for softlist in findwindows.find_elements():
			if softlist.rich_text != "":
				sNamelist.append(softlist.rich_text) # 表示用
				sHandlelist.append(softlist.handle) # データ用


		return sNamelist, sHandlelist

	def f_optionBox(self):
		hbox = QHBoxLayout()
		hbox.addStretch(1)
		optionbutton = QPushButton("詳細設定")
		optionbutton.clicked.connect(self.optionbox)

		hbox.addWidget(optionbutton)
		self.all_layout.addLayout(hbox)

	def optionbox(self):
		self.OWidget.initUI()

		self.OWidget.show()
		print("test")



class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		#self.w = worker()

		self.title = 'BFV NameScan software'
		#self.width = 400
		#self.height = 200
		self.setWindowTitle(self.title)
		#self.setGeometry(0, 0, self.width, self.height)

		self.mWidget = MainWidget()
		self.setCentralWidget(self.mWidget)

		self.statusBar()

		self.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()

	sys.exit(app.exec_())