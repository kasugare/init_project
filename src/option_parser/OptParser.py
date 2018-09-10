#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.util_datetime import htime
from optparse import OptionParser
from OptValidator import OptValidator
import traceback
import sys
import copy
import os

class OptParser:
	def __init__(self, logger):
		self._logger = logger
		self._options()

	def _options(self):
		usage = """usage: %prog [options] arg1,arg2 [options] arg3"""

		parser = OptionParser(usage=usage)
		parser.add_option("-v", "--version",
			action="store_true",
			dest="version",
			default=False,
			help="""show recovery system version""")

		parser.add_option("-p", "--period",
			action="store",
			dest="period",
			type="str",
			default='1m',
			nargs=1,
			help="""[required] recovery period
			[use] -p 1s/1m/1h or --period=1s/1m/1h""")

		parser.add_option("-S", "--StoreType",
			action="store",
			type="string",
			dest="storeType",
			default="file",
			help="""select DB
			[use] -S file, -S hive, --StoreType=file
			[options] rdb or etable
			[default: %default]""")

		parser.add_option("--DEBUG",
			action="store_true",
			default=False,
			dest="debugMode",
			help="""use this option if it have been processed,
			it will operate in DEBUG mode.
			[use] --DEBUG
			[options] --DEBUG or None
			[default: %default""")

		options, args = parser.parse_args()
		self._vaildOptions(options, args)

	def _vaildOptions(self, options, args):
		optVaildator = OptValidator(self._logger, options, args)
		self.orderSheet = optVaildator.doCheckOptions()

	def getOrderSheet(self):
		self.showOptions()
		return self.orderSheet

	def showOptions(self):
		isDebugMode = self.orderSheet['debugMode']
		self._logger.info("=" * 100)
		optKeys = ['version', 'period', 'storeType', 'debugMode']

		if isDebugMode:
			for optKey in optKeys:
				if not self.orderSheet.has_key(optKey) and not optKey == '-':
					continue
				if optKey == '-':
					self._logger.info(optKey * 100)
				else:
					self._logger.info('# %s : %s' %(optKey.ljust(15), str(self.orderSheet[optKey])))
		else:
			for optKey in optKeys:
				if not self.orderSheet.has_key(optKey) and not optKey == '-':
					continue
				if optKey == '-':
					self._logger.info(optKey * 100)
				else:
					value = self.orderSheet[optKey]
					if type(value) == list and len(value) > 10:
						self._logger.info('# %s : [ %d (set) ]' %(optKey.ljust(15), len(self.orderSheet[optKey])))
					else:
						self._logger.info('# %s : %s' %(optKey.ljust(15), str(self.orderSheet[optKey])))
		self._logger.info("=" * 100)
