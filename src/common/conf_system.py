#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import sys
import os

CONF_FILENAME = "../conf/"
CONF_NAME = "system.ini"

def getConfig():
	src_path = os.path.dirname(CONF_FILENAME)
	ini_path = src_path + "/" + CONF_NAME
	if not os.path.exists(ini_path):
		print "# Cannot find system.ini in conf directory : %s" %src_path
		sys.exit(1)

	conf = ConfigParser.RawConfigParser()
	conf.read(ini_path)
	return conf

def getHomeDir(executor_name = 'HOME'):
	conf = getConfig()
	homeDir = conf.get(executor_name, 'home_dir')
	return homeDir

def getAllowedEnv(executor_name = 'ALLOWED_ENV'):
	db_config = {}
	conf = getConfig()
	envs = [env.lower() for env in conf.get(executor_name, 'mode').replace(' ','').split(',')]
	return envs

def getEnvInfo(executor_name = 'ENV'):
	db_config = {}
	conf = getConfig()
	env = conf.get(executor_name, 'mode')
	return env

def getRecoveryServerInfo(executor_name = 'RECOVERY_SERVER'):
	db_config = {}
	conf = getConfig()
	hostIp = conf.get(executor_name, 'hostIp')
	port = int(conf.get(executor_name, 'port'))
	return (hostIP, port)
