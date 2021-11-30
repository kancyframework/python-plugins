# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class BaseMainFrame
###########################################################################

class BaseMainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"钉钉机器人", pos = wx.DefaultPosition, size = wx.Size( 560,354 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		wSizer1 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText = wx.StaticText( self, wx.ID_ANY, u"机器人", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText.Wrap( -1 )

		self.m_staticText.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		wSizer1.Add( self.m_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		dingTalkClientsChoices = []
		self.dingTalkClients = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,-1 ), dingTalkClientsChoices, 0 )
		self.dingTalkClients.SetSelection( 0 )
		wSizer1.Add( self.dingTalkClients, 1, wx.ALL|wx.EXPAND, 5 )

		self.sendButton = wx.Button( self, wx.ID_ANY, u"发送", wx.DefaultPosition, wx.DefaultSize, 0 )
		wSizer1.Add( self.sendButton, 0, wx.ALL, 5 )


		bSizer1.Add( wSizer1, 0, 0, 5 )

		self.messageText = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer1.Add( self.messageText, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.sendButton.Bind( wx.EVT_BUTTON, self.sendDingMessage )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def sendDingMessage( self, event ):
		event.Skip()


