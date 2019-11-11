# Do not remove the license terms and original author:
#
# This software is licensed under CC BY-NC-SA 4.0
# (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International)
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
#
# Original author:
#   Michael Braunstingl, 2018-2019
#   m.braunstingl[at]papaspace.at

from scene import *
import numpy

color_std="#ffffff"
color_gps="#ff00ff"
font_14=("Helvetica",14)
font_24=("Helvetica",24)

font_lbl=font_14
color_lbl="#ffffff"

def adi_ac():
	path=ui.Path.rect(0,0,0,0)
	path.move_to(-60,-3)
	path.line_to(-9,-3)
	path.line_to(0,6)
	path.line_to(9,-3)
	path.line_to(60,-3)
	
	path.line_to(60,3)
	path.line_to(11,3)
	path.line_to(0,14)
	path.line_to(-11,3)
	path.line_to(-60,3)
	path.close()
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.line_width=2
		
	return symbol
	
def adi_pitchBars(pxPerDeg):
	
	font=("Helvetica", 14)
	#labels=Node()
	background=Node()
	blue=ui.Path.rect(-1.0,0.0,200.0,-100.0)
	bg_blue=ShapeNode(blue, "#002f4e","002f4e")
	bg_blue.anchor_point=[0.5,0.0]
	bg_blue.scale=180.0*pxPerDeg
	background.add_child(bg_blue)
	brown=ui.Path.rect(-1.0,0.0,2.0,10.0)
	bg_brown=ShapeNode(brown, "#3f3011","#3f3011")
	bg_brown.anchor_point=[0.5,1.0]
	bg_brown.scale=180.0*pxPerDeg
	background.add_child(bg_brown)
	
	
	for ii in numpy.linspace(-90,90,73):
		
		shape=ui.Path.rect(0,0,0,0)
		shape.line_width=1.0
		
		y=pxPerDeg*ii
		
		# 0 pitch (horizon)
		if (ii==0.0):
			shape.move_to(-300,0)
			shape.line_to(300,0)
		
		# 10deg bars
		elif (ii%10==0):
			w=70
			shape.move_to(-w,0)
			shape.line_to(w,0)
		
		# 5deg bars	
		elif (ii%5==0 and numpy.abs(ii)<30):
			shape.move_to(-30,0)
			shape.line_to(30,0)
			
	  # 2.5deg bars	
		elif (numpy.abs(ii)<30):
			shape.move_to(-20,0)
			shape.line_to(20,0)
		
		symbol=ShapeNode(shape, "#000000", color_std)
		symbol.position=(0.0,y)
		#symbol.add_child(labels)
		
		if (ii%10==0 and ii!=0):
			lbl=LabelNode("%d"%numpy.abs(ii))
			lbl.font=font
			lbl.position=(w+15,0)
			lbl.color=color_std
			symbol.add_child(lbl)
		
		background.add_child(symbol)
	
	return background
	
def adi_rollMarks(r):
	marks=Node()
	
	path=ui.Path.rect(0,0,0,0)
	path.line_width=2.0
	path.move_to(0,-r+10)
	path.line_to(5,-r)
	path.line_to(-5,-r)
	path.close()
	
	for bank in {-20,-10,10,20}:
		bank_rad=numpy.deg2rad(bank)
		path.move_to((10-r)*numpy.sin(bank_rad),
		(10-r)*numpy.cos(bank_rad))
		path.line_to((3-r)*numpy.sin(bank_rad),
		(3-r)*numpy.cos(bank_rad))
	
	for bank in {-60,-30,30,60}:
		bank_rad=numpy.deg2rad(bank)
		path.move_to((10-r)*numpy.sin(bank_rad),
		(10-r)*numpy.cos(bank_rad))
		path.line_to((-r)*numpy.sin(bank_rad),
		(-r)*numpy.cos(bank_rad))
		
	path.move_to(-r,-1)
	path.line_to(10-r,-1)
	path.line_to(10-r,2)
	path.line_to(-r,2)
	path.close()
	
	path.move_to(r,-1)
	path.line_to(r-10,-1)
	path.line_to(r-10,2)
	path.line_to(r,2)
	path.close()
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.anchor_point=(0.5,0.0)
	return symbol
	
def adi_rollPointer(r):
	path=ui.Path.rect(0,0,0,0)
	path.line_width=2.0
	path.move_to(0,-r+10)
	path.line_to(5,-r+20)
	path.line_to(-5,-r+20)
	path.close()
	
	symbol=ShapeNode(path, color_std, color_std)
	symbol.anchor_point=(0.5,0.0)
	return symbol
	

