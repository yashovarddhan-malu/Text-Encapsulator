# Project Name - Text Encapsulator
# Author Name - Yashovarddhan Malu

# For UI file PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtGui
from qt_material import apply_stylesheet
import sys

# OCR Scanning packages
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract as pt
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adding pytesseract to PaTh

# Web Scraping Packages
import bs4 as bs
import urllib.request
import re

# Text Processing Packages
from PyDictionary import PyDictionary
from spellchecker import SpellChecker

# Function Definitions
from summary import summarizer
from web_scraping import Get_URL_Text

ui, _ = loadUiType("encapsulator.ui")

class MyWindow(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Text Encapsulator")
        self.setWindowIcon(QtGui.QIcon('icons\icon.png'))
        apply_stylesheet(app, theme = 'my_theme.xml')

        self.UI_Changes()
        self.Buttons()

    def UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)
        self.lineEdit.setDisabled(True)
        self.label_3.setVisible(False)
        self.label_6.setVisible(False)
        self.lineEdit_2.setDisabled(True)

    def Buttons(self):
        self.pushButton.clicked.connect(self.Open_Summarizer_Tab)
        self.pushButton_2.clicked.connect(self.Open_File_Tab)
        self.pushButton_3.clicked.connect(self.Open_Image_Tab)
        self.pushButton_4.clicked.connect(self.Open_URL_Tab)
        self.pushButton_10.clicked.connect(self.Open_Processing_Tab)

        self.pushButton_5.clicked.connect(self.Get_Summary)
        self.pushButton_6.clicked.connect(self.Reset_Button)
        self.pushButton_7.clicked.connect(self.Clear_Result_Button)
        self.pushButton_8.clicked.connect(self.Save_Summary)

        self.pushButton_13.clicked.connect(self.Open_File_Dialog)
        self.pushButton_12.clicked.connect(self.Get_File_Summary)
        self.pushButton_11.clicked.connect(self.File_Reset_Button)
        self.pushButton_14.clicked.connect(self.File_Clear_Result_Button)

        self.pushButton_16.clicked.connect(self.Open_Image_Dialog)
        self.pushButton_15.clicked.connect(self.Get_Image_Summary)
        self.pushButton_17.clicked.connect(self.Image_Reset_Button)
        self.pushButton_18.clicked.connect(self.Image_Clear_Result_Button)

        self.pushButton_19.clicked.connect(self.Get_URL_Data)
        self.pushButton_21.clicked.connect(self.Get_URL_Summary)
        self.pushButton_22.clicked.connect(self.URL_Reset)
        self.pushButton_20.clicked.connect(self.URL_Clear_Result)

        self.pushButton_24.clicked.connect(self.Spell_Check)
        self.pushButton_25.clicked.connect(self.Spell_Clear)
        self.pushButton_26.clicked.connect(self.Thesaurus)
        self.pushButton_27.clicked.connect(self.Thesaurus_Clear)

    # Opening Tabs 

    def Open_Summarizer_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_File_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    
    def Open_Image_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_URL_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Processing_Tab(self):
        self.tabWidget.setCurrentIndex(4)

    # Summarizer Tab 

    def Get_Summary(self):
        raw_text = self.plainTextEdit_2.toPlainText()
        sentences = self.lineEdit_4.text()
        final_text = summarizer(raw_text, sentences)
        self.plainTextEdit_3.setPlainText(final_text)
        text_length = str(len(raw_text.split()))
        summary_length = str(len(final_text.split()))
        self.lineEdit_5.setText(text_length)
        self.lineEdit_6.setText(summary_length)

    def Reset_Button(self):
        self.plainTextEdit_2.setPlainText('')

    def Clear_Result_Button(self):
        self.plainTextEdit_3.setPlainText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')

    def Save_Summary(self):
        raw_text = self.plainTextEdit_2.toPlainText()
        sentences = self.lineEdit_4.text()
        final_text = summarizer(raw_text, sentences)
        f = open("summary.txt", 'a')
        f.write(final_text)
        f.close()

    # File Processing Tab 

    def Open_File_Dialog(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]

        f = open(path, 'r')
        self.plainTextEdit_5.setPlainText(f.read())

        self.lineEdit.setDisabled(False)
        self.lineEdit.setText(path)
        self.lineEdit.setDisabled(True)
        self.label_3.setVisible(True)

    def Get_File_Summary(self):
        raw_text = self.plainTextEdit_5.toPlainText()
        sentences = self.lineEdit_7.text()
        final_text = summarizer(raw_text, sentences)
        self.plainTextEdit_4.setPlainText(final_text)
        text_length = str(len(raw_text.split()))
        summary_length = str(len(final_text.split()))
        self.lineEdit_8.setText(text_length)
        self.lineEdit_9.setText(summary_length)

    def File_Reset_Button(self):
        self.plainTextEdit_5.setPlainText('')
        self.lineEdit.setDisabled(False)
        self.lineEdit.setText('')
        self.lineEdit.setDisabled(True)
        self.label_3.setVisible(False)

    def File_Clear_Result_Button(self):
        self.plainTextEdit_4.setPlainText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.lineEdit_9.setText('')

    # OCR Tab

    def Open_Image_Dialog(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        image_text = (pt.image_to_string(Image.open(filename[0])))

        self.plainTextEdit_7.setPlainText(image_text)
        self.lineEdit_2.setDisabled(False)
        self.lineEdit_2.setText(path)
        self.lineEdit_2.setDisabled(True)
        self.label_6.setVisible(True)

    def Get_Image_Summary(self):
        raw_text = self.plainTextEdit_7.toPlainText()
        sentences = self.lineEdit_10.text()
        final_text = summarizer(raw_text, sentences)
        self.plainTextEdit_6.setPlainText(final_text)
        text_length = str(len(raw_text.split()))
        summary_length = str(len(final_text.split()))
        self.lineEdit_11.setText(text_length)
        self.lineEdit_12.setText(summary_length)

    def Image_Reset_Button(self):
        self.plainTextEdit_7.setPlainText('')
        self.lineEdit_2.setDisabled(False)
        self.lineEdit_2.setText('')
        self.lineEdit_2.setDisabled(True)
        self.label_6.setVisible(False)

    def Image_Clear_Result_Button(self):
        self.plainTextEdit_6.setPlainText('')
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_12.setText('')

    # URL Tab 

    def Get_URL_Data(self):
        url = self.lineEdit_3.text()
        url_text = Get_URL_Text(url)

        self.plainTextEdit_9.setPlainText(url_text)

    def Get_URL_Summary(self):
        url = self.lineEdit_3.text()
        url_text = Get_URL_Text(url)
        sentences = self.lineEdit_13.text()
        final_text = summarizer(url_text, sentences)
        text_length = str(len(url_text.split()))
        summary_length = str(len(final_text.split()))
        self.plainTextEdit_8.setPlainText(final_text)
        self.lineEdit_14.setText(text_length)
        self.lineEdit_15.setText(summary_length)

    def URL_Reset(self):
        self.plainTextEdit_9.setPlainText('')
        self.lineEdit_3.setText('')

    def URL_Clear_Result(self):
        self.plainTextEdit_8.setPlainText('')
        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')
        self.lineEdit_15.setText('')

    # Processing Tab 

    def Spell_Check(self):
        text = self.plainTextEdit_10.toPlainText()
        spell = SpellChecker(distance= 1)

        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        no_punc = ""
        for char in text:
            if char not in punctuations:
                no_punc += char

        misspelled = spell.unknown(no_punc.split())
        
        self.plainTextEdit_11.setPlainText('\n'.join(map(str, misspelled)))

        suggestions = []
        for word in misspelled:
            suggestions += spell.candidates(word)
        
        self.plainTextEdit_12.setPlainText('\n'.join(map(str, suggestions)))

    def Spell_Clear(self):
        self.plainTextEdit_10.setPlainText('')
        self.plainTextEdit_11.setPlainText('')
        self.plainTextEdit_12.setPlainText('')

    def Thesaurus(self):
        word = self.lineEdit_16.text()
        dictionary = PyDictionary()

        meanings = dictionary.meaning(word)
        synonyms = dictionary.synonym(word)
        antonyms = dictionary.antonym(word)

        meaning_list = list(meanings.items())
        string = '\n'.join(map(str, meaning_list))
        new_string = string.split('\n')

        for w in new_string:
            self.plainTextEdit_13.appendPlainText(w)
            self.plainTextEdit_13.appendPlainText('\n')

        # self.plainTextEdit_14.setPlainText('\n'.join(map(str, synonyms)))
        # self.plainTextEdit_16.setPlainText('\n'.join(map(str, antonyms)))

    def Thesaurus_Clear(self):
        self.plainTextEdit_13.setPlainText('')
        self.plainTextEdit_14.setPlainText('')
        self.plainTextEdit_16.setPlainText('')
        self.lineEdit_16.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)    
    window = MyWindow()
    window.show()
    app.exec_()