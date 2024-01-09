import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QMessageBox, QFileDialog, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur de texte")
        self.resize(800, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.create_menu()

    def create_menu(self):
        # Menu Fichier
        file_menu = self.menuBar().addMenu("Fichier")

        new_action = QAction(QIcon(), "Nouveau", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction(QIcon(), "Ouvrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon(), "Enregistrer", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction(QIcon(), "Enregistrer sous", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        # Ajout d'une séparation entre les actions d'impression et les autres
        file_menu.addSeparator()
        
        print_action = QAction(QIcon(), "Imprimer", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_file)
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction(QIcon(), "Quitter", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Menu Édition
        edit_menu = self.menuBar().addMenu("Édition")

        undo_action = QAction(QIcon(), "Annuler", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(), "Rétablir", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        copy_action = QAction(QIcon(), "Copier", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(), "Coller", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)
        
        search_menu = self.menuBar().addMenu("Recherche")

        find_action = QAction(QIcon(), "Rechercher", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_text)
        search_menu.addAction(find_action)

    def new_file(self):
        self.text_edit.clear()
        
    def print_file(self):
        printer = QPrinter(QPrinter.HighResolution)
        print_dialog = QPrintDialog(printer, self)

        if print_dialog.exec_() == QPrintDialog.Accepted:
            self.text_edit.print_(printer)
        
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier", "", "Fichiers texte (*.txt)")
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
            except IOError:
                QMessageBox.critical(self, "Erreur", "Impossible d'ouvrir le fichier.")

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier", "", "Fichiers texte (*.txt)")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "Enregistrement", "Le fichier a été enregistré avec succès.")
            except IOError:
                QMessageBox.critical(self, "Erreur", "Impossible d'enregistrer le fichier.")

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier sous", "", "Fichiers texte (*.txt)")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "Enregistrement", "Le fichier a été enregistré avec succès.")
            except IOError:
                QMessageBox.critical(self, "Erreur", "Impossible d'enregistrer le fichier.")
    
    def find_text(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Rechercher")
        layout = QVBoxLayout()

        label = QLabel("Mot à rechercher :")
        layout.addWidget(label)

        search_input = QLineEdit()
        layout.addWidget(search_input)

        find_button = QPushButton("Rechercher")
        find_button.clicked.connect(lambda: self.search_text(search_input.text()))
        layout.addWidget(find_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def search_text(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.Start)

        if cursor.selectedText() == text:
            cursor = self.text_edit.textCursor()
        else:
            cursor = self.text_edit.document().find(text)

        if not cursor.isNull():
            self.text_edit.setTextCursor(cursor)
        else:
            QMessageBox.information(self, "Recherche", "Aucune correspondance trouvée.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    text_editor = TextEditor()
    text_editor.show()
    sys.exit(app.exec_())