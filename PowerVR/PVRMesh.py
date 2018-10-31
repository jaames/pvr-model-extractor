from PowerVR.EPOD import *

class EPVRMesh:
  eTriangleList          = 0
  eIndexedTriangleList   = 1
  eTriangleStrips        = 2
  eIndexedTriangleStrips = 3
  eTriPatchList          = 4
  eQuadPatchList         = 5

  class VertexData:
    eNone               = 0
    eFloat              = 1
    eInt                = 2
    eUnsignedShort      = 3
    eRGBA               = 4
    eARGB               = 5
    eD3DCOLOR           = 6
    eUBYTE4             = 7
    eDEC3N              = 8
    eFixed16_16         = 9
    eUnsignedByte      = 10
    eShort             = 11
    eShortNorm         = 12
    eByte              = 13
    eByteNorm          = 14
    eUnsignedByteNorm  = 15
    eUnsignedShortNorm = 16
    eUnsignedInt       = 17
    eABGR              = 18
    eCustom            = 1000
  
  class FaceData:
    e16Bit = 3
    e32Bit = 17

class PVRMesh:
  def __init__(self):
    self.unpackMatrix = []
    self.vertexElementData = []
    self.vertexElements = {}
    self.primitiveData = {
      "numVertices": 0,
      "numFaces": 0,
			"numStrips": 0,
			"numPatchesSubdivisions": 0,
			"numPatches": 0,
			"numControlPointsPerPatch": 0,
			"stripLengths": None,
		  "primitiveType": EPVRMesh.eIndexedTriangleList
    }
    self.boneBatches = {
			"boneMax": 0,
			"count": 0,
			"batches": None,
			"boneCounts": None,
			"offsets": None
		}
    self.faces = {
      "indexType": EPVRMesh.FaceData.e16Bit,
      "data": None
		}
  
  def AddData(self, data):
    self.vertexElementData.append(data)
    return len(self.vertexElementData) - 1
  
  def AddFaces(self, data, type):
    self.faces["indexType"] = type
    self.faces["data"] = data
    self.primitiveData["numFaces"] = len(data) // 3 if len(data) > 0 else 0
    return EPODErrorCodes.eNoError

  def AddElement(self, semantic, type, numComponents, stride, offset, dataIndex):
    if semantic in self.vertexElements:
      return EPODErrorCodes.eKeyAlreadyExists
    self.vertexElements[semantic] = {
      "semantic": semantic,
      "dataType": type,
      "numComponents": numComponents,
      "stride": stride,
      "offset": offset,
      "dataIndex": dataIndex,
    }
    return EPODErrorCodes.eNoError