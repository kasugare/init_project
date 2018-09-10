#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.util_logger import Logger
from option_parser.OptParser import OptParser
import traceback
import sys

class ProcessManager:
	def __init__(self, logger = None):
		if logger != None:
			self._logger = logger
		else:
			self._logger = Logger().getLogger()

		optionParser = OptParser(self._logger)
		self._orderSheet = optionParser.getOrderSheet()

	def doProcess(self, recoveryOptions = None):
		try:
			self._logger.info("# doProcess")
		except Exception, e:
			self._logger.exception(e)
			sys.exit(1)
		self._logger.info("# job completed")
