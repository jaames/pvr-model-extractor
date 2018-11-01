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
  indicesAccessorIndex = glb.addAccessor({
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
  vertexBufferView = glb.addBufferView({
    "buffer": 0,
    "byteOffset": glb.addData(mesh.vertexElementData[0]),
    "byteStride": vertexElements["POSITION"]["stride"],
    "byteLength": len(mesh.vertexElementData[0]),
  })

  for name in vertexElements:
    element = vertexElements[name]
    componentType = 5126
    type = "VEC3"
    
    if name == "TEXCOORD_0":
      type = "VEC2"
    
    elif name == "COLOR_0": # not implemented
      continue

    accessorIndex = glb.addAccessor({
      "bufferView": vertexBufferView,
      "byteOffset": element["offset"],
      # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#accessor-element-size
      "componentType": componentType,
      "count": numVertices,
      "type": type
    })
    attributes[name] = accessorIndex

  # POD meshes only have one primitive?
  # https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#primitive
  glb.addMesh({
    "primitives": [{
      "attributes": attributes,
      "indices": indicesAccessorIndex,
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

  # if the node index is -1 it is a root node
  if node.parentIndex == -1:
    glb.addRootNodeIndex(nodeIndex)
  
  glb.addNode(nodeEntry)

# for mesh in scene.meshes:
#   print(mesh.vertexElements)

# print(glb.buildJSON())

glb.save("./test2.glb")