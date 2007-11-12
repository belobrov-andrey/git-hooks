#!/usr/bin/env python

import os, smtplib
from config import config

def callback(hash):
	global config
	msg = []
	repo = os.getcwd().split("/")[-1]
	if repo == ".git":
		repo = os.getcwd().split("/")[-2]
	sock = os.popen('git log -1 --pretty=format:"%s" ' + hash)
	name = sock.read()
	sock.close()
	sock = os.popen('git log -1 --pretty=format:"%cn <%ce>" ' + hash)
	fro = sock.read()
	sock.close()
	to = config.dest
	subject = "%s: %s" % (repo, name)
	msg.append("From: %s \nTo: %s\nSubject: %s\n" % (fro, to, subject))

	if config.gitweb_url:
		msg.append("Git-Url: %s?p=%s.git;a=commitdiff;h=%s\n" % (config.gitweb_url, repo, hash))
	sock = os.popen("git show " + hash)
	lines = []
	for i in sock.readlines():
		lines.append(i.strip())
	msg.extend(lines)
	sock.close()

	if config.send:
		server = smtplib.SMTP('localhost')
		server.sendmail(fro, to, "\n".join(msg))
		server.quit()
	else:
		print "\n".join(msg)
