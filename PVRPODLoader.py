import struct
import numpy as np

from EPOD import *
from PVRMesh import EPVRMesh, PVRMesh

# https://github.com/powervr-graphics/WebGL_SDK/blob/4.0/Tools/PVRPODLoader.js

PVRVertexDataTypeSize = {
  EPVRMesh.VertexData.eFloat: 4,
  EPVRMesh.VertexData.eInt: 4,
  EPVRMesh.VertexData.eUnsignedInt: 4,
  EPVRMesh.VertexData.eShort: 2,
  EPVRMesh.VertexData.eShortNorm: 2,
  EPVRMesh.VertexData.eUnsignedShort: 2,
  EPVRMesh.VertexData.eUnsignedShortNorm: 2,
  EPVRMesh.VertexData.eRGBA: 4,
  EPVRMesh.VertexData.eABGR: 4,
  EPVRMesh.VertexData.eARGB: 4,
  EPVRMesh.VertexData.eD3DCOLOR: 4,
  EPVRMesh.VertexData.eUBYTE4: 4,
  EPVRMesh.VertexData.eDEC3N: 4,
  EPVRMesh.VertexData.eFixed16_16: 4,
  EPVRMesh.VertexData.eUnsignedByte: 1,
  EPVRMesh.VertexData.eUnsignedByteNorm: 1,
  EPVRMesh.VertexData.eByte: 1,
  EPVRMesh.VertexData.eByteNorm: 1
}

PVRVertexDataTypeMap = {
  EPVRMesh.VertexData.eFloat: np.float32,
  EPVRMesh.VertexData.eInt: np.int32,
  EPVRMesh.VertexData.eUnsignedInt: np.uint32,
  EPVRMesh.VertexData.eShort: np.int16,
  EPVRMesh.VertexData.eShortNorm: np.int16,
  EPVRMesh.VertexData.eUnsignedShort: np.uint16,
  EPVRMesh.VertexData.eUnsignedShortNorm: np.uint16,
  EPVRMesh.VertexData.eRGBA: np.uint32,
  EPVRMesh.VertexData.eABGR: np.uint32,
  EPVRMesh.VertexData.eARGB: np.uint32,
  EPVRMesh.VertexData.eD3DCOLOR: np.uint32,
  EPVRMesh.VertexData.eUBYTE4: np.uint32,
  EPVRMesh.VertexData.eDEC3N: np.uint32,
  EPVRMesh.VertexData.eFixed16_16: np.uint32,
  EPVRMesh.VertexData.eUnsignedByte: np.uint8,
  EPVRMesh.VertexData.eUnsignedByteNorm: np.uint8,
  EPVRMesh.VertexData.eByte: np.int8,
  EPVRMesh.VertexData.eByteNorm: np.int8
}

