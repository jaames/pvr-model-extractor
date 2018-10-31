
class EPVRMaterial:
  class BlendFunction:
    eZERO                   = 0
    eONE                    = 1
    eBLEND_FACTOR           = 2
    eONE_MINUS_BLEND_FACTOR = 3

    eSRC_COLOR              = 0x0300
    eONE_MINUS_SRC_COLOR    = 0x0301
    eSRC_ALPHA              = 0x0302
    eONE_MINUS_SRC_ALPHA    = 0x0303
    eDST_ALPHA              = 0x0304
    eONE_MINUS_DST_ALPHA    = 0x0305
    eDST_COLOR              = 0x0306
    eONE_MINUS_DST_COLOR    = 0x0307
    eSRC_ALPHA_SATURATE     = 0x0308

    eCONSTANT_COLOR           = 0x8001
    eONE_MINUS_CONSTANT_COLOR = 0x8002
    eCONSTANT_ALPHA           = 0x8003
    eONE_MINUS_CONSTANT_ALPHA = 0x8004

  class BlendOperation:
    eADD              = 0x8006
    eMIN              = 0x8007
    eMAX              = 0x8008
    eSUBTRACT         = 0x800A
    eREVERSE_SUBTRACT = 0x800B

class PVRMaterial:
  def __init__(self):
    self.name = ""
    self.diffuseTextureIndex        = -1
    self.ambientTextureIndex        = -1
    self.specularTextureIndex       = -1
    self.specularLevelTextureIndex  = -1
    self.bumpMapTextureIndex        = -1
    self.emissiveTextureIndex       = -1
    self.glossinessTextureIndex     = -1
    self.opacityTextureIndex        = -1
    self.reflectionTextureIndex     = -1
    self.refractionTextureIndex     = -1
    self.opacity    = 1
    self.ambient    = None
    self.diffuse    = None
    self.specular   = None
    self.shininess  = 0
    self.effectFile = ""
    self.effectName = ""

    self.blendSrcRGB = EPVRMaterial.BlendFunction.eONE
    self.blendSrcA   = EPVRMaterial.BlendFunction.eONE
    self.blendDstRGB = EPVRMaterial.BlendFunction.eZERO
    self.blendDstA   = EPVRMaterial.BlendFunction.eZERO
    self.blendOpRGB  = EPVRMaterial.BlendOperation.eADD
    self.blendOpA    = EPVRMaterial.BlendOperation.eADD

    self.flags    = 0
    self.userData = None