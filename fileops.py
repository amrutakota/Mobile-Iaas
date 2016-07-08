#! /usr/bin/python

import os
import sqlite3
from file_ecc import EncodeFile,DecodeFiles
from pinger import Pinger
from dbops import pingips,topk


class FileManager(object):
	filepath = filename = ""
	testFile = prefix = ""
	availfiles = ""
	k=0
	n=0
	userips=[]

	def init(self):
                path=os.path.abspath(self.filename)
                self.filepath,self.filename = os.path.split(path)
                self.filepath = self.filepath+'/'
		self.testFile = self.prefix = self.filepath+self.filename
		self.logFile = self.testFile+'.log'
		return

	def authenticate(self):
		ping = Pinger()
		ping.thread_count = 4
		ping.hosts = pingips()
		nodes=ping.start()
                self.userips=nodes['alive']
		os.system("ssh-keygen")
		for userip in self.userips:
			os.system("ssh-copy-id pi@"+userip)
		return
        
        def availparts(self):		
		os.system("find "+self.filepath+" -name '"+self.filename+".p_*' > "+self.logFile)
		self.availfiles = [int(line[-2]) for line in open(self.logFile)]
		return

	def encode(self):
		names = EncodeFile(self.testFile,self.prefix,self.n,self.k)

	def decode(self):
		decList = map(lambda x: self.prefix + '.p_' + `x`,self.availfiles)
		decodedFile = self.testFile+"_decoded"
		DecodeFiles(decList,decodedFile)
		os.system("rm "+self.logFile+" "+self.testFile+".p_*")
		return

	def send(self):
		self.availparts()
		self.userips=topk(self.n)
		files = [line[:-1] for line in open(self.logFile)]
		if(len(self.userips)<len(files)):
			print "Less active nodes...Connect more devices"
			return
		temp=[x+" "+y+"\n" for x,y in zip(files,self.userips)]
		target=open(self.logFile,'w')
		target.write(str(self.k)+" "+str(self.n)+"\n")
		for line in temp:
			target.write(line)
		for f,ip in zip(files,self.userips): 
			os.system("scp "+f+" pi@"+ip+":/home/pi/files/"+f.split('/')[-1])
		os.system("rm "+self.testFile+" "+self.testFile+".p_*")
		return

	def recv(self):
		files = [line[:-1] for line in open(self.logFile)]
		k,n=files[0].split()
		k=int(k)
		files.remove(files[0])
		temp=open(self.logFile,'w')
		temp.truncate()
		for line in files:
			x,y=line.split()
			temp.write(x+" "+y+"\n")
			x=x.split('/')[-1]
			try:
				a=os.system("scp pi@"+y+":/home/pi/files/"+x+" "+self.filepath+x)
				if a==0:
					k=k-1
				if k==0:
					break
			except:
				print "host not found"
		temp.close()
		if k!=0:
			print "Cannot decode file"
			return
		self.availparts()
		return
