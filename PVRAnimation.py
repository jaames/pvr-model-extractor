class EPVRAnimation:
  eHasPositionAnimation = 0x01
  eHasRotationAnimation = 0x02
  eHasScaleAnimation =    0x04
  eHasMatrixAnimation =   0x08

class PVRAnimation:
  def __init__(self):
    self.flags = 0
    self.numFrames = 0
    self.positions = None
    self.rotations = None
    self.scales =    None
    self.matrices =  None
    self.positionIndices = None
    self.rotationIndices = None
    self.scaleIndices =    None
    self.matrixIndices =   None