def adi_yawPointer(r):
	path=ui.Path.rect(0,0,0,0)
	path.line_width=2.0
	path.move_to(-7,-r+24)
	path.line_to(7,-r+24)
	path.line_to(6,-r+22)
	path.line_to(-6,-r+22)
	path.close()
	
	symbol=ShapeNode(path, color_std, color_std)
	symbol.anchor_point=(0.5,0.0)
	return symbol
	
	

def alt_display(parent):
	w=60
	
	path=ui.Path.rect(0,0,w,30)
	path.line_width=1.0
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.anchor_point=(1.0,0.5)
	
	parent.add_child(symbol)
	
	lbl=LabelNode("ALT")
	lbl.font=font_lbl
	lbl.position=[0,14]
	lbl.anchor_point=[1.0,0.0]
	lbl.color=color_lbl
	symbol.add_child(lbl)
	
	txt_large=LabelNode("000")
	txt_large.font=font_24
	txt_large.position=[-16,0]
	txt_large.anchor_point=[1.0,0.5]
	txt_large.color="#ff00ff"
	symbol.add_child(txt_large)
	
	txt_small=LabelNode("00")
	txt_small.font=font_14
	txt_small.position=[-2,0]
	txt_small.anchor_point=[1.0,0.5]
	txt_small.color="#ff00ff"
	symbol.add_child(txt_small)
	
	return [symbol, txt_large, txt_small]
	
	
def hdg_display(parent,h):
	w=26
	
	path=ui.Path.rect(0,0,0,0)
	path.line_width=1.0
	path.move_to(-w,-h)
	path.line_to(+w,-h)
	path.line_to(+w,0)
	path.line_to(5,0)
	path.line_to(0,5)
	path.line_to(-5,0)
	path.line_to(-w,0)
	path.close()
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.anchor_point=(0.5,1.0)
	
	parent.add_child(symbol)
	
	#lbl_hdg=LabelNode("HDG")
	#lbl_hdg.font=font_lbl
	#lbl_hdg.position=[-30,-h]
	#lbl_hdg.anchor_point=[1.0,0.0]
	#lbl_hdg.color=color_lbl
	#symbol.add_child(lbl_hdg)
	
	txt_hdg=LabelNode("000")
	txt_hdg.font=font_24
	txt_hdg.position=[0,-h]
	txt_hdg.anchor_point=[0.5,0.0]
	txt_hdg.color="#00ff00"
	symbol.add_child(txt_hdg)
	
	return [symbol, txt_hdg]


def gs_display(parent):
	w=44
	
	path=ui.Path.rect(0,0,w,30)
	path.line_width=1.0
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.anchor_point=(0.0,0.5)
	
	parent.add_child(symbol)
	
	lbl=LabelNode("GS")
	lbl.font=font_lbl
	lbl.position=[0,14]
	lbl.anchor_point=[0.0,0.0]
	lbl.color=color_lbl
	symbol.add_child(lbl)
	
	txt=LabelNode("000")
	txt.font=font_24
	txt.position=[42,0]
	txt.anchor_point=[1.0,0.5]
	txt.color="#ff00ff"
	symbol.add_child(txt)
	
	return [symbol, txt]

def g_display(parent):
	w=44
	
	path=ui.Path.rect(0,0,w,30)
	path.line_width=1.0
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.anchor_point=(1.0,0.5)
	
	parent.add_child(symbol)
	
	lbl=LabelNode("G")
	lbl.font=font_lbl
	lbl.position=[0,14]
	lbl.anchor_point=[1.0,0.0]
	lbl.color=color_lbl
	symbol.add_child(lbl)
	
	txt=LabelNode("000")
	txt.font=font_24
	txt.position=[0,0]
	txt.anchor_point=[1.0,0.5]
	txt.color="#ffffff"
	symbol.add_child(txt)
	
	return [symbol, txt]

