#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RecoveryProcessManager:
	def __init__(self):
		self.recoveryReqHandler = None

		self._logger = ELogger.getInstance()
		logPath, logLevel = getLogDir()
		self._logger.setFilename(logPath)
		if logLevel == 'info':
			self._logger.setLevel(ELogger.DEBUG)
		else:
			self._logger.setLevel(ELogger.DEBUG)

	def runRecoveryServer(self):
		self._logger.info("# Start recovery server")
		try:
			svrsock = socket(AF_INET, SOCK_STREAM)
			svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
			svrsock.bind(getRecoveryServerInfo())
			svrsock.listen(5)

			while True:
				socketObj, addr = svrsock.accept()
				requestHandler = Thread(target=self._bindClientRequest, args=(socketObj, addr))
				requestHandler.setDaemon(1)
				requestHandler.start()

				self._logger.info("# connected client")
				self._logger.info("- client addr : %s, port : %d" %(addr[0], addr[1]))
		except Exception, e:
			self._logger.exception(e)

	def _bindClientRequest(self, socketObj, addr):
		dataBuffer = []
		try:
			receivedByte = 0
			dataLength = 0
			while True:
				if receivedByte == 0:
					data = socketObj.recv(BUFFER)
					lengthIndex = data.find('\r\n')
					dataLength = int(data[:lengthIndex].split('#')[1])
					rawData = data[lengthIndex+2:]
					dataBuffer.append(rawData)
					receivedByte = len(rawData)

				if receivedByte >= dataLength:
					break

				data = socketObj.recv(min(dataLength - receivedByte, BUFFER))
				dataBuffer.append(data)

				receivedByte = receivedByte + len(str(data))
				if dataLength - receivedByte <= 0:
					break

		except Exception, e:
			self._logger.exception(e)

		data = self._decodeData(dataBuffer)

	def runAutoRecovery(self):
		self._runRequestReducer()
		self._runMonitoringServer()
		self._runRecovery()

	def _runRecovery(self):
		ProcessHandler(self._logger).doRecovery()

	def _runRequestReducer(self):
		self._logger.info("# Start Request Reducer")
		self.recoveryReqHandler = RecoveryReqHandler(self._logger)
		self.recoveryReqHandler.prepare()


	def _runMonitoringServer(self):
		self._logger.info("# Start Monitoring Server")
		monitoringServer = Thread(target=MonitoringServer(self, self._logger).runMonitoringServer, args=())
		monitoringServer.setDaemon(1)
		monitoringServer.start()
