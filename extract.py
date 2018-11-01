from PowerVR.PVRPODLoader import PVRPODLoader
from GLB.GLBExporter import GLBExporter
import json
import numpy as np

glb = GLBExporter()
pod = PVRPODLoader.open("./test2.pod")

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
  attributes = {}
  numFaces = mesh.primitiveData["numFaces"]
  numVertices = mesh.primitiveData["numVertices"]

  # face index buffer view
  indices = mesh.faces["data"]
  indicesAccessor = glb.addAccessor({
    "bufferView": glb.addBufferView({
      "buffer": 0,
      "byteOffset": glb.addData(indices.tobytes()),
      "byteLength": indices.nbytes,
      "target": 34963
    }),
    "byteOffset": 0,
    # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#accessor-element-size
    "componentType": 5123,
    "count": numFaces * 3,
    "type": "SCALAR"
  })


  # vertex buffer view
  vertexElements = mesh.vertexElements
  print(vertexElements)
  vertexBufferView = glb.addBufferView({
    "buffer": 0,
    "byteOffset": glb.addData(mesh.vertexElementData[0]),
    "byteStride": vertexElements["POSITION0"]["stride"],
    "byteLength": len(mesh.vertexElementData[0]),
  })

  # if "POSITION0" in vertexElements:
  positionAccessor = glb.addAccessor({
    "bufferView": vertexBufferView,
    "byteOffset": 0,
    # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#accessor-element-size
    "componentType": 5126,
    "count": numVertices,
    "type": "VEC3"
  })
  attributes["POSITION"] = positionAccessor

  # if "NORMAL0" in vertexElements:
  normalAccessor = glb.addAccessor({
    "bufferView": vertexBufferView,
    "byteOffset": 12,
    # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#accessor-element-size
    "componentType": 5126,
    "count": numVertices,
    "type": "VEC3"
  })
  attributes["NORMAL"] = normalAccessor

  # if "TANGENT0" in vertexElements:
  tangentAccessor = glb.addAccessor({
    "bufferView": vertexBufferView,
    "byteOffset": 24,
    # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#accessor-element-size
    "componentType": 5126,
    "count": numVertices,
    "type": "VEC3"
  })
  attributes["TANGENT"] = tangentAccessor

  uvAccessor = glb.addAccessor({
    "bufferView": vertexBufferView,
    "byteOffset": 36,
    # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#accessor-element-size
    "componentType": 5126,
    "count": numVertices,
    "type": "VEC2"
  })
  attributes["TEXCOORD_0"] = uvAccessor

  # POD meshes only have one primitive?
  # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#primitive
  glb.addMesh({
    "primitives": [{
      "attributes": attributes,
      "indices": indicesAccessor,
      "mode": 4,
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
      print(mesh.vertexElements)

  # if the node index is -1 it is a root node
  if node.parentIndex == -1:
    glb.addRootNodeIndex(nodeIndex)
  
  glb.addNode(nodeEntry)

# for mesh in scene.meshes:
#   print(mesh.vertexElements)

# print(glb.buildJSON())

glb.save("./test2.glb")