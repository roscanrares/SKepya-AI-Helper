from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QLabel, QComboBox, QTextEdit,
                             QProgressBar, QGroupBox, QStatusBar, QToolTip, QSplitter,
                             QMessageBox, QTabWidget, QScrollArea, QFrame, QToolBar)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QSize, QObject, pyqtSlot
from PyQt6.QtGui import QIcon, QFont, QKeySequence, QShortcut, QAction, QTextCursor, QColor
import sys
import os
import io
import datetime
from main import migration, comments_generator, refactor_variables, test_creation, readme_generator


# Custom output stream redirector
class OutputRedirector(QObject):
    outputWritten = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buffer = ""

    def write(self, text):
        if text:  # Don't write empty strings
            self._buffer += text
            if '\n' in text:  # If newline in text, emit signal
                self.outputWritten.emit(self._buffer)
                self._buffer = ""
            # Always ensure the original stdout gets the message too (for debugging)
            if hasattr(self, 'original_stream'):
                self.original_stream.write(text)

    def flush(self):
        if self._buffer:
            self.outputWritten.emit(self._buffer)
            self._buffer = ""
        if hasattr(self, 'original_stream'):
            self.original_stream.flush()


class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

    def __init__(self, operation_func, *args):
        super().__init__()
        self.operation_func = operation_func
        self.args = args
        self.is_cancelled = False

    def run(self):
        try:
            # Simulating progress updates - you would integrate real progress updates
            # from your actual functions
            self.status.emit("Starting operation...")
            self.progress.emit(10)

            self.operation_func(*self.args)

            if not self.is_cancelled:
                self.progress.emit(100)
                self.status.emit("Operation completed")
                self.finished.emit("Operation completed successfully!")
        except Exception as e:
            self.error.emit(str(e))

    def cancel(self):
        self.is_cancelled = True
        self.status.emit("Operation cancelled")
        self.terminate()


class CodeToolsUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.worker = None
        self.recent_files = []
        self.setWindowTitle("Code Tools")
        self.setGeometry(100, 100, 800, 600)

        # Set up stdout and stderr redirection
        self.setup_stdout_redirection()

        self.initUI()

        # Print startup message to see in console output
        print(f"Application started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current User: {os.getlogin()}")

    def setup_stdout_redirection(self):
        # Create redirectors for stdout and stderr
        self.stdout_redirector = OutputRedirector()
        self.stderr_redirector = OutputRedirector()

        # Store original streams
        self.stdout_redirector.original_stream = sys.stdout
        self.stderr_redirector.original_stream = sys.stderr

        # Replace system streams with our redirectors
        sys.stdout = self.stdout_redirector
        sys.stderr = self.stderr_redirector

    def initUI(self):
        # Main layout structure
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Create toolbar
        self.createToolbar()

        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(splitter)

        # Top section - File selection and operations
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        splitter.addWidget(top_widget)

        # File selection group
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout(file_group)

        file_selection_layout = QHBoxLayout()
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
        select_file_btn = QPushButton('Select File')
        select_file_btn.setIcon(QIcon.fromTheme("document-open"))
        select_file_btn.setToolTip("Choose a source code file to work with")
        select_file_btn.clicked.connect(self.selectFile)

        file_selection_layout.addWidget(select_file_btn)
        file_selection_layout.addWidget(self.file_label, stretch=1)
        file_layout.addLayout(file_selection_layout)

        # Recent files dropdown
        recent_files_layout = QHBoxLayout()
        recent_files_layout.addWidget(QLabel("Recent:"))
        self.recent_combo = QComboBox()
        self.recent_combo.setToolTip("Select from recently used files")
        self.recent_combo.currentIndexChanged.connect(self.loadRecentFile)
        recent_files_layout.addWidget(self.recent_combo, stretch=1)
        file_layout.addLayout(recent_files_layout)

        top_layout.addWidget(file_group)

        # Progress bar and status
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        progress_controls = QHBoxLayout()
        self.status_label = QLabel("Ready")
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon.fromTheme("process-stop"))
        self.cancel_btn.clicked.connect(self.cancelOperation)
        self.cancel_btn.setEnabled(False)

        progress_controls.addWidget(self.status_label, stretch=1)
        progress_controls.addWidget(self.cancel_btn)

        progress_layout.addWidget(self.progress_bar)
        progress_layout.addLayout(progress_controls)
        top_layout.addWidget(progress_group)

        # Operations group
        operations_group = QGroupBox("Operations")
        operations_layout = QVBoxLayout(operations_group)

        # Case type selection in a row
        case_layout = QHBoxLayout()
        self.case_label = QLabel('Variable naming convention:')
        self.case_combo = QComboBox()
        self.case_combo.addItems(['snake_case', 'camelCase', 'PascalCase'])
        self.case_combo.setToolTip("Select the naming style for variable refactoring")
        case_layout.addWidget(self.case_label)
        case_layout.addWidget(self.case_combo, stretch=1)
        operations_layout.addLayout(case_layout)

        # Operation buttons in a grid
        buttons_layout = QHBoxLayout()

        self.operations = [
            ('Generate Migration', self.runMigration, "Convert code to newer language version"),
            ('Generate Comments', self.runComments, "Add explanatory comments to the code"),
            ('Refactor Variables', self.runRefactorVariables, "Rename variables using selected convention"),
            ('Create Tests', self.runTestCreation, "Generate unit tests for the code"),
            ('Generate README', self.runReadmeGenerator, "Create a README file for the project")
        ]

        self.operation_buttons = {}
        for label, func, tooltip in self.operations:
            btn = QPushButton(label)
            btn.setToolTip(tooltip)
            btn.clicked.connect(func)
            buttons_layout.addWidget(btn)
            self.operation_buttons[label] = btn

            # Add keyboard shortcuts for buttons (Alt+first letter)
            shortcut_key = "Alt+" + label[0]
            shortcut = QShortcut(QKeySequence(shortcut_key), self)
            shortcut.activated.connect(func)
            btn.setToolTip(f"{tooltip} ({shortcut_key})")

        operations_layout.addLayout(buttons_layout)
        top_layout.addWidget(operations_group)

        # Bottom section - Results
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        splitter.addWidget(bottom_widget)

        # Results tab widget
        results_tabs = QTabWidget()

        # Result text
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        results_tabs.addTab(self.result_text, "Output")

        # Log tab
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        results_tabs.addTab(self.log_text, "Log")

        # Console output tab
        self.console_text = QTextEdit()
        self.console_text.setReadOnly(True)
        self.console_text.setFont(QFont("Courier New", 10))  # Monospaced font for console
        # Set a dark background and light text for console-like feel
        self.console_text.setStyleSheet("background-color: #1e1e1e; color: #f0f0f0;")
        results_tabs.addTab(self.console_text, "Console")

        # Connect our stdout/stderr redirectors to the console widget
        self.stdout_redirector.outputWritten.connect(self.append_stdout)
        self.stderr_redirector.outputWritten.connect(self.append_stderr)

        bottom_layout.addWidget(results_tabs)

        # Status bar at the bottom
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Set initial splitter sizes (60% top, 40% bottom)
        splitter.setSizes([6, 4])

        # Set Console as the default active tab
        results_tabs.setCurrentIndex(2)  # Index 2 is the Console tab

    @pyqtSlot(str)
    def append_stdout(self, text):
        """Append standard output text to the console widget"""
        self.console_text.moveCursor(QTextCursor.MoveOperation.End)
        self.console_text.insertPlainText(text)
        self.console_text.moveCursor(QTextCursor.MoveOperation.End)

    @pyqtSlot(str)
    def append_stderr(self, text):
        """Append standard error text to the console widget in red"""
        self.console_text.moveCursor(QTextCursor.MoveOperation.End)
        # Store current format to restore after inserting red text
        current_format = self.console_text.currentCharFormat()

        # Create format for error text (red)
        error_format = self.console_text.currentCharFormat()
        error_format.setForeground(QColor("red"))
        self.console_text.setCurrentCharFormat(error_format)

        # Insert the error text
        self.console_text.insertPlainText(text)

        # Restore original format
        self.console_text.setCurrentCharFormat(current_format)
        self.console_text.moveCursor(QTextCursor.MoveOperation.End)

    def createToolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        # Add toolbar actions
        open_action = QAction(QIcon.fromTheme("document-open"), "Open File", self)
        open_action.triggered.connect(self.selectFile)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        toolbar.addAction(open_action)

        toolbar.addSeparator()

        # Save result action
        save_action = QAction(QIcon.fromTheme("document-save"), "Save Result", self)
        save_action.triggered.connect(self.saveResult)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        toolbar.addAction(save_action)

        # Clear console action
        clear_console_action = QAction(QIcon.fromTheme("edit-clear"), "Clear Console", self)
        clear_console_action.triggered.connect(self.clearConsole)
        clear_console_action.setShortcut(QKeySequence("Ctrl+L"))
        toolbar.addAction(clear_console_action)

        # Help action
        help_action = QAction(QIcon.fromTheme("help-contents"), "Help", self)
        help_action.triggered.connect(self.showHelp)
        toolbar.addAction(help_action)

    def clearConsole(self):
        """Clear the console output"""
        self.console_text.clear()
        print("Console cleared")

    def closeEvent(self, event):
        """Restore original stdout and stderr when closing the application"""
        sys.stdout = self.stdout_redirector.original_stream
        sys.stderr = self.stderr_redirector.original_stream
        super().closeEvent(event)

    def selectFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")

        if file_name:
            self.selected_file = file_name
            self.file_label.setText(os.path.basename(file_name))
            self.statusBar.showMessage(f"File selected: {os.path.basename(file_name)}")
            print(f"Selected file: {file_name}")

            # Add to recent files if not already there
            if file_name not in self.recent_files:
                self.recent_files.insert(0, file_name)
                self.recent_files = self.recent_files[:5]  # Keep only last 5
                self.updateRecentFilesCombo()

    def updateRecentFilesCombo(self):
        self.recent_combo.clear()
        for file_path in self.recent_files:
            self.recent_combo.addItem(os.path.basename(file_path), file_path)

    def loadRecentFile(self, index):
        if index >= 0 and self.recent_combo.count() > 0:
            file_path = self.recent_combo.itemData(index)
            if file_path and os.path.exists(file_path):
                self.selected_file = file_path
                self.file_label.setText(os.path.basename(file_path))
                self.statusBar.showMessage(f"File selected: {os.path.basename(file_path)}")
                print(f"Loaded recent file: {file_path}")

    def showLoading(self, operation_name):
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Running {operation_name}...")
        self.cancel_btn.setEnabled(True)

        for btn in self.operation_buttons.values():
            btn.setEnabled(False)

        self.statusBar.showMessage(f"Running {operation_name}...")
        print(f"Starting operation: {operation_name}")

    def hideLoading(self):
        self.progress_bar.setValue(100)
        self.status_label.setText("Ready")
        self.cancel_btn.setEnabled(False)

        for btn in self.operation_buttons.values():
            btn.setEnabled(True)

        self.statusBar.showMessage("Ready")

    def handleOperationProgress(self, value):
        self.progress_bar.setValue(value)
        print(f"Progress: {value}%")

    def handleOperationStatus(self, message):
        self.status_label.setText(message)
        self.log_text.append(message)
        print(f"Status: {message}")

    def handleOperationComplete(self, message):
        self.hideLoading()
        self.statusBar.showMessage(message, 5000)  # Show message for 5 seconds
        self.log_text.append(f"SUCCESS: {message}")
        print(f"Operation completed: {message}")
        QMessageBox.information(self, "Operation Complete", message)

    def handleOperationError(self, error_message):
        self.hideLoading()
        self.statusBar.showMessage(f"Error: {error_message}", 10000)
        self.log_text.append(f"ERROR: {error_message}")
        print(f"ERROR: {error_message}", file=sys.stderr)  # This will appear in red in our console
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_message}")

    def cancelOperation(self):
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(self, "Confirm Cancel",
                                         "Are you sure you want to cancel the current operation?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                print("Operation cancelled by user")
                self.worker.cancel()
                self.hideLoading()

    def checkFile(self):
        if not self.selected_file:
            QMessageBox.warning(self, "No File Selected",
                                "Please select a file first.")
            print("Error: No file selected")
            return False

        if not os.path.exists(self.selected_file):
            QMessageBox.critical(self, "File Not Found",
                                 f"The selected file '{self.selected_file}' no longer exists.")
            print(f"Error: File not found: {self.selected_file}")
            return False

        return True

    def runThreadedOperation(self, operation_func, operation_name, *args):
        if not self.checkFile():
            return

        # Confirm potentially destructive operations
        if operation_name in ["Migration", "Refactor Variables"]:
            reply = QMessageBox.question(self, "Confirm Operation",
                                         f"This operation ({operation_name}) may modify your code. Continue?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                print(f"Operation {operation_name} cancelled by user")
                return

        self.showLoading(operation_name)
        self.worker = WorkerThread(operation_func, *args)
        self.worker.finished.connect(lambda msg: self.handleOperationComplete(f"{operation_name} completed!"))
        self.worker.error.connect(self.handleOperationError)
        self.worker.progress.connect(self.handleOperationProgress)
        self.worker.status.connect(self.handleOperationStatus)
        self.worker.finished.connect(lambda msg: setattr(self, 'last_operation', operation_name.lower()))
        self.worker.start()

        # Set result preview
        self.result_text.clear()
        self.result_text.append(f"Running {operation_name}...\n")
        self.result_text.append(f"File: {self.selected_file}\n")
        if operation_name == "Refactor Variables":
            case_type = self.case_combo.currentText()
            self.result_text.append(f"Using naming convention: {case_type}\n")
            print(f"Refactoring variables to {case_type}")

    def runMigration(self):
        self.runThreadedOperation(migration, "Migration", self.selected_file)

    def runComments(self):
        self.runThreadedOperation(comments_generator, "Comments", self.selected_file)

    def runRefactorVariables(self):
        case_type = self.case_combo.currentText()
        self.runThreadedOperation(refactor_variables, "Refactor Variables", self.selected_file, case_type)

    def runTestCreation(self):
        self.runThreadedOperation(test_creation, "Test Creation", self.selected_file)

    def runReadmeGenerator(self):
        self.runThreadedOperation(readme_generator, "README Generator", self.selected_file)

    def saveResult(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Result", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write(self.result_text.toPlainText())
                self.statusBar.showMessage(f"Result saved to {file_name}", 5000)
                print(f"Results saved to file: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save file: {str(e)}")
                print(f"ERROR: Failed to save file: {str(e)}", file=sys.stderr)

    def showHelp(self):
        help_text = """
        <h3>Code Tools Help</h3>
        <p>This application provides various code manipulation tools:</p>
        <ul>
            <li><b>Generate Migration</b>: Convert code to newer language versions</li>
            <li><b>Generate Comments</b>: Add explanatory comments to code</li>
            <li><b>Refactor Variables</b>: Rename variables according to conventions</li>
            <li><b>Create Tests</b>: Generate unit tests for code</li>
            <li><b>Generate README</b>: Create documentation for your code</li>
        </ul>
        <p>To get started, select a file using the 'Select File' button.</p>
        <p>You can view console output in the 'Console' tab.</p>
        """

        QMessageBox.information(self, "Help", help_text)
        print("Help dialog shown")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a more modern look

    # Set application-wide tooltip styling
    QToolTip.setFont(QFont('SansSerif', 10))

    window = CodeToolsUI()
    window.show()
    sys.exit(app.exec())
