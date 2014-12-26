#!/usr/bin/env python
import sys
import pygame
import getopt
from string import split
from math import *



pygame.init()
pygame.font.init()
size=(640,480)
scale=0.9
color=(127,127,127)
fontcolor=(63,63,63)
vertexcolor=(255,255,255)
bg=(0,0,0)
font=pygame.font.SysFont("monospace",20)
font.set_bold(True)
directed=False
one_indexed=False
screenshot="graph.jpg"

def draw_edge(v1,v2):
	draw_edge_pos(pos[v1],pos[v2])

def draw_edge_pos(v1,v2):
	pygame.draw.line(window,color,v1,v2,2)

def draw_directed_edge(v1,v2):
	draw_directed_edge_pos(pos[v1],pos[v2])

def draw_arrow_dash(pos,angle):
	pygame.draw.line(window,color,pos,(pos[0]+25*sin(angle),pos[1]+25*cos(angle)),2)

def draw_directed_edge_pos(v1,v2):
	draw_edge_pos(v1,v2)
	angle=atan2(v1[0]-v2[0],v1[1]-v2[1])
	draw_arrow_dash(v2,angle+0.3)
	draw_arrow_dash(v2,angle-0.3)

def draw_vertex(i,p):
	pygame.draw.circle(window,vertexcolor,[int(p[0]),int(p[1])],10)
	text=font.render(str(i),1,fontcolor)
	window.blit(text,[int(p[0]-font.size(str(i))[0]/2),int(p[1]-font.size(str(i))[1]/2)])

def draw_all():
	window.fill(bg)
	for e in edges:
		if directed:
			draw_directed_edge(e[0],e[1])
		else:
			draw_edge(e[0],e[1])
	for i,p in enumerate(pos):
		draw_vertex(i+1,p)
	pygame.display.flip()

def make_screenshot():
	pygame.image.save(window,screenshot)
	print "Screenshot saved as "+screenshot

def move_pos(a,b):
	return (a[0]+b[0],a[1]+b[1])

def get_closest(a):
	closest=-1
	min_dist=5000*5000 # much more than size**2
	for i,v in enumerate(pos):
		cur_dist=(v[0]-a[0])**2+(v[1]-a[1])**2
		if cur_dist<min_dist:
			min_dist=cur_dist
			closest=i
	return closest

def usage():
	print "This program is used to draw mathematical graphs."
	print "Usage:"
	print sys.argv[0]+" [-d] [-h] [-o] [-s filename.jpg]"
	print "Flags:"
	print "-d"
	print "\tuse directed graphs (default: non-directed)"
	print "-h"
	print "\tshow this help"
	print "-o"
	print "\tindex vertices from one (default: zero-indexing)"
	print "-s filename.jpg"
	print "\t save graph image as filename.jpg"
	print ""
	print "The program reads from stdin input in the following form:"
	print "First, two integers 'n' and 'm', where:"
	print "n - number of vertices,"
	print "m - number of edges."
	print "Then, there are m descriptions of edges, each consisting"
	print "of two integers - source and destination vertex numbers."
	print "Note that after sending input the program is still interactive"
	print "- you can for example press 'S' key to save a screenshot or"
	print "move vertices with your mouse."
	print ""
	print "Example usage:"
	print sys.argv[0]+" -d <<< \"5 3"
	print "1 2"
	print "1 4"
	print "4 0\""


#ENTRY POINT

try:
	opts,args=getopt.getopt(sys.argv[1:],"dohs:")
except getopt.GetoptError:
	usage()
	exit(1)

for opt,arg in opts:
	if opt=='-d':
		directed=True
	if opt=='-o':
		one_indexed=True
	if opt=='-h':
		usage()
		exit(1)
	if opt=='-s':
		screenshot=arg

window=pygame.display.set_mode(size)
inp=split(sys.stdin.read())
n=int(inp[0])
edges=[]
m=int(inp[1])
inp=inp[2:]
if len(inp)!=2*m:
	usage()
	exit(1)
for i in xrange(0,2*m,2):
	if not one_indexed:
		edges.append((int(inp[i]),int(inp[i+1])))
	else:
		edges.append((int(inp[i]-1),int(inp[i+1]-1)))
pos=[(size[0]/2+size[0]/2*scale*sin(pi*2*i/n),size[1]/2-size[1]/2*scale*cos(pi*2*i/n)) for i in range(n)]
draw_all()
make_screenshot()

# MAIN LOOP

mouse_start=(0,0)
moving_vertex=-1

while True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			if event.key==pygame.K_s:
				make_screenshot()
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_start=event.pos
			moving_vertex=get_closest(mouse_start)
		elif event.type==pygame.MOUSEBUTTONUP:
			moving_vertex=-1
		elif event.type==pygame.MOUSEMOTION:
			if moving_vertex>=0:
				pos[moving_vertex]=move_pos(pos[moving_vertex],event.rel)
		else:
			#print event
			""
	draw_all()
			
