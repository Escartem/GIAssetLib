import io
import os
import struct


class FileReader:
	""" 
	Taken from AnimeWwise@f28afbb
	"""

	def __init__(self, file, endianness:str, name:str=None):
		self.stream = file
		self.endianness = endianness
		self.name = name

	def _read(self, mode:str, bufferLength:int, endianness:str=None, pos:int=None) -> bytes:
		# endianness override
		if endianness is None:
			endianness = self.endianness

		endianness = "<" if endianness == "little" else ">"

		if pos:
			pos_backup = self.GetBufferPos()
			self.SetBufferPos(pos)

		data = struct.unpack(f"{endianness}{mode}", bytearray(self.stream.read(bufferLength)))[0]

		if pos:
			self.SetBufferPos(pos_backup)

		return data

	# read methods
	def ReadInt8(self, endianness:str=None, pos:int=None) -> int:
		return self._read("b", 1, endianness, pos)

	def ReadUInt8(self, endianness:str=None, pos:int=None) -> int:
		return self._read("B", 1, endianness, pos)

	def ReadInt16(self, endianness:str=None, pos:int=None) -> int:
		return self._read("h", 2, endianness, pos)
	
	def ReadUInt16(self, endianness:str=None, pos:int=None) -> int:
		return self._read("H", 2, endianness, pos)
	
	def ReadInt32(self, endianness:str=None, pos:int=None) -> int:
		return self._read("i", 4, endianness, pos)
	
	def ReadUInt32(self, endianness:str=None, pos:int=None) -> int:
		return self._read("I", 4, endianness, pos)

	def ReadLong(self, endianness:str=None, pos:int=None) -> int:
		return self._read("l", 4, endianness, pos)

	def ReadULong(self, endianness:str=None, pos:int=None) -> int:
		return self._read("L", 4, endianness, pos)

	def ReadLongLong(self, endianness:str=None, pos:int=None) -> int:
		return self._read("q", 8, endianness, pos)

	def ReadULongLong(self, endianness:str=None, pos:int=None) -> int:
		return self._read("Q", 8, endianness, pos)

	def ReadBytes(self, length:int, endianness:str=None, pos:int=None) -> bytes:
		return self._read(f"{str(length)}s", int(length), endianness, pos)

	# buffer utils
	def GetBufferPos(self) -> int:
		return self.stream.tell()

	def SetBufferPos(self, pos:int):
		self.stream.seek(pos)

	def GetStreamLength(self) -> int:
		if isinstance(self.stream, io.BytesIO):
			return self.stream.getbuffer().nbytes
		elif isinstance(self.stream, io.BufferedReader):
			pos = self.GetBufferPos()
			self.stream.seek(0, os.SEEK_END)
			length = self.GetBufferPos()
			self.SetBufferPos(pos)
			return length
		else:
			raise Exception("unknown buffer type")

	def GetRemainingLength(self) -> int:
		return self.GetStreamLength() - self.GetBufferPos()

	def GetName(self) -> str:
		if self.name:
			return self.name
		return ""