def wpt_display(parent):
	w=80
	
	path=ui.Path.rect(0,0,w,66)
	path.line_width=0.0
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.anchor_point=(0.0,1.0)
	parent.add_child(symbol)
	
	txt_name=LabelNode("")
	txt_name.font=font_lbl
	txt_name.color=color_gps
	txt_name.position=[0,0]
	txt_name.anchor_point=[0.0,1.0]
	symbol.add_child(txt_name)
	
	lbl_dtk=LabelNode("DTK")
	lbl_dtk.font=font_lbl
	lbl_dtk.color=color_gps
	lbl_dtk.position=[0,-40]
	lbl_dtk.anchor_point=[0.0,0.0]
	symbol.add_child(lbl_dtk)
	
	txt_dtk=LabelNode("---")
	txt_dtk.font=font_24
	txt_dtk.color=color_gps
	txt_dtk.position=[w,-40]
	txt_dtk.anchor_point=[1.0,0.0]
	symbol.add_child(txt_dtk)
	
	txt_dist=LabelNode("---")
	txt_dist.font=font_24
	txt_dist.color=color_gps
	txt_dist.position=[0.0,-64]
	txt_dist.anchor_point=[0.0,0.0]
	symbol.add_child(txt_dist)
	
	lbl_dist=LabelNode("NM")
	lbl_dist.font=font_lbl
	lbl_dist.color=color_gps
	lbl_dist.position=[w,-60]
	lbl_dist.anchor_point=[1.0,0.0]
	symbol.add_child(lbl_dist)
	
	return [symbol,txt_name,txt_dtk,txt_dist]
	

def cdi(r):
	path=ui.Path.rect(0,0,0,0)
	path.line_width=3.0
	
	path.move_to(0.0,r-2.0)
	path.line_to(0.0,0.5*r)
	
	path.move_to(0.0,-0.5*r)
	path.line_to(0.0,-r+20.0)
	path.line_to(7.0,-r+20.0)
	path.line_to(0.0,-r+2.0)
	path.line_to(-7.0,-r+20.0)
	path.line_to(0.0,-r+20.0)
	
	symbol=ShapeNode(path, "#ff00ff", "#ff00ff")
	symbol.anchor_point=(0.5,0.5)
	
	# offset track needle
	path=ui.Path.rect(0,0,0,0)
	path.line_width=3.0
	
	path.move_to(0.0,0.5*r)
	path.line_to(0.0,-0.5*r)
	
	track=ShapeNode(path, "#ff00ff", "#ff00ff")
	track.anchor_point=(0.5,0.5)
	symbol.add_child(track)
	
	# offset scale
	imark=0
	mark=[0]*4
	for ii in [-1.0,-0.5,0.5,1.0]:
		mark[imark]=ShapeNode(ui.Path.oval(-2,-2,5,5),"#000000","#ffffff")
		mark[imark].position=(0.5*ii*r,0.0)
		symbol.add_child(mark[imark])
	
		imark=imark+1
	
	
	return[symbol,track]
	
	
def compass_rose(parent,r):
	
	path=ui.Path.oval(-r,-r,2*r,2*r)
	path.line_width=1.5
	
	for phi in numpy.arange(36):
		cphi=numpy.cos(numpy.deg2rad(10.0*phi))
		sphi=numpy.sin(numpy.deg2rad(10.0*phi))
		path.move_to((r+8)*sphi,(r+8)*cphi)
		path.line_to(r*sphi,r*cphi)
		
		cphi=numpy.cos(numpy.deg2rad(10.0*phi+5.0))
		sphi=numpy.sin(numpy.deg2rad(10.0*phi+5.0))
		path.move_to((r+4)*sphi,(r+4)*cphi)
		path.line_to(r*sphi,r*cphi)
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.anchor_point=(0.5,0.5)
	parent.add_child(symbol)
	
	for phi in numpy.arange(12):
		cphi=numpy.cos(numpy.deg2rad(30.0*phi))
		sphi=numpy.sin(numpy.deg2rad(30.0*phi))
		
		lbl_txt="%d"%(3.0*phi)
		if phi==0:
			lbl_txt="N"
		elif phi==3:
			lbl_txt="E"
		if phi==6:
			lbl_txt="S"
		if phi==9:
			lbl_txt="W"
			
		lbl=LabelNode(lbl_txt)
		lbl.font=font_lbl
		lbl.color="#ffffff"
		lbl.position=[(r+8)*sphi,(r+8)*cphi]
		lbl.rotation=-numpy.deg2rad(30.0*phi)
		lbl.anchor_point=[0.5,0.0]
		symbol.add_child(lbl)
		
	return [symbol]
	
