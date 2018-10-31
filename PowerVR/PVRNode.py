from PowerVR.PVRAnimation import EPVRAnimation, PVRAnimation

class PVRNode:
  def __init__(self):
    self.index = -1
    self.name = ""
    self.materialIndex = -1
    self.parentIndex = -1
    self.animation = PVRAnimation()
    self.userData = None