class PVRPODLoader:
  def __init__(self, stream):
    self.stream = stream
    self.Read()
  
  def Read(self):
    for (ident, length) in self.ReadTags():
      # Read version block
      if ident == EPODIdentifiers.eFormatVersion | EPODDefines.startTagMask:
        versionString = self.stream.read(length).decode("utf-8")
      
      # Read scene block
      elif ident == EPODIdentifiers.eScene | EPODDefines.startTagMask:
        return self.ReadSceneBlock()
      
      # Skip unimplemented block types
      else:
        self.stream.seek(length, 1)

  def ReadTag(self):
    try:
      return struct.unpack("<II", self.stream.read(8))
    except struct.error:
      return None
  
  def ReadTags(self):
    tag = self.ReadTag()
    while tag:
      yield tag
      tag = self.ReadTag()

  def ReadSceneBlock(self):
    for (ident, length) in self.ReadTags():

      if ident == EPODIdentifiers.eScene | EPODDefines.endTagMask:
        # do final checks, break tag loop
        break

      elif ident == EPODIdentifiers.eSceneClearColour | EPODDefines.startTagMask:
        print("clear color", np.frombuffer(self.stream.read(12), dtype=np.float32))

      elif ident == EPODIdentifiers.eSceneAmbientColour | EPODDefines.startTagMask:
        print("ambient color", np.frombuffer(self.stream.read(12), dtype=np.float32))

      elif ident == EPODIdentifiers.eSceneNumCameras | EPODDefines.startTagMask:
        print("cameras", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneNumLights | EPODDefines.startTagMask:
        print("lights", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneNumMeshes | EPODDefines.startTagMask:
        print("meshes", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneNumNodes | EPODDefines.startTagMask:
        print("nodes", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneNumMeshNodes | EPODDefines.startTagMask:
        print("mesh nodes", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneNumTextures | EPODDefines.startTagMask:
        print("textures", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneNumMaterials | EPODDefines.startTagMask:
        print("materials", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneNumFrames | EPODDefines.startTagMask:
        print("frames", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneFlags | EPODDefines.startTagMask:
        print("flags", struct.unpack("<i", self.stream.read(4))[0])

      elif ident == EPODIdentifiers.eSceneFPS | EPODDefines.startTagMask:
        print("fps", struct.unpack("<i", self.stream.read(4))[0])
        
      elif ident == EPODIdentifiers.eSceneUserData | EPODDefines.startTagMask:
        print("user data")
        self.stream.read(length)

      elif ident == EPODIdentifiers.eSceneUnits | EPODDefines.startTagMask:
        print("units", struct.unpack("<i", self.stream.read(4)))

      elif ident == EPODIdentifiers.eSceneCamera | EPODDefines.startTagMask:
        print("camera")
        self.stream.read(length)

      elif ident == EPODIdentifiers.eSceneLight | EPODDefines.startTagMask:
        print("light")
        self.stream.read(length)

      elif ident == EPODIdentifiers.eSceneMesh | EPODDefines.startTagMask:
        print("mesh")
        self.ReadMeshBlock()

      elif ident == EPODIdentifiers.eSceneNode | EPODDefines.startTagMask:
        print("node")
        self.stream.read(length)

      elif ident == EPODIdentifiers.eSceneTexture | EPODDefines.startTagMask:
        print("texture")
        self.stream.read(length)

      elif ident == EPODIdentifiers.eSceneMaterial | EPODDefines.startTagMask:
        print("material")
        self.stream.read(length)

      # Skip unimplemented block types
      else:
        self.stream.seek(length, 1)

  def ReadMeshBlock(self):
    mesh = PVRMesh()
    numUVWs = 0
    podUVWs = 0
    interleavedDataIndex = -1

    for (ident, length) in self.ReadTags():

      if ident == EPODIdentifiers.eSceneMesh | EPODDefines.endTagMask:
        # do final checks
        # break tag loop
        return mesh

      elif ident == EPODIdentifiers.eMeshNumVertices | EPODDefines.startTagMask:
        mesh.primitiveData["numVertices"] = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMeshNumFaces | EPODDefines.startTagMask:
        mesh.primitiveData["numFaces"] = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMeshNumUVWChannels | EPODDefines.startTagMask:
        podUVWs = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMeshStripLength | EPODDefines.startTagMask:
        mesh.primitiveData["stripLengths"] = np.frombuffer(self.stream.read(length), dtype=np.uint32)

      elif ident == EPODIdentifiers.eMeshNumStrips | EPODDefines.startTagMask:
        mesh.primitiveData["numStrips"] = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMeshInteravedDataList | EPODDefines.startTagMask:
        mesh.AddData(self.stream.read(length))

      elif ident == EPODIdentifiers.eMeshBoneBatchIndexList | EPODDefines.startTagMask:
        mesh.boneBatches["batches"] = np.frombuffer(self.stream.read(length), dtype=np.uint32)

      elif ident == EPODIdentifiers.eMeshNumBoneIndicesPerBatch | EPODDefines.startTagMask:
        mesh.boneBatches["boneCounts"] = np.frombuffer(self.stream.read(length), dtype=np.uint32)

      elif ident == EPODIdentifiers.eMeshBoneOffsetPerBatch | EPODDefines.startTagMask:
        mesh.boneBatches["offsets"] = np.frombuffer(self.stream.read(length), dtype=np.uint32)

      elif ident == EPODIdentifiers.eMeshMaxNumBonesPerBatch | EPODDefines.startTagMask:
        mesh.boneBatches["boneMax"] = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMeshMaxNumBonesPerBatch | EPODDefines.startTagMask:
        mesh.boneBatches["count"] = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMeshUnpackMatrix | EPODDefines.startTagMask:
        mesh.unpackMatrix = np.frombuffer(self.stream.read(length), dtype=np.float32)

      elif ident == EPODIdentifiers.eMeshUnpackMatrix | EPODDefines.startTagMask:
        mesh.unpackMatrix = np.frombuffer(self.stream.read(length), dtype=np.float32)

      elif ident == EPODIdentifiers.eMeshVertexIndexList | EPODDefines.startTagMask:
        (data, dataType) = self.ReadVertexIndexData()
        mesh.AddFaces(data, dataType)

      elif ident == EPODIdentifiers.eMeshVertexList | EPODDefines.startTagMask:
        self.ReadVertexData(mesh, "POSITION0", ident, interleavedDataIndex)

      elif ident == EPODIdentifiers.eMeshNormalList | EPODDefines.startTagMask:
        self.ReadVertexData(mesh, "NORMAL0", ident, interleavedDataIndex)

      elif ident == EPODIdentifiers.eMeshTangentList | EPODDefines.startTagMask:
        self.ReadVertexData(mesh, "TANGENT0", ident, interleavedDataIndex)

      elif ident == EPODIdentifiers.eMeshBinormalList | EPODDefines.startTagMask:
        self.ReadVertexData(mesh, "BINORMAL0", ident, interleavedDataIndex)

      elif ident == EPODIdentifiers.eMeshUVWList | EPODDefines.startTagMask:
        self.ReadVertexData(mesh, "UV" + str(numUVWs), ident, interleavedDataIndex)
        numUVWs += 1
      
      elif ident == EPODIdentifiers.eMeshVertexColourList | EPODDefines.startTagMask:
        self.ReadVertexData(mesh, "VERTEXCOLOR0", ident, interleavedDataIndex)
      
      elif ident == EPODIdentifiers.eMeshBoneIndexList | EPODDefines.startTagMask:
        self.ReadVertexData(mesh, "BONEINDEX0", ident, interleavedDataIndex)
      
      elif ident == EPODIdentifiers.eMeshBoneWeightList | EPODDefines.startTagMask:
        self.ReadVertexData(mesh, "BONEWEIGHT", ident, interleavedDataIndex)

      else:
        self.stream.seek(length, 1)

  def ReadVertexIndexData(self):
    data = None
    dataType = EPVRMesh.FaceData.e16Bit

    for (ident, length) in self.ReadTags():
      if ident == EPODIdentifiers.eMeshVertexIndexList | EPODDefines.endTagMask:
        return (data, dataType)
      
      elif ident == EPODIdentifiers.eBlockDataType | EPODDefines.startTagMask:
        value = struct.unpack("<i", self.stream.read(4))[0]
        if value == EPVRMesh.VertexData.eUnsignedInt:
          dataType = EPVRMesh.FaceData.e32Bit
        elif value == EPVRMesh.VertexData.eUnsignedShort:
          dataType = EPVRMesh.FaceData.e16Bit
        else:
          print("unhandled vert data type:", value)

      elif ident == EPODIdentifiers.eBlockData | EPODDefines.startTagMask:
        if dataType == EPVRMesh.FaceData.e16Bit:
          data = np.frombuffer(self.stream.read(length), dtype=np.uint16)
        elif dataType == EPVRMesh.FaceData.e32Bit:
          data = np.frombuffer(self.stream.read(length), dtype=np.uint32)
      
      else:
        self.stream.seek(length, 1)

  def ReadVertexData(self, mesh, semanticName, blockIdentifier, dataIndex):
    numComponents = 0
    stride = 0
    offset = 0
    dataType = EPVRMesh.VertexData.eNone

    for (ident, length) in self.ReadTags():

      if ident == blockIdentifier | EPODDefines.endTagMask:
        if numComponents != 0:
          mesh.AddElement(semanticName, dataType, numComponents, stride, offset, dataIndex)
        break

      elif ident == EPODIdentifiers.eBlockDataType | EPODDefines.startTagMask:
        dataType = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eBlockNumComponents | EPODDefines.startTagMask:
        numComponents = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eBlockStride | EPODDefines.startTagMask:
        stride = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eBlockData | EPODDefines.startTagMask:
        if dataIndex == -1:
          data = np.frombuffer(self.stream.read(length), dtype=PVRVertexDataTypeMap[dataType])
          dataIndex = mesh.AddData(data)
        else:
          offset = struct.unpack("<I", self.stream.read(4))[0]

      else: 
        self.stream.seek(length, 1)

with open("./test.pod", "rb") as f:
  model = PVRPODLoader(f)
