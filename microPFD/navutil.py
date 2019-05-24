# Copyright (C) Michael Braunstingl, 2018 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited

import numpy
import os


re=6378100.0


def roll_pitch_yaw_hdg(ATT,MAG,GRAV,a_user):
	ctheta=numpy.cos(ATT[1])
	stheta=numpy.sin(ATT[1])
	rtheta=numpy.array([[1,0,0],[0,ctheta,stheta],[0,-stheta,ctheta]])
	
	cphi=numpy.cos(ATT[0]+numpy.pi*0.5)
	sphi=numpy.sin(ATT[0]+numpy.pi*0.5)
	rphi=numpy.array([[cphi,0,sphi],[0,1,0],[-sphi,0,cphi]])
	
	cpsi=numpy.cos(ATT[2])
	spsi=numpy.sin(ATT[2])
	rpsi=numpy.array([[cpsi,spsi,0],[-spsi,cpsi,0],[0,0,1]])
	
	x=numpy.array([1,0,0])
	y=numpy.array([0,1,0])
	z=numpy.array([0,0,1])
	
	x=rphi.dot(x)
	x=rtheta.dot(x)
	x=rpsi.dot(x)
	
	y=rphi.dot(y)
	y=rtheta.dot(y)
	y=rpsi.dot(y)
	
	z=rphi.dot(z)
	z=rtheta.dot(z)
	z=rpsi.dot(z)

	
	xlvlh=x.dot(numpy.array([1,0,0]))*numpy.array([1,0,0])+x.dot(numpy.array([0,1,0]))*numpy.array([0,1,0])
	xlvlh=xlvlh/numpy.linalg.norm(xlvlh)
	
	ylvlh=numpy.cross(x,xlvlh)*numpy.sign(x[2])
	ylvlh=ylvlh/numpy.linalg.norm(ylvlh)
	
	zlvlh=numpy.cross(xlvlh,ylvlh)
	zlvlh=zlvlh/numpy.linalg.norm(zlvlh)
	
	# xyz axes are synamicallg calibrated by ios, this is not correct
	
	
	# Calculate LVLH axes
	
	
	
	# Calculation of euler angles
	
	pitch=-numpy.arccos(x.dot(xlvlh))*numpy.sign(x[2])
	roll=-numpy.arccos(y.dot(ylvlh))*numpy.sign(y[2])
	roll-=0.5*numpy.pi
	
	#print(GRAV)
	
	
	
	# new stuff
	
	pitch=-numpy.arccos(GRAV[2])*numpy.sign(GRAV[1])-numpy.pi*0.5
	roll=-numpy.arccos(-GRAV[0])*numpy.sign(GRAV[1])-numpy.pi*0.5
	
	
	# old stuff
	#yaw=numpy.arcsin(numpy.dot(numpy.cross(ylvlh,z),GRAV))
	#print(yaw)
	yaw=numpy.arcsin(GRAV[0]+a_user[0])
	
	hdg=numpy.rad2deg(numpy.arccos(x.dot([1,0,0])))
	hdg=hdg*numpy.sign(x.dot([0,1,0]))
	hdg=hdg%360.0
	
	return [roll,pitch,yaw,hdg]


def geo2cart(a):
	return (re+a[0])*numpy.array([numpy.cos(a[2])*numpy.cos(a[1]),numpy.cos(a[2])*numpy.sin(a[1]),numpy.sin(a[2])])
	
	
def great_circle(a,b):
	# great circle normal plane
	a_norm=a/numpy.linalg.norm(a)
	b_norm=b/numpy.linalg.norm(b)
	ab_norm=(b-a)/numpy.linalg.norm(b-a)
	
	normal=numpy.cross(a,b)/(numpy.linalg.norm(a)*numpy.linalg.norm(b))
	
	#dist=numpy.linalg.norm(b-a)
	#print ("a"+str(a))
	#print ("b"+str(b))
	
	# ground distance
	normal_l=numpy.linalg.norm(normal)
	dist=re*numpy.arcsin(normal_l)
	normal=normal/normal_l
	
	# desired track at point a:
	# ... normal of meridian plane
	
	
	east=numpy.cross([0.0,0.0,1.0],a)
	east=east/numpy.linalg.norm(east)
	north=numpy.cross(a/numpy.linalg.norm(a),east)
	
	ab_tang=north*numpy.dot(ab_norm,north)+east*numpy.dot(ab_norm,east)
	ab_tang=ab_tang/numpy.linalg.norm(ab_tang)
	
	#print (numpy.dot(ab_norm,north))
	#print("a="+str(a))
	#print("b="+str(b))
	#print("ab="+str(b-a))
	dtk=numpy.arccos(numpy.dot(ab_tang,north))
	dtk=dtk*numpy.sign(numpy.dot(ab_tang,east))
	
	dtk=dtk%(2.0*numpy.pi)
	
	
	
	
	return [dist,dtk]


def m2ft(x):
	return x/0.3048
	

def find_by_ident(ident):
	fnm="navdata/airports.csv"
	
	print fnm
	print os.path.exists(fnm)
	
	f=open(fnm,"r")
	lines=f.readlines()
	f.close()
	
	print len(lines)
	
	#n_id=5;n_lat=6;n_lon=7;n_elev=8
	n_id=1;n_lat=4;n_lon=5;n_elev=6
	
	for jj,ln in enumerate(lines):
		tokens=ln.split(",")
		compare=tokens[n_id].replace('"','')
	
		if compare==ident:
			lon=float(tokens[n_lon].replace('"',''))
			lat=float(tokens[n_lat].replace('"',''))
			alt=float(tokens[n_elev].replace('"',''))
			geo_pos=numpy.array([alt*0.3048,numpy.deg2rad(lon),numpy.deg2rad(lat)])
			
			name=tokens[3].replace('"','')
			
			return airport(compare,geo_pos,name)
		
			
class airport:
	def __init__(self,ident,geo_pos,name):
		self.ident=ident
		self.geo_pos=geo_pos
		self.name=name

	
	
print find_by_ident("LOWW")


	
	
	