def ac_symbol(parent):
		
	path=ui.Path.rect(0,0,0,0)
	path.line_width=1.5
	path.move_to(0.0,-10.0)
	path.line_to(2.0,-8.0)
	path.line_to(2.0,-2.0)
	path.line_to(10.0,3.0)
	path.line_to(10.0,6.0)
	path.line_to(2.0,2.0)
	path.line_to(2.0,7.0)
	path.line_to(6.0,9.0)
	path.line_to(6.0,11.0)
	path.line_to(0.0,10.0)
	
	path.line_to(-6.0,11.0)
	path.line_to(-6.0,9.0)
	path.line_to(-2.0,7.0)
	path.line_to(-2.0,2.0)
	path.line_to(-10.0,6.0)
	path.line_to(-10.0,3.0)
	path.line_to(-2.0,-2.0)
	path.line_to(-2.0,-8.0)
	path.line_to(-2.0,-8.0)
	path.close()
	
	symbol=ShapeNode(path, "#000000", color_std)
	symbol.anchor_point=(0.5,0.5)
	parent.add_child(symbol)

	return [symbol]
	
	
class scale:
	def __init__(self,x,y):
		self.x=x
		self.y=y


class button:
	def __init__(self,name,w,h):
		self.symbol=ShapeNode(ui.Path.rect(0,0,w,h), "#646464", "#323232")
		self.symbol.anchor_point=(0.5,0.5)
	
		self.lbl=LabelNode(name)
		self.lbl.anchor_point=(0.5,0.5)
		self.symbol.add_child(self.lbl)
		self.symbol.alpha=0.9


class bbox:
	def __init__(self,x,y,w,h):
		self.x=x
		self.y=y
		self.w=w
		self.h=h


class scratchpad:
	def __init__(self,pfd,w,h):
		self.pfd=pfd
		node=Node()
		bw=w/10
		x=bw/2.0
		
		self.bbox=bbox(0,0,w,h)
		self.buttons=list()
		
		for ii,name in enumerate(["0","1","2","3","4","5","6","7","8","9"]):
			x=(ii+0.5)*bw
			b=button(name,bw,bw)
			b.symbol.position=(x,3.5*bw)
			node.add_child(b.symbol)
			self.buttons.append(b)
		
		for ii,name in enumerate(["A","B","C","D","E","F","G","H","I","J"]):
			x=(ii+0.5)*bw
			b=button(name,bw,bw)
			b.symbol.position=(x,2.5*bw)
			node.add_child(b.symbol)
			self.buttons.append(b)
			
		for ii,name in enumerate(["K","L","M","N","O","P","Q","R","S","T"]):
			x=(ii+0.5)*bw
			b=button(name,bw,bw)
			b.symbol.position=(x,1.5*bw)
			node.add_child(b.symbol)
			self.buttons.append(b)
		
		for ii,name in enumerate(["U","V","W","X","Y","Z",".","-"]):
			x=(ii+0.5)*bw
			b=button(name,bw,bw)
			b.symbol.position=(x,0.5*bw)
			node.add_child(b.symbol)
			self.buttons.append(b)
		
		self.delete=button("DEL",bw,bw)
		self.delete.symbol.position=(8.5*bw,0.5*bw)
		self.delete.lbl.font=font_14
		node.add_child(self.delete.symbol)
		
		self.enter=button("OK",bw,bw)
		self.enter.symbol.position=(9.5*bw,0.5*bw)
		self.enter.lbl.font=font_14
		node.add_child(self.enter.symbol)
		
		# Text field
		symbol=ShapeNode(ui.Path.rect(0,0,w-1,32), "#161616", "#00ccff")
		symbol.anchor_point=(0.0,0.5)
		symbol.position=(0.0,4.5*bw)
		
		self.lbl=LabelNode("")
		self.lbl.color="#00ccff"
		self.lbl.anchor_point=(0.0,0.5)
		self.lbl.position=(3.0,0.0)
		symbol.add_child(self.lbl)
		
		node.add_child(symbol)
			
		self.symbol=node
		
	def on_touch(self,touch,scale):
		if is_touched(self.enter.symbol,touch,scale):
			self.pfd.scratchpad_event("ENTER",self.lbl.text)
		elif is_touched(self.delete.symbol,touch,scale) and len(self.lbl.text)>0:
			self.lbl.text=self.lbl.text[0:len(self.lbl.text)-1]
			
		for b in self.buttons:
			if is_touched(b.symbol,touch,scale):
				self.lbl.text=self.lbl.text+b.lbl.text
				return
		
def is_touched(obj,touch,scale):
		
		return touch.location.x*scale.x>obj.bbox.x and touch.location.x*scale.x<obj.bbox.x+obj.bbox.w and touch.location.y*scale.x>obj.bbox.y and touch.location.y*scale.x<obj.bbox.y+obj.bbox.h
