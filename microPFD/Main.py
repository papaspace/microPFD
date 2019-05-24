# Copyright (C) Michael Braunstingl, 2018 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited

import console
import motion
import location
import scene
import numpy
import navutil
import symbolgen as sg

font_14=("Helvetica",14)
font_24=("Helvetica",24)

font_lbl=font_14
color_lbl="#00ff00"

class PFD(scene.Scene):
	def __init__(self):
		self.isInit=False
		console.set_idle_timer_disabled(True)
		super(PFD,self).__init__()
		
	
	def setup(self):
		color_gps="#2299ff"
		self.background_color="#161616"
		
		self.scrw=numpy.min([440,self.size.w])
		self.scrh=self.size.h/self.size.w*self.scrw
		self.scale=self.size.h/self.scrh
		
		
		self.adiCenter=[self.scrw/2.0, self.scrh-155]
		self.pxPerDeg=10
		
		self.hdg_mode=True
		self.dtk=0.0
		self.yaw_history=list()
		
		ADI=scene.Node(parent=self)
		ADI.position=self.adiCenter
		
		# Attitude pitch marks
		#self.pitchMarks=scene.SpriteNode("IMG_2130.JPG")
		
		self.pitchMarks=sg.adi_pitchBars(self.pxPerDeg)
		ADI.add_child(self.pitchMarks)
		self.rollPointer=sg.adi_rollPointer(150)
		ADI.add_child(self.rollPointer)
		self.yawPointer=sg.adi_yawPointer(150)
		ADI.add_child(self.yawPointer)
		
		ADI.add_child(sg.adi_ac())
		ADI.add_child(sg.adi_rollMarks(150))
		
		
		# Location labels
		locationNode=scene.ShapeNode(scene.ui.Path.rect(0,0,200,48))
		locationNode.anchor_point=[0.0,0.99]
		locationNode.position=[0.0,self.scrh]
		locationNode.fill_color="#000000"
		
		h=24
		self.lbl_lat=scene.LabelNode("%3.3f"%0)
		self.lbl_lat.position=[0,0]
		self.lbl_lat.anchor_point=[0,1.0]
		self.lbl_lat.color=color_gps
		locationNode.add_child(self.lbl_lat)
		self.lbl_lon=scene.LabelNode("%3.3f"%0)
		self.lbl_lon.position=[0,-h]
		self.lbl_lon.anchor_point=[0,1.0]
		self.lbl_lon.color=color_gps
		locationNode.add_child(self.lbl_lon)
		
		adi_height=280
		hsi_height=self.scrh-adi_height
		altNode=scene.ShapeNode(scene.ui.Path.rect(0,0,self.scrw+1,self.scrh-adi_height), "#000000", parent=self)
		altNode.anchor_point=(0.0,0.0)
		altNode.position=[-1.0,-1.0]
		
		
		
		# Alt label
		[alt_symbol,self.txt_alth,self.txt_altd]=sg.alt_display(ADI)
		alt_symbol.position=[self.scrw/2,0.0]
	
		# GS label
		[gs_symbol,self.txt_spd]=sg.gs_display(ADI)
		gs_symbol.position=[-self.scrw/2,0.0]
		
		# HSI
		self.cdi_r=180.0
		[self.rose]=sg.compass_rose(altNode,self.cdi_r)
		self.rose.position=[self.scrw/2,self.scrh-adi_height-self.cdi_r-32]
		
		[self.cdi_needle,self.cdi_track]=sg.cdi(self.cdi_r)
		
		[ac]=sg.ac_symbol(altNode)
		ac.position=[self.scrw/2,self.scrh-adi_height-self.cdi_r-32]
		
		# Heading label
		h=30
		[self.hdg_symbol,self.txt_hdg]=sg.hdg_display(altNode,h)
		self.hdg_symbol.position=[self.scrw/2,hsi_height+10]
		
		
		# Waypoint info display
		[self.wpt_dsp,self.wpt_name,self.wpt_dtk,self.wpt_dist]=sg.wpt_display(altNode)
		self.wpt_dsp.position=[0,hsi_height]
		
		self.wpt=""
		self.scratchpad=sg.scratchpad(self,self.scrw,128)
		
		# G meter
		[g_symbol,self.txt_g]=sg.g_display(ADI)
		g_symbol.position=[self.scrw/2,-adi_height/3]
		
		location.start_updates()
		motion.start_updates()
		
		self.isInit=True
		print(self.pitchMarks)
		print("PFD initialized")
		
	def update(self):
		if not self.isInit:
			print("Waiting for init")
			return
		
		
		GRAV=motion.get_gravity()
		#GRAV=numpy.add(motion.get_gravity(), motion.get_user_acceleration())
		
		GRAV=GRAV/numpy.linalg.norm(GRAV)
		FORCE=motion.get_user_acceleration()
		ATT=motion.get_attitude()
		LOC=location.get_location()
		MAG=motion.get_magnetic_field()
	  
		[roll,pitch,yaw,hdg]=navutil.roll_pitch_yaw_hdg(ATT,MAG,GRAV,FORCE)
		
		# Pitch and roll pointer
		self.pitchMarks.rotation=roll
		offsetY=self.pxPerDeg*(numpy.rad2deg(pitch))
		#offsetX=-numpy.tan(roll)*offsetY
		offsetX=-numpy.sin(roll)*offsetY
		self.pitchMarks.position=(offsetX, offsetY*numpy.cos(roll))
		
		self.rollPointer.rotation=roll
		
		# Yaw pointer (ball) ...
		# smooth the signal a little
		self.yaw_history.append(yaw)
		if len(self.yaw_history)>5:
			self.yaw_history.pop(0)
		self.yawPointer.rotation=roll-numpy.mean(self.yaw_history)
		
		#print("%d %d %d"%(numpy.rad2deg(ATT[0]), numpy.rad2deg(ATT[1]),numpy.rad2deg(ATT[2])))
	 
		if LOC!=None:
			self.lbl_lat.text="LAT %2.6f deg"%LOC["latitude"]
	
			self.lbl_lon.text="LON %2.6f deg"%LOC["longitude"]
			
			# Altitude display...
			# hundreds
			self.txt_alth.text="%01d"%((LOC["altitude"]/0.3048)/100.0)
			# decis
			self.txt_altd.text="%02d"%((LOC["altitude"]/0.3048)%100.0)
			
			# Ground speed display
			gs=LOC["speed"]*3.6/1.852
			if gs<0.0:
				self.txt_spd.text="--"
			else:
				self.txt_spd.text="%d"%gs
			
			self.pos_geo=[LOC["altitude"],numpy.deg2rad(LOC["longitude"]),numpy.deg2rad(LOC["latitude"])]
			self.pos_cart=navutil.geo2cart(self.pos_geo)
			
		# HSI...
		self.txt_g.text="%2.1f"%(numpy.linalg.norm(GRAV+FORCE))
		
		# HDG display
		if self.hdg_mode==False:
			hdg=LOC["course"]
			self.txt_hdg.color="#ff00ff"
		else:
			self.txt_hdg.color="#00ff00"
		if hdg<0.0:
			self.txt_hdg.text="TRK"
			self.txt_hdg.color="#ff0000"
			hdg=0.0
			
		else:
			self.txt_hdg.text="%03d"%(hdg)
		self.rose.rotation=numpy.deg2rad(hdg)

		# Waypoint info, CDI
		if self.wpt!="":
			
			[dist,dtk]=navutil.great_circle(self.pos_cart,self.wpt_cart)
			
			fmt_dist="%d"
			if (dist/1852.0<10.0):
				fmt_dist="%0.1f"
			self.wpt_dist.text=fmt_dist%(dist/1852.0)
			self.wpt_dtk.text="%03d"%numpy.rad2deg(dtk)
			
			
			self.cdi_needle.rotation=-self.dtk
			
			full_scale_defl=12.0
			defl=numpy.amax([-full_scale_defl, numpy.amin([full_scale_defl, numpy.rad2deg((dtk-self.dtk))])])
			self.cdi_track.position=numpy.array([0.5/full_scale_defl*self.cdi_r*defl,0.0,0.0])
			#print("pos="+str(self.pos_geo))
			#print("wpt="+str(self.wpt_geo))
		
		
	def scratchpad_event(self,evt,txt):
		if evt=="ENTER":
			try:
				self.wpt=navutil.find_by_ident(txt)
				self.wpt_name.text=self.wpt.ident
				self.wpt_geo=self.wpt.geo_pos
				self.wpt_cart=navutil.geo2cart(self.wpt_geo)
				
				[self.dist,self.dtk]=navutil.great_circle(self.pos_cart,self.wpt_cart)
				self.scratchpad.symbol.remove_from_parent()
				self.rose.add_child(self.cdi_needle)
				
				
				
				print("ELEV "+str(int(self.wpt.geo_pos[0]/0.3048))+" ft, "+self.wpt.name)
			except:
				if len(txt)>0:
					print("WPT NOT FOUND: "+txt)
				else:
					print("WPT DELETED")
				self.wpt=""
				self.wpt_name.text=""
				self.wpt_dtk.text="---"
				self.wpt_dist.text="---"
				self.cdi_needle.remove_from_parent()
				self.scratchpad.symbol.remove_from_parent()
	
	def stop(self):
		location.stop_updates()
		motion.stop_updates()
		
	def touch_began(self,touch):
		s=sg.scale(self.scrw/self.size.w,self.scrh/self.size.h)
		if sg.is_touched(self.hdg_symbol,touch,s):
			self.hdg_mode=not self.hdg_mode
			
		elif sg.is_touched(self.wpt_dsp,touch,s):
			self.add_child(self.scratchpad.symbol)
		elif self.scratchpad.symbol.parent==self and sg.is_touched(self.scratchpad,touch,s):
			self.scratchpad.on_touch(touch,s)
			

		
if __name__=="__main__":
	scene.run(PFD(), scene.PORTRAIT, show_fps=False) 
