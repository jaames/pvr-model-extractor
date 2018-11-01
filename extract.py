from PowerVR.PVRPODLoader import PVRPODLoader
from GLB.GLBExporter import GLBExporter
import json


glb = GLBExporter()
pod = PVRPODLoader.open("./test2.pod")

scene = pod.scene

for (nodeIndex, node) in enumerate(scene.nodes):
  nodeEntry = {
    "name": node.name,
    "children": [i for (i, node) in enumerate(scene.nodes) if node.parentIndex == nodeIndex],
    "translation": node.animation.positions.tolist(),
    "scale": node.animation.scales[0:3].tolist(),
    "rotation": node.animation.rotations[0:4].tolist(),
  }

  # print(node.animation)
  # if the node has a mesh index
  if node.index != -1: 
    meshIndex = node.index
    mesh = scene.meshes[meshIndex]
    print(mesh.boneBatches)
  # if the node index is -1 it is a root node
  if node.parentIndex == -1:
    glb.addRootNodeIndex(nodeIndex)
  
  glb.addNode(nodeEntry)

# for mesh in scene.meshes:
#   print(mesh.vertexElements)

# print(glb.buildJSON())

glb.save("./test2.glb")