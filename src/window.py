# window.py
#
# Copyright 2018 Francisco Jose Quiñones Enciso
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gdk
from gi.repository import Gst
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Gnome-Streaming-Player/window.ui')
class GnomeStreamingPlayerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GnomeStreamingPlayerWindow'
    #the variable channels should be a json file in a home directory.. in a future version
    channels = [{ "id":1,"enabled": True,
		            "name":"TV Online",
		            "type":"menu",
		            "data":[
			            {
				            "id": 1,
				            "enabled": True,
				            "name": "TV Peru HD",
				            "link_source": "http://cdnh4.iblups.com/hls/R9WtilpKKB.m3u8",
				            "link_logo": ""
			            },
			            {
				            "id": 2,
				            "enabled": True,
				            "name": "TV Peru 7.3",
				            "link_source": "http://cdnh4.iblups.com/hls/RMuwrdk7M9.m3u8",
				            "link_logo": ""
			            },
			            {
				            "id": 3,
				            "enabled": True,
				            "name": "Panamericana Televisión",
				            "link_source": "http://cdnh4.iblups.com/hls/ptv2.m3u8",
				            "link_logo": ""
			            },
			            {
				            "id": 4,
				            "enabled": True,
				            "name": "Real Madrid TV",
				            "link_source": "http://rmtv24hweblive-lh.akamaihd.net/i/rmtv24hwebes_1@300661/master.m3u8",
				            "link_logo": ""
			            }
		            ]
	            },
	            {
		            "id":2,
		            "enabled": True,
		            "name":"Camera Home - Pruebas camara hikvision",
		            "type":"menu",
		            "data":[
			            {
				            "id": 1,
				            "enabled": True,
				            "name": "Camera 1",
				            "link_source": "rtsp://admin:Hik12345@192.168.1.40:554/h264/ch1/main/av_stream",
				            "link_logo": ""
			            },
			            {
				            "id": 2,
				            "enabled": True,
				            "name": "Camera 2",
				            "link_source": "rtsp://admin:Hik12345@192.168.1.40:554/h264/ch2/main/av_stream",
				            "link_logo": ""
			            },
			            {
				            "id": 3,
				            "enabled": True,
				            "name": "Camera 3",
				            "link_source": "rtsp://admin:Hik12345@192.168.1.40:554/h264/ch3/main/av_stream",
				            "link_logo": ""
			            },
			            {
				            "id": 4,
				            "enabled": True,
				            "name": "Camera 4",
				            "link_source": "rtsp://admin:Hik12345@192.168.1.40:554/h264/ch4/main/av_stream",
				            "link_logo": ""
			            }
		            ]
	            }
            ]
    header_bar,tree_sources, btn_play_pause,btn_fullscreen,box_player = GtkTemplate.Child.widgets(5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.playing = False
        store = Gtk.TreeStore(str, str)
        for i in range(len(self.channels)):
            piter = store.append(None, [self.channels[i]["name"], self.channels[i]["type"]])
            print(piter)
            sublevel = self.channels[i]["data"]
            j = 0
            while j < len(sublevel):
                print(sublevel[j]["name"])
                store.append(piter, [sublevel[j]["name"],sublevel[j]["link_source"]])
                j += 1
        renderer_books = Gtk.CellRendererText()
        column_books = Gtk.TreeViewColumn("Sources", renderer_books, text=0)
        self.tree_sources.connect("button_press_event", self.mouse_click)
        self.tree_sources.append_column(column_books)
        self.tree_sources.set_model(store)
        self.create_pipeline()

    def create_pipeline(self):
        Gst.init(None)
        Gst.debug_set_active(True)
        self.source = Gst.ElementFactory.make("playbin", "player")
        self.sink  = Gst.ElementFactory.make("gtksink", "fakesink")
        self.source.set_property("video-sink", self.sink)
        self.viewer = self.sink.get_property("widget")
        self.box_player.pack_start(self.viewer, True, True, 0)
        #self.box_player.reorder_child(viewer, 0)
        self.viewer.show()
    def _onPlayPause(self,play_pause_button):
        if self.playing :
            self.onPause()
        else:
            self.onPlay()


    def onPlay(self):
        if self.playing:
            self.source.set_state(Gst.State.READY)
        self.playing = True
        self.source.set_property("uri", self.uri)
        self.source.set_state(Gst.State.PLAYING)
        img = Gtk.Image.new_from_stock(Gtk.STOCK_MEDIA_PAUSE,Gtk.IconSize.BUTTON)
        self.btn_play_pause.set_image(img)

    def onPause(self):
        self.playing  = False
        self.source.set_state(Gst.State.READY)
        img = Gtk.Image.new_from_stock(Gtk.STOCK_MEDIA_PLAY,Gtk.IconSize.BUTTON)
        self.btn_play_pause.set_image(img)

    def _onFullscreen(self,btn_full_screen):
        #not implement yet
        pass


    def mouse_click(self, tv, event):
        if event.button == 1:
            data = self.tree_sources.get_path_at_pos(int(event.x), int(event.y))
            if data :
                if event.type == Gdk.EventType._2BUTTON_PRESS :
                    selection = self.tree_sources.get_selection()
                    (model, iter) = selection.get_selected()
                    if (model[iter][1]!="menu"):
                        self.uri = model[iter][1]
                        self.header_bar.set_title(model[iter][0])
                        self.onPlay()
                        print(model[iter][1])

