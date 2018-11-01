import struct
import numpy as np

from PowerVR.EPOD import *
from PowerVR.PVRModel import PVRModel
from PowerVR.PVRMesh import PVRMesh, EPVRMesh
from PowerVR.PVRMaterial import PVRMaterial, EPVRMaterial
from PowerVR.PVRLight import PVRLight, EPVRLight
from PowerVR.PVRTexture import PVRTexture
from PowerVR.PVRCamera import PVRCamera
from PowerVR.PVRNode import PVRNode

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
    self.scene = None
    self.versionString = None
    self.Read()

  @classmethod
  def open(cls, path):
    with open(path, "rb") as buffer:
      return cls(buffer)
  
  def Read(self):
    for (ident, length) in self.ReadTags():
      # Read version block
      if ident == EPODIdentifiers.eFormatVersion | EPODDefines.startTagMask:
        self.versionString = self.ReadString(length)
      
      # Read scene block
      elif ident == EPODIdentifiers.eScene | EPODDefines.startTagMask:
        self.scene = self.ReadSceneBlock()
      
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
    model = PVRModel()
    for (ident, length) in self.ReadTags():

      if ident == EPODIdentifiers.eScene | EPODDefines.endTagMask:
        # do final checks, break tag loop
        return model

      elif ident == EPODIdentifiers.eSceneClearColour | EPODDefines.startTagMask:
        model.clearColour = np.frombuffer(self.stream.read(12), dtype=np.float32)

      elif ident == EPODIdentifiers.eSceneAmbientColour | EPODDefines.startTagMask:
        model.ambientColour = np.frombuffer(self.stream.read(12), dtype=np.float32)

      elif ident == EPODIdentifiers.eSceneNumCameras | EPODDefines.startTagMask:
        model.numCameras = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneNumLights | EPODDefines.startTagMask:
        model.numLights = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneNumMeshes | EPODDefines.startTagMask:
        model.numMeshes = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneNumNodes | EPODDefines.startTagMask:
        model.numNodes = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneNumMeshNodes | EPODDefines.startTagMask:
        model.numMeshNodes = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneNumTextures | EPODDefines.startTagMask:
        model.numTextures = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneNumMaterials | EPODDefines.startTagMask:
        model.numMaterials = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneNumFrames | EPODDefines.startTagMask:
        model.numFrames = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneFlags | EPODDefines.startTagMask:
        model.flags = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneFPS | EPODDefines.startTagMask:
        model.fps = struct.unpack("<i", self.stream.read(4))[0]
        
      elif ident == EPODIdentifiers.eSceneUserData | EPODDefines.startTagMask:
        model.userData = self.stream.read(length)

      elif ident == EPODIdentifiers.eSceneUnits | EPODDefines.startTagMask:
        model.units = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eSceneCamera | EPODDefines.startTagMask:
        print("camera not implemented")
        self.stream.read(length)

      elif ident == EPODIdentifiers.eSceneLight | EPODDefines.startTagMask:
        print("light not implemented")
        self.stream.read(length)

      elif ident == EPODIdentifiers.eSceneMesh | EPODDefines.startTagMask:
        mesh = self.ReadMeshBlock()
        model.meshes.append(mesh)

      elif ident == EPODIdentifiers.eSceneNode | EPODDefines.startTagMask:
        node = self.ReadNodeBlock()
        model.nodes.append(node)

      elif ident == EPODIdentifiers.eSceneTexture | EPODDefines.startTagMask:
        texture = self.ReadTextureBlock()
        model.textures.append(texture)

      elif ident == EPODIdentifiers.eSceneMaterial | EPODDefines.startTagMask:
        material = self.ReadMaterialBlock()
        model.materials.append(material)

      # Skip unimplemented block types
      else:
        self.stream.seek(length, 1)

  def ReadNodeBlock(self):
    node = PVRNode()
    animation = node.animation
    isOldFormat = False

    for (ident, length) in self.ReadTags():
      if ident == EPODIdentifiers.eSceneNode | EPODDefines.endTagMask:
        # do final checks
        return node

      elif ident == EPODIdentifiers.eNodeIndex | EPODDefines.startTagMask:
        node.index = struct.unpack("<i", self.stream.read(4))[0]
      
      elif ident == EPODIdentifiers.eNodeName | EPODDefines.startTagMask:
        node.name = self.ReadString(length)
      
      elif ident == EPODIdentifiers.eNodeMaterialIndex | EPODDefines.startTagMask:
        node.materialIndex = struct.unpack("<i", self.stream.read(4))[0]
      
      elif ident == EPODIdentifiers.eNodeParentIndex | EPODDefines.startTagMask:
        node.parentIndex = struct.unpack("<i", self.stream.read(4))[0]
      
      elif ident == EPODIdentifiers.eNodePosition | EPODDefines.startTagMask: # Deprecated
        pos = np.frombuffer(self.stream.read(length), dtype=np.float32)
        isOldFormat = True;
      
      elif ident == EPODIdentifiers.eNodeRotation | EPODDefines.startTagMask: # Deprecated
        rotation = np.frombuffer(self.stream.read(length), dtype=np.float32)
        isOldFormat = True;
      
      elif ident == EPODIdentifiers.eNodeScale | EPODDefines.startTagMask: # Deprecated
        scale = np.frombuffer(self.stream.read(length), dtype=np.float32)
        isOldFormat = True;
      		
      elif ident == EPODIdentifiers.eNodeMatrix | EPODDefines.startTagMask:	# Deprecated
        matrix = np.frombuffer(self.stream.read(length), dtype=np.float32)
        isOldFormat = True;
      
      elif ident == EPODIdentifiers.eNodeAnimationPosition | EPODDefines.startTagMask:
        animation.positions = np.frombuffer(self.stream.read(length), dtype=np.float32)
      
      elif ident == EPODIdentifiers.eNodeAnimationRotation | EPODDefines.startTagMask:
        animation.rotations = np.frombuffer(self.stream.read(length), dtype=np.float32)
      
      elif ident == EPODIdentifiers.eNodeAnimationScale | EPODDefines.startTagMask:
        animation.scales = np.frombuffer(self.stream.read(length), dtype=np.float32)
      
      elif ident == EPODIdentifiers.eNodeAnimationMatrix | EPODDefines.startTagMask:
        animation.matrices = np.frombuffer(self.stream.read(length), dtype=np.float32)
      
      elif ident == EPODIdentifiers.eNodeAnimationFlags | EPODDefines.startTagMask:
        animation.flags = struct.unpack("<I", self.stream.read(4))[0]
      
      elif ident == EPODIdentifiers.eNodeAnimationPositionIndex | EPODDefines.startTagMask:
        animation.positionIndices = np.frombuffer(self.stream.read(length), dtype=np.uint32)
      
      elif ident == EPODIdentifiers.eNodeAnimationRotationIndex | EPODDefines.startTagMask:
        animation.rotationIndices = np.frombuffer(self.stream.read(length), dtype=np.uint32)
      
      elif ident == EPODIdentifiers.eNodeAnimationScaleIndex | EPODDefines.startTagMask:
        animation.scaleIndices = np.frombuffer(self.stream.read(length), dtype=np.uint32)
      
      elif ident == EPODIdentifiers.eNodeAnimationMatrixIndex | EPODDefines.startTagMask:
        animation.matrixIndices = np.frombuffer(self.stream.read(length), dtype=np.uint32)
      
      elif ident == EPODIdentifiers.eNodeUserData | EPODDefines.startTagMask:
        node.userData = self.stream.read(length)
      
      # skip unkown blocks
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

  def ReadTextureBlock(self):
    texture = PVRTexture()
    for (ident, length) in self.ReadTags():
      if ident == EPODIdentifiers.eSceneTexture | EPODDefines.endTagMask:
        # do final checks
        return texture

      elif ident == EPODIdentifiers.eTextureFilename | EPODDefines.startTagMask:
        texture.name = self.ReadString(length)
        
      # skip unkown blocks
      else:
        self.stream.seek(length, 1)

  def ReadMaterialBlock(self):
    material = PVRMaterial()

    for (ident, length) in self.ReadTags():
      if ident == EPODIdentifiers.eSceneMaterial | EPODDefines.endTagMask:
        # do final checks
        return material

      elif ident == EPODIdentifiers.eMaterialName | EPODDefines.startTagMask:
        material.name = self.ReadString(length)

      elif ident == EPODIdentifiers.eMaterialDiffuseTextureIndex | EPODDefines.startTagMask:
        material.diffuseTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialOpacity | EPODDefines.startTagMask:
        material.opacity = struct.unpack("<f", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialAmbientColour | EPODDefines.startTagMask:
        material.ambient = np.frombuffer(self.stream.read(12), dtype=np.float32)
        
      elif ident == EPODIdentifiers.eMaterialDiffuseColour | EPODDefines.startTagMask:
        material.diffuse = np.frombuffer(self.stream.read(12), dtype=np.float32)

      elif ident == EPODIdentifiers.eMaterialSpecularColour | EPODDefines.startTagMask:
        material.specular = np.frombuffer(self.stream.read(12), dtype=np.float32)

      elif ident == EPODIdentifiers.eMaterialShininess | EPODDefines.startTagMask:
        material.specular = struct.unpack("<f", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialEffectFile | EPODDefines.startTagMask:
        material.effectFile = self.ReadString(length)

      elif ident == EPODIdentifiers.eMaterialEffectName | EPODDefines.startTagMask:
        material.effectName = self.ReadString(length)

      elif ident == EPODIdentifiers.eMaterialAmbientTextureIndex | EPODDefines.startTagMask:
        material.ambientTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialSpecularColourTextureIndex | EPODDefines.startTagMask:
        material.specularColourTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialSpecularLevelTextureIndex | EPODDefines.startTagMask:
        material.specularLevelTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialBumpMapTextureIndex | EPODDefines.startTagMask:
        material.bumpMapTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialEmissiveTextureIndex | EPODDefines.startTagMask:
        material.emissiveTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialGlossinessTextureIndex | EPODDefines.startTagMask:
        material.glossinessTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialOpacityTextureIndex | EPODDefines.startTagMask:
        material.opacityTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialReflectionTextureIndex | EPODDefines.startTagMask:
        material.reflectionTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialRefractionTextureIndex | EPODDefines.startTagMask:
        material.refractionTextureIndex = struct.unpack("<i", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialBlendingRGBSrc | EPODDefines.startTagMask:
        material.blendSrcRGB = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialBlendingAlphaSrc | EPODDefines.startTagMask:
        material.blendSrcA = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialBlendingRGBDst | EPODDefines.startTagMask:
        material.blendDstRGB = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialBlendingAlphaDst | EPODDefines.startTagMask:
        material.blendDstA = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialBlendingRGBOperation | EPODDefines.startTagMask:
        material.blendOpRGB = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialBlendingAlphaOperation | EPODDefines.startTagMask:
        material.blendOpA = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialBlendingRGBAColour | EPODDefines.startTagMask:
        material.blendColour = np.frombuffer(self.stream.read(length), dtype=np.float32)

      elif ident == EPODIdentifiers.eMaterialBlendingFactorArray | EPODDefines.startTagMask:
        material.blendFactor = np.frombuffer(self.stream.read(length), dtype=np.float32)

      elif ident == EPODIdentifiers.eMaterialFlags | EPODDefines.startTagMask:
        material.flags = struct.unpack("<I", self.stream.read(4))[0]

      elif ident == EPODIdentifiers.eMaterialUserData | EPODDefines.startTagMask:
        material.userData = self.stream.read(length)

      # skip unkown blocks
      else:
        self.stream.seek(length, 1)

  def ReadString(self, length):
    return self.stream.read(length).decode("utf-8").strip("\x00")

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
