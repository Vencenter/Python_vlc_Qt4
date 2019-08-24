# -*- coding: utf-8 -*-
import sys,time
import os.path
import vlc
import pafy
from PyQt4 import  QtGui 
from PyQt4 import  QtGui as QtWidgets
from PyQt4 import  QtCore

reload(sys)
sys.setdefaultencoding("utf-8")
All_list=[]
Format="avimp4mkvtsflv"

class Player_list(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(Player_list,self).__init__(parent=None)
        self._parent=parent
        self.setWindowTitle(u'播放列表')
        self.setViewMode(QtGui.QListView.IconMode)
        self.setIconSize(QtCore.QSize(100, 40))  #Icon 大小
        self.setMaximumWidth(300)  # 最大宽度
        self.setMinimumWidth(200)
        self.setSpacing(2)  # 间距大小
        self.setAcceptDrops(True)

    def mouseDoubleClickEvent(self,event):
        #print str(self.currentItem().text())
        #print str(self.currentItem().path).decode("utf-8")
        
        self._parent.start(str(self.currentItem().path))
        
    def dragEnterEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()
    def dragMoveEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()

    def dropEvent( self, event ):
            global All_list
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                filepath = str(urls[0].path())[1:]
                filename=str(filepath.split("/")[-1])

                if All_list!=[]:
                    for i in All_list:
                        if filename in i:
                            return
                filename=filename.decode("utf-8")
                if(filename.split(".")[-1] in Format):
                    self.item = QtGui.QListWidgetItem(self)
                    self.item.path=filepath
                    self.item.setIcon(QtGui.QIcon('tu.png'))
                    self.item.setText(filename)
                    self.item.setSizeHint(self.sizeHint()/2.2)
                    self.item.setBackground(QtWidgets.QColor('gray'))
                    self.item.setTextAlignment(QtCore.Qt.AlignHCenter)
                    self.item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                    self.addItem(self.item)

                    All_list.append(filepath)
                
                
                
    

class graphicsView(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(graphicsView,self).__init__(parent)
        self._parent=parent
        self.resize(400,200)
        self.setWindowTitle(u"User-Agent")
        self.initUI()
    def initUI(self):

        self.headers=""
        
        Agent=QtWidgets.QLabel(u'address：')
        self.Agent_address=QtWidgets.QLineEdit("")

        

        set_button=QtWidgets.QPushButton(u"播放")

        close_button=QtWidgets.QPushButton(u"返回")


        laty_1=QtWidgets.QFormLayout()
        laty_1.addWidget(Agent)
        laty_1.addWidget(self.Agent_address)
  

        laty_3=QtWidgets.QHBoxLayout()
        laty_3.addStretch(10)
        laty_3.addSpacing(10)
        laty_3.addWidget(set_button)
        laty_3.addWidget(close_button)

        

        
        all_lay=QtWidgets.QVBoxLayout()
        all_lay.addLayout(laty_1)
        all_lay.addLayout(laty_3)



        self.setLayout(all_lay)

        set_button.clicked.connect(self.set_data)
        close_button.clicked.connect(self.close)

        self.resize(320,120)
        
    def set_data( self ):
        self.headers=str(self.Agent_address.text())
        self.close()

class Player(QtWidgets.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setWindowTitle("Video Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.mediaplayer1 = self.instance.media_player_new()

        self._exr=0

        self._address=graphicsView(self)

        self._list=Player_list(self)

        self.createUI()
        self.isPaused = False

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)

        front_tool_button = QtWidgets.QToolButton()
        front_tool_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        front_tool_button.setToolTip(u'上一个')
        #front_tool_button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        #front_tool_button.setText('')
        front_tool_button.setIcon(QtWidgets.QIcon('cache/front.jpeg'))
        front_tool_button.setAutoRaise(True)

        self.play_tool_button = QtWidgets.QToolButton()
        self.play_tool_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.play_tool_button.setToolTip(u'播放')
        #front_tool_button.setText('')
        self.play_tool_button.setIcon(QtWidgets.QIcon('cache/play.jpeg'))
        self.play_tool_button.setAutoRaise(True)

       


        random_tool_button = QtWidgets.QToolButton()
        random_tool_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        random_tool_button.setToolTip(u'网络')

        #front_tool_button.setText('')
        random_tool_button.setIcon(QtWidgets.QIcon('cache/random.jpeg'))
        random_tool_button.setAutoRaise(True)

        next_tool_button = QtWidgets.QToolButton()
        next_tool_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        next_tool_button.setToolTip(u'下一个')
        #front_tool_button.setText('')
        next_tool_button.setIcon(QtWidgets.QIcon('cache/next.jpeg'))
        next_tool_button.setAutoRaise(True)

        stop_tool_button = QtWidgets.QToolButton()
        stop_tool_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        stop_tool_button.setToolTip(u'停止')
        #front_tool_button.setText('')
        stop_tool_button.setIcon(QtWidgets.QIcon('cache/stop.jpeg'))
        stop_tool_button.setAutoRaise(True)

        self.videoframe = QtWidgets.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)


        
        self.playbutton = QtWidgets.QPushButton("Play")
        self.stopbutton = QtWidgets.QPushButton("Stop")
        
        self.start_time_label= QtWidgets.QLabel("00:00:00")
        self.positionslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("time")
        self.positionslider.setMaximum(1000)
        self.end_time_label= QtWidgets.QLabel("--")



        self.volume_label= QtWidgets.QLabel(u"声音")
        self.volumeslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")


        mainSplitter=QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        mainSplitter.setOpaqueResize(1)
        mainSplitter.addWidget(self.videoframe)
        mainSplitter.addWidget(self._list)
        mainSplitter.setStretchFactor(1,10)
        mainSplitter.setStretchFactor(1,2)



        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.hbuttonbox.addWidget(front_tool_button)
        self.hbuttonbox.addWidget(self.play_tool_button)
        self.hbuttonbox.addWidget(random_tool_button)
        self.hbuttonbox.addWidget(next_tool_button)
        self.hbuttonbox.addWidget(stop_tool_button)
        self.hbuttonbox.addStretch(1)
        self.hbuttonbox.addWidget(self.volume_label)
        self.hbuttonbox.addWidget(self.volumeslider)


        self.Hboxpos = QtWidgets.QHBoxLayout()
        self.Hboxpos.addWidget(self.start_time_label,1)      
        self.Hboxpos.addWidget(self.positionslider,13)
        self.Hboxpos.addWidget(self.end_time_label,1)      
        

        self.Vbox = QtWidgets.QVBoxLayout()
        self.Vbox.addWidget(mainSplitter,10)
        self.Vbox.addLayout(self.Hboxpos,1)
        self.Vbox.addLayout(self.hbuttonbox,1)


        self.Hbox = QtWidgets.QHBoxLayout()
        self.Hbox.addLayout(self.Vbox)

        

        self.widget.setLayout(self.Hbox)



        self.positionslider.sliderMoved.connect(self.setPosition)
        self.play_tool_button.clicked.connect(self.changestatus)
        stop_tool_button.clicked.connect(self.Stop)
        self.volumeslider.valueChanged.connect(self.setVolume)

        front_tool_button.clicked.connect(self.front_video)
        next_tool_button.clicked.connect(self.next_video)

        random_tool_button.clicked.connect(self.network)


        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateUI)

        self.setGeometry(400,150,500,680)
        
    def front_video(self):
        now= self._list.selectedIndexes()[0].row()
        Max=self._list.count()
        
        if (now-1) >=0:
            filename=All_list[now-1]
            if not filename:
                return
            self._list.setCurrentRow(now-1)
            if sys.version < '3':
                filename = unicode(filename)
                
            self.media = self.instance.media_new(filename)
            self.mediaplayer.set_media(self.media)

            #print dir(self.mediaplayer)
            
            #self.end_time_label.setText("11")

            self.media.parse()
            self.setWindowTitle(self.media.get_meta(0))
            if sys.platform.startswith('linux'): # for Linux using the X Server
                self.mediaplayer.set_xwindow(self.videoframe.winId())
            elif sys.platform == "win32": # for Windows
                self.mediaplayer.set_hwnd(self.videoframe.winId())
            elif sys.platform == "darwin": # for MacOS
                self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
            self.PlayPause()


    def next_video(self):
        now= self._list.selectedIndexes()[0].row()
        Max=self._list.count()

        if (now+1) <Max:
            filename=All_list[now+1]
            if not filename:
                return
            self._list.setCurrentRow(now+1)
            if sys.version < '3':
                filename = unicode(filename)
                
            self.media = self.instance.media_new(filename)
            self.mediaplayer.set_media(self.media)

            #print dir(self.mediaplayer)
            
            #self.end_time_label.setText("11")

            self.media.parse()
            self.setWindowTitle(self.media.get_meta(0))
            if sys.platform.startswith('linux'): # for Linux using the X Server
                self.mediaplayer.set_xwindow(self.videoframe.winId())
            elif sys.platform == "win32": # for Windows
                self.mediaplayer.set_hwnd(self.videoframe.winId())
            elif sys.platform == "darwin": # for MacOS
                self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
            self.PlayPause()

            
    def changestatus(self):
        if self._exr==0:
            self.play_tool_button.setToolTip(u'暂停')
            self.play_tool_button.setIcon(QtWidgets.QIcon('cache/pause.jpg'))
            self.play_tool_button.setAutoRaise(True)
            self._exr=1
            self.mediaplayer.pause()
            #print dir(self.mediaplayer)
        else:
            self.play_tool_button.setToolTip(u'播放')
            self.play_tool_button.setIcon(QtWidgets.QIcon('cache/play.jpeg'))
            self.play_tool_button.setAutoRaise(True)
            self._exr=0
            self.mediaplayer.play()

    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        self.mediaplayer.stop()
        self.playbutton.setText("Play")
    def network(self):
        self._address.show()
        
        if not (self._address.exec_()):
            filename=str(self._address.Agent_address.text())
            filename = unicode(filename)
            if filename!="":
                if "youtube" in filename:
                    video = pafy.new(filename)
                    best = video.getbestvideo()
                    self.mediaplayer.set_mrl(best.url)
                    best1 = video.getbestaudio() 
                    self.mediaplayer1.set_mrl(best1.url)


                    if sys.platform.startswith('linux'):
                        self.mediaplayer.set_xwindow(self.videoframe.winId())
                    elif sys.platform == "win32":
                        self.mediaplayer.set_hwnd(self.videoframe.winId())
                    elif sys.platform == "darwin":
                        self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

                    self.mediaplayer.play()
                    self.mediaplayer1.play()
                else:
               
                    self.mediaplayer.set_mrl(filename)

                    if sys.platform.startswith('linux'):
                        self.mediaplayer.set_xwindow(self.videoframe.winId())
                    elif sys.platform == "win32":
                        self.mediaplayer.set_hwnd(self.videoframe.winId())
                    elif sys.platform == "darwin":
                        self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

                    self.mediaplayer.play()
           

  
            
                
        

        


    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None or filename is False:
            print("Attempt to openup OpenFile")
            filenameraw = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
            filename = filenameraw
        #print filename 
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
        self.PlayPause()
    def start(self, filename=None):
        file_name=filename.replace(u"\u301c", u" ")
        file_name=file_name.replace(u"\u3099", u" ")
        filename =filename.decode("utf-8")

        
        #print file_name

        
        if not filename:
            return

        if sys.version < '3':
            filename = unicode(filename)
            
        self.media = self.instance.media_new(filename)
        self.mediaplayer.set_media(self.media)

        #print dir(self.mediaplayer)
        
        #self.end_time_label.setText("11")

        self.media.parse()
        self.setWindowTitle(self.media.get_meta(0))
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
        self.PlayPause()

        
    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        #print self.mediaplayer.get_position() * 1000
        #print self.mediaplayer.get_length()/1000
        seconds =self.mediaplayer.get_length()/1000
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        sec=("%02d:%02d:%02d" % (h, m, s))
        self.end_time_label.setText(sec) 

        self.positionslider.setToolTip((str(int(self.mediaplayer.get_position() * 1000)))+"s")
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)
     
        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())
