from PowerVR.EPOD import *

class PVRModel:
  def __init__(self):
    self.clearColour = None
    self.ambientColour = None

    self.numCameras = 0
    self.cameras = []

    self.numLights = 0
    self.lights = []

    self.numMeshes = 0
    self.meshes = []

    self.numNodes = 0
    self.numMeshNodes = 0
    self.nodes = []

    self.numTextures = 0
    self.textures = []

    self.numMaterials = 0
    self.materials = []

    self.numFrames = 0
    self.currentFrame = 0
    self.fps = 0

    self.userData = None

    self.units = 0.0
    self.flags = 0

    self.cache = {}

  def InitCache():
    self.cache["worldMatrixFrameZero"] = []
    self.cache["cachedFrame"] = []
    self.cache["worldMatrixFrameN"] = []
    self.cache["frame"] = 0
    self.cache["frameFraction"] = 0.0
    self.FlushCache()
  
  def FlushCache():
    self.setCurrentFrame(0)
    # for i in range(1, self.numNodes):
    #   m = self.getWorldMatrixNoCache(i)
    #   self.cache["worldMatrixFrameZero"][i] = m
    #   self.cache["worldMatrixFrameN"][i] = m
    #   self.cache["cachedFrame"][i] = 0.0
  
  def setCurrentFrame(frame):
    pass