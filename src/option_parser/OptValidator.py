#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.conf_version import getVersionInfo
from copy import deepcopy
import traceback
import datetime
import time
import sys
import os

class OptValidator:
	def __init__(self, logger, options, args):
		self._logger = logger
		self._versionInfo = getVersionInfo()
		self._orderSheet = self._setOrderSheet(options, args)

		if self._orderSheet['debugMode']:
			self._logger.setLevel("DEBUG")
		else:
			self._logger.setLevel("INFO")

	def _setOrderSheet(self, options, args):
		orderSheet = {}
		if options.version != None:
			orderSheet['version'] = options.version
		if options.period != None:
			orderSheet['period'] = options.period
		if options.storeType != None:
			orderSheet['storeType'] = options.storeType
		if options.debugMode != None:
			orderSheet['debugMode'] = options.debugMode
		return orderSheet

	def doCheckOptions(self):
		self._logger.debug("# check user options ...")
		orderSheet = {}
		# set debug mode
		orderSheet['debugMode'] = self._checkLogMode()
		# Verbose
		orderSheet['version'] = self._checkVersion()
		# select insert target DB
		orderSheet['storeType'] = self._checkStoreType(orderSheet)

		return orderSheet


	def _checkInputFileArgs(self, args):
		files = []
		if args:
			for expectedFile in args:
				if os.path.exists(expectedFile):
					files.append(expectedFile)
		return files

	def _checkVersion(self):
		if self._orderSheet.get('version'):
			print "# Recovery System"
			if self._versionInfo.has_key('version'):
				print " - version : %s" %(self._versionInfo['version'])
			if self._versionInfo.has_key('update_date'):
				print " - update date : %s" %(self._versionInfo['update_date'])
			if self._versionInfo.has_key('describe'):
				print " - describe : %s" %(self._versionInfo['describe'])

			sys.exit(1)
		return self._versionInfo

	def _checkStoreType(self, orderSheet):
		storeType = self._orderSheet.get('storeType')

		if storeType == 'file':
			return storeType
		elif storeType == 'hdfs':
			return storeType
		elif storeType == 'hive':
			return storeType
		else:
			self._logger.error('exit : _checkStoreType')
			sys.exit(1)

	def _checkLogMode(self):
		return self._orderSheet.get('debugMode')
