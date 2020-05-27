import time
import math
import subprocess
from subprocess import check_output , CalledProcessError

class XDoToolWrapper:

	def __init__( self , options={} ):
		self.options = options
		self.window_id = False
		self.window_geometry = False

	def sleep( self , milliseconds ):
		time.sleep( milliseconds )

	def exec( self , bash_command ):
		return subprocess.getoutput( bash_command )

	def get_monitors( self ):
		result = self.exec( "xrandr --prop | grep connected" )
		result = result.split("\n")
		monitors = {}
		for line_index , line in enumerate( result ):
			line_items = line.split( " " )
			if len( line_items ) < 3:
				continue
			if line_items[ 1 ] == "connected":
				size = line_items[3].split( "x" )
				size_x = size[ 0 ]
				size_y = size[ 1 ].split( "+" )[ 0 ]
				monitors[ line_items[ 2 ] ] = {
					"name": line_items[ 0 ] ,
					"size": {
						"x": size_x ,
						"y": size_y ,
					}
				}
		self.monitors = monitors

	def attach_via_name( self , window_name , number_of_tries=10 , sleep_time=1 ):
		for i in range( 1 , number_of_tries ):
			window_id = self.exec( f"xdotool search --desktop 0 --name '{window_name}'" )
			window_id = window_id.split( "\n" )
			window_id = window_id[ 0 ]
			if window_id.isdigit() == True:
				self.window_id = window_id
				return True
			else:
				time.sleep( sleep_time )
		return False

	def activate_window( self ):
		if self.window_id == False:
			return
		self.exec( f"xdotool windowactivate {self.window_id}" )

	def focus_window( self ):
		if self.window_id == False:
			return
		self.exec( f"xdotool windowfocus {self.window_id}" )

	def refocus_window( self ):
		if self.window_id == False:
			return
		self.activate_window()
		self.sleep( .3 )
		self.focus_window()
		self.sleep( .3 )

	def raise_window( self ):
		if self.window_id == False:
			return
		self.exec( f"xdotool windowraise {self.window_id}" )

	def get_window_geometry( self ):
		if self.window_id == False:
			return
		try:
			self.refocus_window()
			result = self.exec( f"xdotool getactivewindow getwindowgeometry" )
			lines = result.split( "\n" )
			geometry = lines[ -1 ].split( "Geometry: " )[ 1 ].split( "x" )
			geometry_x = geometry[ 0 ]
			geometry_y = geometry[ 1 ]
			center_x = math.floor( ( geometry_x / 2 ) )
			center_y = math.floor( ( geometry_y / 2 ) )
			self.window_geometry = {
				"x": geometry_x ,
				"y": geometry_y ,
				"center": {
					"x": center_x ,
					"y": center_y ,
				}
			}
			print( self.window_geometry )
		except Exception as e:
			print( e )
			return False

	def unmaximize_window( self ):
		if self.window_id == False:
			return
		self.refocus_window()
		self.exec( f"wmctrl -rf {self.window_id} -b remove,maximized_ver,maximized_horz" )

	def maximize_window( self ):
		if self.window_id == False:
			return
		self.refocus_window()
		self.exec( f"xdotool key F11" )

	def maximize_window( self ):
		self.maximize_window()

	def move_mouse( self , x=0 , y=0 ):
		if self.window_id == False:
			return
		self.refocus_window()
		self.exec( f"xdotool mousemove {x} {y}" )

	def left_click( self ):
		if self.window_id == False:
			return
		self.refocus_window()
		self.exec( f"xdotool click 1" )

	def right_click( self ):
		if self.window_id == False:
			return
		self.refocus_window()
		self.exec( f"xdotool click 2" )

	def double_click( self ):
		if self.window_id == False:
			return
		self.refocus_window()
		self.exec( f"xdotool click --repeat 2 --delay 200 1" )

	def center_mouse( self ):
		if self.window_id == False:
			return
		if self.window_geometry == False:
			return
		self.move_mouse( self.window_geometry["center"][ "x" ] , self.window_geometry["center"][ "y" ] )

	def press_keyboard_key( self , keyboard_key ):
		if self.window_id == False:
			return
		self.refocus_window()
		self.exec( f"xdotool key '{keyboard_key}'" )


if __name__ == '__main__':
	xdotool = XDoToolWrapper()
	xdotool.get_monitors()
	xdotool.attach_via_name( "Chrome" )
	xdotool.get_window_geometry()