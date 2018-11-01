# https://github.com/powervr-graphics/WebGL_SDK/blob/4.0/Tools/PVRTexture.js
# http://cdn.imgtec.com/sdk-documentation/PVR%20File%20Format.Specification.pdf
from os import path
import struct

class EPVRTexture:
  class ChannelTypes:
    UnsignedByteNorm = 0,
    SignedByteNorm = 1,
    UnsignedByte = 2,
    SignedByte = 3,
    UnsignedShortNorm = 4,
    SignedShortNorm = 5,
    UnsignedShort = 6,
    SignedShort = 7,
    UnsignedIntegerNorm = 8,
    SignedIntegerNorm = 9,
    UnsignedInteger = 10,
    SignedInteger = 11,
    SignedFloat = 12,
    Float = 12 # the name Float is now deprecated.
    UnsignedFloat = 13

class PVRTexture:
  def __init__(self):
    self.name = ""
    self.version = 0x03525650
    self.flags = 0
    self.pixelFormatH = 0
    self.pixelFormatL = 0
    self.colourSpace = 0;
    self.channelType = 0
    self.height = 1
    self.width = 1
    self.depth = 1
    self.numSurfaces = 1
    self.numFaces = 1
    self.MIPMapCount = 1
    self.metaDataSize = 0
    self.stream = None

  def setName(self, name):
    self.name = path.splitext(name)[0]
  
  def open(self, dir="./", ext=".pvr"):
    resource = path.join(dir, self.name + ext)
    with open(resource, "rb") as stream:
      self.stream = stream
      self.read()
  
  def read(self):
    meta = {}
    self.version, self.flags = struct.unpack("<II", self.stream.read(8))
    self.pixelFormatH, self.pixelFormatL = struct.unpack("<II", self.stream.read(8))
    self.colorSpace, self.channelType = struct.unpack("<II", self.stream.read(8))
    self.height, self.width, self.depth = struct.unpack("<III", self.stream.read(12))
    self.numSurfaces, self.numFaces = struct.unpack("<II", self.stream.read(8))
    self.MIPMapCount, self.metadataSize = struct.unpack("<II", self.stream.read(8))

    