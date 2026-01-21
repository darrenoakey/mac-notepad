#!/usr/bin/env python3
import sys
from pathlib import Path
import setproctitle
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QMessageBox
)
from PySide6.QtGui import QAction, QKeySequence, QIcon


# ##################################################################
# notepad window
# simple text editor mimicking windows notepad using pyside6
class NotepadWindow(QMainWindow):
    def __init__(self, filepath: str | None = None) -> None:
        super().__init__()
        self.current_file: Path | None = None
        self.text_modified = False
        self._setup_window()
        self._setup_text_area()
        self._setup_menu()
        if filepath:
            self._open_file_path(Path(filepath))

    # ##################################################################
    # setup window
    # configure the main window title and size
    def _setup_window(self) -> None:
        self.setWindowTitle("Untitled - Notepad")
        self.resize(800, 600)
        icon_path = Path(__file__).parent.parent / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    # ##################################################################
    # setup text area
    # create the main text editing widget
    def _setup_text_area(self) -> None:
        self.text = QPlainTextEdit()
        self.text.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.text.textChanged.connect(self._on_text_changed)
        self.setCentralWidget(self.text)

    # ##################################################################
    # setup menu
    # create the file and edit menus matching windows notepad
    def _setup_menu(self) -> None:
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")

        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.text.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.text.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.text.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.text.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.text.paste)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.text.selectAll)
        edit_menu.addAction(select_all_action)

    # ##################################################################
    # on text changed
    # track when text has been modified
    def _on_text_changed(self) -> None:
        self.text_modified = True
        self._update_title()

    # ##################################################################
    # update title
    # show filename and modified indicator in window title
    def _update_title(self) -> None:
        name = self.current_file.name if self.current_file else "Untitled"
        modified = "*" if self.text_modified else ""
        self.setWindowTitle(f"{modified}{name} - Notepad")

    # ##################################################################
    # check save
    # ask user to save if there are unsaved changes
    def _check_save(self) -> bool:
        if not self.text_modified:
            return True
        response = QMessageBox.question(
            self, "Notepad", "Do you want to save changes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        if response == QMessageBox.StandardButton.Cancel:
            return False
        if response == QMessageBox.StandardButton.Yes:
            return self._save_file()
        return True

    # ##################################################################
    # new file
    # clear editor for a new document
    def _new_file(self) -> None:
        if not self._check_save():
            return
        self.text.clear()
        self.current_file = None
        self.text_modified = False
        self._update_title()

    # ##################################################################
    # open file
    # show file dialog and open selected file
    def _open_file(self) -> None:
        if not self._check_save():
            return
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)"
        )
        if filepath:
            self._open_file_path(Path(filepath))

    # ##################################################################
    # open file path
    # load content from a specific file path
    def _open_file_path(self, filepath: Path) -> None:
        try:
            content = filepath.read_text()
            self.text.setPlainText(content)
            self.current_file = filepath
            self.text_modified = False
            self._update_title()
        except Exception as err:
            QMessageBox.critical(self, "Error", f"Cannot open file: {err}")

    # ##################################################################
    # save file
    # save to current file or prompt for new filename
    def _save_file(self) -> bool:
        if self.current_file:
            return self._write_file(self.current_file)
        return self._save_file_as()

    # ##################################################################
    # save file as
    # prompt for filename and save
    def _save_file_as(self) -> bool:
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt);;All Files (*)"
        )
        if filepath:
            return self._write_file(Path(filepath))
        return False

    # ##################################################################
    # write file
    # write text content to disk
    def _write_file(self, filepath: Path) -> bool:
        try:
            content = self.text.toPlainText()
            filepath.write_text(content)
            self.current_file = filepath
            self.text_modified = False
            self._update_title()
            return True
        except Exception as err:
            QMessageBox.critical(self, "Error", f"Cannot save file: {err}")
            return False

    # ##################################################################
    # close event
    # handle window close with save check
    def closeEvent(self, event) -> None:
        if self._check_save():
            event.accept()
        else:
            event.ignore()


# ##################################################################
# main
# entry point - create app and show window
def main(filepath: str | None = None) -> int:
    setproctitle.setproctitle("notepad")
    app = QApplication(sys.argv)
    window = NotepadWindow(filepath)
    window.show()
    return app.exec()
