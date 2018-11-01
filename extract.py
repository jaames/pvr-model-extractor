from PowerVR.PVRPODLoader import PVRPODLoader
from GLB.GLBExporter import GLBExporter
import json
import numpy as np

glb = GLBExporter()
pod = PVRPODLoader.open("./test.pod")

scene = pod.scene

for (materialIndex, material) in enumerate(scene.materials):
  glb.addMaterial({
    "name": material.name,
    "pbrMetallicRoughness": {
      "baseColorFactor": material.diffuse.tolist() + [1],
      "roughnessFactor": 1 - material.shininess,
    }
  })

for (meshIndex, mesh) in enumerate(scene.meshes):
  # POD meshes only have one primitive?
  # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#primitive
  attributes = {}
  indices = 0
  # change to 4 for tris
  mode = 4

  # face buffer view
  faceData = mesh.faces["data"]
  dataOffset = glb.addData(faceData.tobytes())
  numFaces = mesh.primitiveData["numFaces"]

  bufferViewIndex = glb.addBufferView({
    "buffer": 0,
    "byteOffset": dataOffset,
    "byteLength": faceData.nbytes,
    "target": 34963
  })

  accessorIndex = glb.addAccessor({
    "bufferView": bufferViewIndex,
    "byteOffset": 0,
    # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#accessor-element-size
    "componentType": 5123,
    "count": numFaces * 3,
    "type": "SCALAR"
  })
  indices = accessorIndex

  # vert POSITION buffer view
  positionData = mesh.vertexElements["POSITION0"]
  dataOffset = glb.addData(mesh.vertexElementData[0])
  numVertices = mesh.primitiveData["numVertices"]

  bufferViewIndex = glb.addBufferView({
    "buffer": 0,
    "byteOffset": dataOffset,
    "byteStride": positionData["stride"],
    "byteLength": len(mesh.vertexElementData[0]),
  })

  # vert POSITION accessor
  accessorIndex = glb.addAccessor({
    "bufferView": bufferViewIndex,
    "byteOffset": 0,
    # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#accessor-element-size
    "componentType": 5126,
    "count": numVertices,
    "type": "VEC3"
  })

  attributes["POSITION"] = accessorIndex

  glb.addMesh({
    "primitives": [{
      "attributes": attributes,
      "indices": indices,
      "mode": mode,
    }],
  })

for (nodeIndex, node) in enumerate(scene.nodes):
  nodeEntry = {
    "name": node.name,
    "children": [i for (i, node) in enumerate(scene.nodes) if node.parentIndex == nodeIndex],
    "translation": node.animation.positions.tolist(),
    "scale": node.animation.scales[0:3].tolist(),
    "rotation": node.animation.rotations[0:4].tolist(),
  }
  # if the node has a mesh index
  if node.index != -1: 
    meshIndex = node.index
    nodeEntry["mesh"] = meshIndex
    if node.materialIndex != -1:
      glb.meshes[meshIndex]["primitives"][0]["material"] = node.materialIndex
    
    if node.name == "headwear0002":
      mesh = scene.meshes[meshIndex]
      faceData = mesh.faces["data"]
      print(faceData.nbytes)
      print(mesh.vertexElements["POSITION0"])
      print(mesh.primitiveData["numFaces"])

  # if the node index is -1 it is a root node
  if node.parentIndex == -1:
    glb.addRootNodeIndex(nodeIndex)
  
  glb.addNode(nodeEntry)

# for mesh in scene.meshes:
#   print(mesh.vertexElements)

# print(glb.buildJSON())

glb.save("./test.glb")