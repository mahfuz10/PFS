#Boa:Frame:FrmMain
#
# PhotoFilmStrip - Creates movies out of your pictures.
#
# Copyright (C) 2008 Jens Goepfert
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import os, sys

import wx
from wx.lib.wordwrap import wordwrap

from core.Picture import Picture
from core.PhotoFilmStrip import PhotoFilmStrip

from lib.Settings import Settings
from lib.common.ObserverPattern import Observer

from gui.ctrls.ImageSectionEditor import ImageSectionEditor, EVT_RECT_CHANGED
from gui.ctrls.PyListView import PyListView
from gui.DlgRender import DlgRender
from gui.PnlEditPicture import PnlEditPicture
from gui.ActionManager import ActionManager

from res.license import licenseText


[wxID_FRMMAIN, wxID_FRMMAINBITMAPLEFT, wxID_FRMMAINBITMAPRIGHT, 
 wxID_FRMMAINCMDMOVELEFT, wxID_FRMMAINCMDMOVERIGHT, wxID_FRMMAINCMDREMOVE, 
 wxID_FRMMAINLISTVIEW, wxID_FRMMAINPANELTOP, wxID_FRMMAINPNLEDITPICTURE, 
] = [wx.NewId() for _init_ctrls in range(9)]


class FrmMain(wx.Frame, Observer):
    
    _custom_classes = {"wx.Panel": ["ImageSectionEditor",
                                    "PnlEditPicture"],
                       "wx.ListView": ["PyListView"]}
    
    def _init_coll_sizerPictures_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.listView, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.sizerPictureCtrls, 0, border=0, flag=wx.EXPAND)

    def _init_coll_sizerPictureCtrls_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.cmdMoveLeft, 0, border=2, flag=wx.ALL)
        parent.AddStretchSpacer(1)
        parent.AddWindow(self.cmdMoveRight, 0, border=2, flag=wx.ALL)
        parent.AddStretchSpacer(1)
        parent.AddWindow(self.cmdRemove, 0, border=2, flag=wx.ALL)

    def _init_coll_sizerMain_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panelTop, 1, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.pnlEditPicture, 0, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.sizerPictures, 0, border=0, flag=wx.EXPAND)

    def _init_coll_sizerPnlTop_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.bitmapLeft, 1, border=2, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.bitmapRight, 1, border=2, flag=wx.ALL | wx.EXPAND)

    def _init_sizers(self):
        # generated method, don't edit
        self.sizerPnlTop = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.sizerMain = wx.BoxSizer(orient=wx.VERTICAL)

        self.sizerPictures = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.sizerPictureCtrls = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_sizerPnlTop_Items(self.sizerPnlTop)
        self._init_coll_sizerMain_Items(self.sizerMain)
        self._init_coll_sizerPictures_Items(self.sizerPictures)
        self._init_coll_sizerPictureCtrls_Items(self.sizerPictureCtrls)

        self.SetSizer(self.sizerMain)
        self.panelTop.SetSizer(self.sizerPnlTop)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRMMAIN, name=u'FrmMain', parent=prnt,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
              style=wx.DEFAULT_FRAME_STYLE, title='PhotoFilmStrip')
        self.SetClientSize(wx.Size(400, 250))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.panelTop = wx.Panel(id=wxID_FRMMAINPANELTOP, name=u'panelTop',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
              style=wx.TAB_TRAVERSAL)

        self.bitmapLeft = ImageSectionEditor(id=wxID_FRMMAINBITMAPLEFT,
              name=u'bitmapLeft', parent=self.panelTop, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL)

        self.bitmapRight = ImageSectionEditor(id=wxID_FRMMAINBITMAPRIGHT,
              name=u'bitmapRight', parent=self.panelTop, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL)

        self.pnlEditPicture = PnlEditPicture(id=wxID_FRMMAINPNLEDITPICTURE,
              name=u'pnlEditPicture', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL)

        self.listView = PyListView(id=wxID_FRMMAINLISTVIEW, name=u'listView',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, 120),
              style=wx.LC_ICON | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)
        self.listView.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListViewListItemSelected, id=wxID_FRMMAINLISTVIEW)
        self.listView.Bind(wx.EVT_LIST_ITEM_DESELECTED,
              self.OnListViewListItemDeselected, id=wxID_FRMMAINLISTVIEW)

        self.cmdMoveLeft = wx.BitmapButton(bitmap=wx.ArtProvider.GetBitmap('wxART_GO_BACK',
              wx.ART_TOOLBAR, wx.DefaultSize), id=wxID_FRMMAINCMDMOVELEFT,
              name=u'cmdMoveLeft', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=wx.BU_AUTODRAW)
        self.cmdMoveLeft.Bind(wx.EVT_BUTTON, self.OnCmdMoveLeftButton,
              id=wxID_FRMMAINCMDMOVELEFT)

        self.cmdMoveRight = wx.BitmapButton(bitmap=wx.ArtProvider.GetBitmap('wxART_GO_FORWARD',
              wx.ART_TOOLBAR, wx.DefaultSize), id=wxID_FRMMAINCMDMOVERIGHT,
              name=u'cmdMoveRight', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=wx.BU_AUTODRAW)
        self.cmdMoveRight.Bind(wx.EVT_BUTTON, self.OnCmdMoveRightButton,
              id=wxID_FRMMAINCMDMOVERIGHT)

        self.cmdRemove = wx.BitmapButton(bitmap=wx.ArtProvider.GetBitmap('wxART_DELETE',
              wx.ART_TOOLBAR, wx.DefaultSize), id=wxID_FRMMAINCMDREMOVE,
              name=u'cmdRemove', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=wx.BU_AUTODRAW)
        self.cmdRemove.Bind(wx.EVT_BUTTON, self.OnCmdRemoveButton,
              id=wxID_FRMMAINCMDREMOVE)

        self._init_sizers()

    def __init__(self):
        self._init_ctrls(None)
        Observer.__init__(self)
        self.SetTitle(Settings.APP_NAME)
        
        iconBundle = wx.IconBundle()
        iconBundle.AddIcon(wx.ArtProvider_GetIcon("PFS_ICON_32", wx.ART_OTHER))
        iconBundle.AddIcon(wx.ArtProvider_GetIcon("PFS_ICON_48", wx.ART_OTHER))
        self.SetIcons(iconBundle)
        
        self.statusBar = wx.StatusBar(self)
        self.statusBar.SetFieldsCount(3)
        self.SetStatusBar(self.statusBar)
        
        self.actionManager = ActionManager()
        
        menuBar = self.actionManager.GetMenuBar()
        self.SetMenuBar(menuBar)
        toolBar = self.actionManager.GetToolBar(self)
        self.SetToolBar(toolBar)

        self.Bind(wx.EVT_MENU, self.OnProjectNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnProjectLoad, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU_RANGE, self.OnProjectLoadFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        self.Bind(wx.EVT_MENU, self.OnProjectSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnProjectSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        
        self.Bind(wx.EVT_MENU, self.OnCmdMoveLeftButton, id=self.actionManager.ID_PIC_MOVE_LEFT)
        self.Bind(wx.EVT_MENU, self.OnCmdMoveRightButton, id=self.actionManager.ID_PIC_MOVE_RIGHT)
        self.Bind(wx.EVT_MENU, self.OnCmdRemoveButton, id=self.actionManager.ID_PIC_REMOVE)

        self.Bind(wx.EVT_MENU, self.pnlEditPicture.OnCmdRotateLeftButton, id=ActionManager.ID_PIC_ROTATE_CCW)
        self.Bind(wx.EVT_MENU, self.pnlEditPicture.OnCmdRotateRightButton, id=ActionManager.ID_PIC_ROTATE_CW)

        self.Bind(wx.EVT_MENU, self.OnImportPics, id=self.actionManager.ID_PIC_IMPORT)

        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=wx.ID_HELP)

        self.Bind(wx.EVT_MENU, self.OnRenderFilmstrip, id=self.actionManager.ID_RENDER_FILMSTRIP)
        
        self.Bind(EVT_RECT_CHANGED, self.OnRectChanged, id=self.bitmapLeft.GetId())
        self.Bind(EVT_RECT_CHANGED, self.OnRectChanged, id=self.bitmapRight.GetId())

        self.SetBackgroundColour(toolBar.GetBackgroundColour())
        self.SetInitialSize(self.GetEffectiveMinSize())
        
        self._imageList = wx.ImageList(64, 64)
        self.listView.AssignImageList(self._imageList, wx.IMAGE_LIST_NORMAL)
        
        self.actionManager.OnPictureSelected(False)
        self.actionManager.OnProjectChanged(False)
        self.actionManager.OnProjectReady(False)

        self.__currentProject = ""
        
        self.OnProjectNew(None)
        
    def OnClose(self, event):
        if self.__CheckAndAskSaving():
            self.Destroy()

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = Settings.APP_NAME
        info.Version = Settings.APP_VERSION
        info.Copyright = u"(C) 2008 Jens G\xf6pfert"
        info.Description = wordwrap(
            u"%s creates movies out of your pictures." % Settings.APP_NAME,
            350, wx.ClientDC(self))
        info.WebSite = (u"http://photostoryx.sourceforge.net", "%s home page" % Settings.APP_NAME)
        info.Developers = [u"Jens G\xf6pfert"]

        info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        wx.AboutBox(info)
        
    def __CheckAndAskSaving(self):
        if self.actionManager.CanSave():
            name = self.__currentProject
            if not name:
                name = _("Unnamed PhotoFilmStrip")
                
            dlg = wx.MessageDialog(self,
                                   _(u"'%s' has been modified. Save changes?") % name, 
                                   _(u"Question"),
                                   wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            response = dlg.ShowModal()
            dlg.Destroy()
            
            if response == wx.ID_CANCEL:
                return False
            elif response == wx.ID_YES and not self.OnProjectSave(None):
                return False
        return True

    def OnProjectNew(self, event):
        self.__NewProject()
        
    def __UpdateStatusText(self):
        pics = self.listView.GetPyDataList()

        imgCount = len(pics)
        self.statusBar.SetStatusText("%s: %d" % (_(u"Images"), imgCount), 1)
        
        totalTime = 0
        for pic in pics:
            totalTime += pic.GetDuration()

        minutes = totalTime / 60
        seconds = totalTime % 60
        self.statusBar.SetStatusText("%s: %02d:%02d" % (_(u"Duration"), 
                                                    minutes, 
                                                    seconds), 2)

    def __NewProject(self, askSaving=True):
        if askSaving and not self.__CheckAndAskSaving():
            return

        self._imageList.RemoveAll()
        self.listView.DeleteAllItems()
        self.bitmapLeft.SetBitmap(None)
        self.bitmapRight.SetBitmap(None)

        self.cmdMoveLeft.Enable(False)
        self.cmdMoveRight.Enable(False)
        self.cmdRemove.Enable(False)
        self.pnlEditPicture.Enable(False)

        self.actionManager.OnPictureSelected(False)
        self.actionManager.OnProjectChanged(False)
        self.actionManager.OnProjectReady(False)

        self.SetTitle(Settings.APP_NAME)
        self.__currentProject = ""
        self.__UpdateStatusText()
        
    def __LoadProject(self, filepath):
        self.__NewProject(False)
        
        self.actionManager.AddFileToHistory(filepath)
        
        photoFilmStrip = PhotoFilmStrip()
        photoFilmStrip.Load(filepath)
        pics = photoFilmStrip.GetPictures()
        
        self._InsertPictures(pics)

        self.__currentProject = filepath
        self.SetTitle(Settings.APP_NAME + ' - ' + filepath)
        self.actionManager.OnProjectChanged(False)
        self.actionManager.OnProjectReady(True)
        
        Settings().SetProjectPath(os.path.dirname(filepath))
    
    def OnProjectLoad(self, event):
        if not self.__CheckAndAskSaving():
            return

        dlg = wx.FileDialog(self, _(u"Select %s-Project") % Settings.APP_NAME, 
                            Settings().GetProjectPath(), "", 
                            Settings.APP_NAME + u'-' + _(u"Project") + " (*.pfs)|*.pfs", 
                            wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.__LoadProject(dlg.GetPath())
            
    def OnProjectLoadFileHistory(self, event):
        if not self.__CheckAndAskSaving():
            return

        fileNum = event.GetId() - wx.ID_FILE1
        path = self.actionManager.GetHistoryFile(fileNum)
        self.__LoadProject(path)
        
    def __SaveProject(self, filepath):
        pics = self.listView.GetPyDataList()
        photoFilmStrip = PhotoFilmStrip()
        photoFilmStrip.SetPictures(pics)
        photoFilmStrip.Save(filepath)
        
        self.actionManager.AddFileToHistory(filepath)
        
        self.__currentProject = filepath
        self.SetTitle(Settings.APP_NAME + ' - ' + filepath)
        self.actionManager.OnProjectChanged(False)
        return True
    
    def OnProjectSave(self, event):
        if self.__currentProject:
            return self.__SaveProject(self.__currentProject)
        else:
            return self.OnProjectSaveAs(event)

    def OnProjectSaveAs(self, event):
        dlg = wx.FileDialog(self, _(u"Save %s-Project") % Settings.APP_NAME, 
                            Settings().GetProjectPath(), 
                            "" if self.__currentProject else "photofilmstrip", 
                            Settings.APP_NAME + u'-' + _(u"Project") + " (*.pfs)|*.pfs", 
                            wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            if os.path.splitext(filepath)[1].lower() != ".pfs":
                filepath += ".pfs"
            return self.__SaveProject(filepath)
        return False

    def OnRenderFilmstrip(self, event):
        photoFilmStrip = PhotoFilmStrip()
        photoFilmStrip.SetPictures(self.listView.GetPyDataList())
        dlg = DlgRender(self, photoFilmStrip)
        dlg.ShowModal()
        dlg.Destroy()

    def OnImportPics(self, event):
        dlg = wx.FileDialog(self, _(u"Import images"), 
                            Settings().GetImagePath(), "", 
                            _(u"Imagefiles") + " (*.*)|*.*", 
                            wx.OPEN | wx.FD_MULTIPLE | wx.FD_PREVIEW)
        if dlg.ShowModal() == wx.ID_OK:
            pics = []
            for path in dlg.GetPaths():
                pic = Picture(path)
                pics.append(pic)
            
            self._InsertPictures(pics)
            self.actionManager.OnProjectChanged(True)
            
            Settings().SetImagePath(os.path.dirname(path))

    def OnListViewListItemSelected(self, event):
        item = event.GetIndex()
        if item == 0:
            kind = 'first'
        elif item == self.listView.GetItemCount() - 1:
            kind = 'last'
        else:
            kind = 'any'
        self.cmdMoveLeft.Enable(item > 0)
        self.cmdMoveRight.Enable(item < self.listView.GetItemCount() - 1)
        self.cmdRemove.Enable(True)
        
        pic = self.listView.GetPyData(item)
        bmp = pic.GetBitmap()
        self.bitmapLeft.SetBitmap(bmp)
        self.bitmapLeft.SetSection(pic.GetStartRect())
        self.bitmapRight.SetBitmap(bmp)
        self.bitmapRight.SetSection(pic.GetTargetRect())

        self.pnlEditPicture.SetPicture(pic)
        
        self.actionManager.OnPictureSelected(True, kind)
        event.Skip()

    def OnListViewListItemDeselected(self, event):
        item = event.GetIndex()
        
        self.cmdMoveLeft.Enable(False)
        self.cmdMoveRight.Enable(False)
        self.cmdRemove.Enable(False)
        self.actionManager.OnPictureSelected(False)

    def OnRectChanged(self, event):
        selItem = self.listView.GetFirstSelected()
        pic = self.listView.GetPyData(selItem)
        if event.GetEventObject() is self.bitmapLeft:
            pic.SetStartRect(self.bitmapLeft.GetSection())
        else:
            pic.SetTargetRect(self.bitmapRight.GetSection())

    def _InsertPictures(self, pics):
        count = self.listView.GetItemCount()
        for idx, pic in enumerate(pics):
            path = pic.GetFilename()
            imgIdx = self._imageList.AddWithColourMask(pic.GetScaledBitmap(64, 64), wx.CYAN)
            itm = self.listView.InsertStringItem(sys.maxint, 
                                                 os.path.basename(path))
            self.listView.SetItemPosition(itm, wx.Point((idx + count) * 80, 10))
            self.listView.SetItemImage(itm, imgIdx)
            self.listView.SetPyData(itm, pic)

            pic.AddObserver(self)
        
        if self.listView.GetSelectedItemCount() == 0:
            self.listView.Select(0)
        
        self.__UpdateStatusText()
        self.actionManager.OnProjectReady(self.listView.GetItemCount() > 0)
        self.actionManager.OnProjectChanged(True)

    def OnCmdMoveLeftButton(self, event):
        selItem = self.listView.GetFirstSelected()
        pic = self.listView.GetPyData(selItem)
        
        self.listView.DeleteItem(selItem)
        imgIdx = self._imageList.AddWithColourMask(pic.GetScaledBitmap(64, 64), wx.CYAN)
        itm = self.listView.InsertStringItem(selItem - 1, 
                                             os.path.basename(pic.GetFilename()))
        self.listView.SetItemImage(itm, imgIdx)
        
        self.listView.SetPyData(itm, pic)
        self.listView.Select(itm)
        
        self.actionManager.OnProjectChanged(True)

    def OnCmdMoveRightButton(self, event):
        selItem = self.listView.GetFirstSelected()
        pic = self.listView.GetPyData(selItem)
        
        self.listView.DeleteItem(selItem)
        imgIdx = self._imageList.AddWithColourMask(pic.GetScaledBitmap(64, 64), wx.CYAN)
        itm = self.listView.InsertStringItem(selItem + 1, 
                                             os.path.basename(pic.GetFilename()))
        self.listView.SetItemImage(itm, imgIdx)
        self.listView.SetPyData(itm, pic)
        self.listView.Select(itm)
        
        self.actionManager.OnProjectChanged(True)

    def OnCmdRemoveButton(self, event):
        selItem = self.listView.GetFirstSelected()
        self.listView.DeleteItem(selItem)
        
        if selItem > self.listView.GetItemCount() - 1:
            selItem = self.listView.GetItemCount() - 1
        self.listView.Select(selItem)
        
        if self.listView.GetItemCount() == 0:
            self.pnlEditPicture.SetPicture(None)
        
        self.__UpdateStatusText()
        self.cmdRemove.Enable(self.listView.GetItemCount() > 0)
        self.actionManager.OnPictureSelected(self.listView.GetSelectedItemCount() > 0)
        self.actionManager.OnProjectChanged(True)
        self.actionManager.OnProjectReady(self.listView.GetItemCount() > 0)

    def ObservableUpdate(self, obj, arg):
        if isinstance(obj, Picture):
            if arg == 'bitmap':
                bmp = obj.GetBitmap()
                self.bitmapLeft.SetBitmap(bmp)
                self.bitmapRight.SetBitmap(bmp)
                imgIdx = self._imageList.AddWithColourMask(obj.GetScaledBitmap(64, 64), wx.CYAN)
                item = self.listView.FindItemPyData(obj)
                self.listView.SetItemImage(item, imgIdx)
            
            if arg == 'duration':
                self.__UpdateStatusText()
             
            self.actionManager.OnProjectChanged(True)

    def OnHelp(self, event):
        wx.MessageBox(_(u"Help will be available soon."), _(u"Information"))
