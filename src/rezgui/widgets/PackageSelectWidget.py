from rezgui.qt import QtCore, QtGui
from rezgui.mixins.ContextViewMixin import ContextViewMixin
from rezgui.dialogs.BrowsePackageDialog import BrowsePackageDialog
from rezgui.widgets.PackageLineEdit import PackageLineEdit
from rezgui.widgets.IconButton import IconButton


class PackageSelectWidget(QtGui.QWidget, ContextViewMixin):

    focusOutViaKeyPress = QtCore.Signal(str)
    focusOut = QtCore.Signal(str)
    textChanged = QtCore.Signal(str)

    def __init__(self, context_model=None, parent=None):
        super(PackageSelectWidget, self).__init__(parent)
        ContextViewMixin.__init__(self, context_model)

        self.edit = PackageLineEdit(self.context_model, self)
        self.edit.setStyleSheet("QLineEdit { border : 0px;}")
        self.btn = IconButton("round_plus")
        self.btn.hide()

        layout = QtGui.QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.edit, 1)
        layout.addWidget(self.btn)
        self.setLayout(layout)

        self.edit.focusIn.connect(self._focusIn)
        self.edit.focusOut.connect(self._focusOut)
        self.edit.focusOutViaKeyPress.connect(self._focusOutViaKeyPress)
        self.edit.textChanged.connect(self._textChanged)
        self.btn.clicked.connect(self._browse_package)

    def text(self):
        return self.edit.text()

    def setText(self, txt):
        self.edit.setText(txt)

    def clone_into(self, other):
        self.edit.clone_into(other.edit)

    def setFocus(self):
        self.edit.setFocus()
        self.btn.show()

    def _focusIn(self):
        self.btn.show()

    def _focusOut(self, txt):
        self.btn.hide()
        self.focusOut.emit(txt)

    def _focusOutViaKeyPress(self, txt):
        self.btn.hide()
        self.focusOutViaKeyPress.emit(txt)

    def _textChanged(self, txt):
        self.textChanged.emit(txt)

    def _browse_package(self, button):
        self.btn.show()
        # TODO
        dlg = BrowsePackageDialog(context_model=self.context_model,
                                  package_text=self.text(),
                                  parent=self.parentWidget())
        dlg.exec_()
        if dlg.package:
            txt = dlg.package.qualified_name
            self.setText(txt)
        self.setFocus()
