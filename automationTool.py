import pandas as pd
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class temsilci(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__()

    def olustur(self, parent, option, index):
        olustur = QLineEdit(parent)
        olustur.setValidator(QDoubleValidator())
        return olustur

class bakkalBorcDefteri(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setStyleSheet('font-size: 25px;')
        
        Satirlar, Sütünlar = self.df.shape
        self.setColumnCount(Sütünlar)
        self.setRowCount(Satirlar)
        self.setHorizontalHeaderLabels(("Müşteri Adı-Soyad","Borç Tutarı","Son Ödeme tarihi","Ödendi/Ödenmedi","Ödeme Tipi"))
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setItemDelegateForColumn(1, temsilci())

    
        for x in range(self.rowCount()):
            for y in range(self.columnCount()):
                self.setItem(x, y, QTableWidgetItem(str(self.df.iloc[x, y])))

        self.cellChanged[int, int].connect(self.guncellemeDF)   

    def guncellemeDF(self, satir, sütün):
        metin = self.item(satir, sütün).text()
        self.df.iloc[satir, sütün] = metin
    

class DF(QWidget):
    
    veri = np.array([["Müşteri Bilgisi Giriniz",0,"Tarih Belirt"], ["Müşteri Bilgisi Giriniz",0,"Tarih Belirt"],["Müşteri Bilgisi Giriniz",0,"Tarih Belirt"]])
    df = pd.DataFrame(data=veri, index=[1,2,3], columns =["Müşteri Adı-Soyad","Borç Tutarı","Son Ödeme tarihi"])
    df["Ödendi/Ödenmedi"] = pd.Series(data=["Durum Ne", "Durum Ne","Durum Ne"], index=[1,2,3])
    df["Ödeme Tipi"] = pd.Series(data=["Kredi", "Nakit","Kredi"], index=[1,2,3])
    df.loc[4] = pd.Series(data=["Müşteri Bilgisi Giriniz",0,"Tarih Belirt","Durum Ne","Kredi"], index=["Müşteri Adı-Soyad","Borç Tutarı","Son Ödeme tarihi","Ödendi/Ödenmedi","Ödeme Tipi"])
    df.loc[5] = pd.Series(data=["Müşteri Bilgisi Giriniz",0,"Tarih Belirt","Durum Ne","Nakit"], index=["Müşteri Adı-Soyad","Borç Tutarı","Son Ödeme tarihi","Ödendi/Ödenmedi","Ödeme Tipi"])
    df.loc[6] = pd.Series(data=["Müşteri Bilgisi Giriniz",0,"Tarih Belirt","Durum Ne","Nakit"], index=["Müşteri Adı-Soyad","Borç Tutarı","Son Ödeme tarihi","Ödendi/Ödenmedi","Ödeme Tipi"])
    
    def __init__(self):
        super().__init__()
        self.setGeometry(1400,900,1300,600)
        self.move(50,70)
        self.setStyleSheet("background-color: orange;") 
        self.setWindowTitle("Bakkal Borç Defteri".upper())
        self.setWindowIcon(QIcon('icon2.png'))
        
        anaYerlesim = QVBoxLayout()
        self.table = bakkalBorcDefteri(DF.df)
        anaYerlesim.addWidget(self.table)

        yazdir = QPushButton('Girdileri Konsola Yazdır')
        yazdir.setStyleSheet('font-size: 37px')
        yazdir.clicked.connect(self.girdi_degerlerini_yazdir)
        anaYerlesim.addWidget(yazdir)

        cikti = QPushButton('CSV Dosyasına Aktar')
        cikti.setStyleSheet('font-size: 37px')
        cikti.clicked.connect(self.CSV_dosyasina_aktar)
        anaYerlesim.addWidget(cikti)
        self.setLayout(anaYerlesim)

    def CSV_dosyasina_aktar(self):
        self.table.df.to_csv('BORÇ DEFTER KAYDI.csv', index=False)
        print('CSV dosyası dışa aktarıldı')
    
    def girdi_degerlerini_yazdir(self):
        print(self.table.df)


uyg = QApplication(sys.argv)
bakkalBorcDefteri = DF()
bakkalBorcDefteri.show()
sys.exit(uyg.exec_())

