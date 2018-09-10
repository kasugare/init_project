#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.recovery_conf import getProcessInfo
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, Lock
import traceback
import pickle


BUFFER = 1024

class MonitoringServer:
	def __init__(self, RecoveryPorcessManager, _logger):
		self._logger = _logger
		processInfo = getProcessInfo()
		self.hostIp = processInfo['host']
		self.hostPort = int(processInfo['port'])

	def runMonitoringServer(self):
		try:
			svrsock = socket(AF_INET, SOCK_STREAM)
			svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
			svrsock.bind((self.hostIp, self.hostPort))
			svrsock.listen(5)

			while True:
				socketObj, addr = svrsock.accept()
				requestHandler = Thread(target=self._bindClientRequest, args=(socketObj, addr))
				requestHandler.setDaemon(1)
				requestHandler.start()
		except Exception, e:
			self._logger.error(str(traceback.format_exc(e)))

	def _bindClientRequest(self, socketObj, addr):
		requestCall = self._recvMessage(socketObj)
		self._sendMessage(socketObj, requestCall)


	def _sendMessage(self, socketObj, message):
		try:
			encodedMsg = pickle.dumps(message)
			sendMsg = "#%d\r\n%s" %(len(encodedMsg), encodedMsg)
			msgLength = len(sendMsg)
			totalsent = 0

			while totalsent < msgLength:
				sendLength = socketObj.send(sendMsg[totalsent:])
				if sendLength == 0:
					break
				totalsent = totalsent + sendLength

		except Exception, e:
			self._logger.error(str(traceback.format_exc(e)))


	def _recvMessage(self, socketObj):
		dataBuffer = []
		try:
			receivedByte = 0
			msgLength = 0
			while True:
				if receivedByte == 0:
					data = socketObj.recv(BUFFER)
					lengthIndex = data.find('\r\n')
					if lengthIndex == -1:
						return
					msgLength = int(data[:lengthIndex].split('#')[1])
					rawData = data[lengthIndex+2:]
					dataBuffer.append(rawData)
					receivedByte = len(rawData)

				if receivedByte >= msgLength:
					break
				data = socketObj.recv(min(msgLength - receivedByte, BUFFER))
				dataBuffer.append(data)
				receivedByte = receivedByte + len(str(data))
				if msgLength - receivedByte <= 0:
					break
		except Exception, e:
			self._logger.error(str(traceback.format_exc(e)))
		clientMsg = pickle.loads("".join(dataBuffer))
		return clientMsg

