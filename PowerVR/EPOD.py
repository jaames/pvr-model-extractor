class EPODDefines:
  startTagMask = 0x0
  endTagMask   = 0x80000000
  tagMash      = 0x80000000
  PODFormatVersion = "AB.POD.2.0"
  PODFormatVersionLen = 11

class EPODErrorCodes:
  eNoError             = 0
  eFileNotFound        = 1
  eFileVersionMismatch = 2
  eFileStreamError     = 3
  eKeyAlreadyExists    = 4
  eUnknown             = 5

class EPODIdentifiers: 
	eFormatVersion  = 1000
	eScene          = 1001
	eExportOptions  = 1002
	eHistory        = 1003
	eEndiannessMismatch = -402456576
  
	# Scene
	eSceneClearColour	   = 2000
	eSceneAmbientColour  = 2001
	eSceneNumCameras     = 2002
	eSceneNumLights      = 2003
	eSceneNumMeshes      = 2004
	eSceneNumNodes       = 2005
	eSceneNumMeshNodes   = 2006
	eSceneNumTextures    = 2007
	eSceneNumMaterials   = 2008
	eSceneNumFrames      = 2009
	eSceneCamera         = 2010
	eSceneLight          = 2011
	eSceneMesh           = 2012
	eSceneNode           = 2013
	eSceneTexture        = 2014
	eSceneMaterial       = 2015
	eSceneFlags          = 2016
	eSceneFPS            = 2017
	eSceneUserData       = 2018
	eSceneUnits          = 2019

	# Materials
	eMaterialName                       = 3000
	eMaterialDiffuseTextureIndex        = 3001
	eMaterialOpacity                    = 3002
	eMaterialAmbientColour              = 3003
	eMaterialDiffuseColour              = 3004
	eMaterialSpecularColour             = 3005
	eMaterialShininess                  = 3006
	eMaterialEffectFile                 = 3007
	eMaterialEffectName                 = 3008
	eMaterialAmbientTextureIndex        = 3009
	eMaterialSpecularColourTextureIndex = 3010
	eMaterialSpecularLevelTextureIndex  = 3011
	eMaterialBumpMapTextureIndex        = 3012
	eMaterialEmissiveTextureIndex       = 3013
	eMaterialGlossinessTextureIndex     = 3014
	eMaterialOpacityTextureIndex        = 3015
	eMaterialReflectionTextureIndex     = 3016
	eMaterialRefractionTextureIndex     = 3017
	eMaterialBlendingRGBSrc             = 3018
	eMaterialBlendingAlphaSrc           = 3019
	eMaterialBlendingRGBDst             = 3020
	eMaterialBlendingAlphaDst           = 3021
	eMaterialBlendingRGBOperation       = 3022
	eMaterialBlendingAlphaOperation     = 3023
	eMaterialBlendingRGBAColour         = 3024
	eMaterialBlendingFactorArray        = 3025
	eMaterialFlags                      = 3026
	eMaterialUserData                   = 3027

	# Textures
	eTextureFilename				    = 4000

	# Nodes
	eNodeIndex				           = 5000
	eNodeName                    = 5001
	eNodeMaterialIndex           = 5002
	eNodeParentIndex             = 5003
	eNodePosition                = 5004
	eNodeRotation                = 5005
	eNodeScale                   = 5006
	eNodeAnimationPosition       = 5007
	eNodeAnimationRotation       = 5008
	eNodeAnimationScale          = 5009
	eNodeMatrix                  = 5010
	eNodeAnimationMatrix         = 5011
	eNodeAnimationFlags          = 5012
	eNodeAnimationPositionIndex  = 5013
	eNodeAnimationRotationIndex  = 5014
	eNodeAnimationScaleIndex     = 5015
	eNodeAnimationMatrixIndex    = 5016
	eNodeUserData                = 5017

	# Mesh
	eMeshNumVertices			       = 6000
	eMeshNumFaces                = 6001
	eMeshNumUVWChannels          = 6002
	eMeshVertexIndexList         = 6003
	eMeshStripLength             = 6004
	eMeshNumStrips               = 6005
	eMeshVertexList              = 6006
	eMeshNormalList              = 6007
	eMeshTangentList             = 6008  
	eMeshBinormalList            = 6009
	eMeshUVWList                 = 6010
	eMeshVertexColourList        = 6011
	eMeshBoneIndexList           = 6012
	eMeshBoneWeightList          = 6013
	eMeshInteravedDataList       = 6014
	eMeshBoneBatchIndexList      = 6015
	eMeshNumBoneIndicesPerBatch  = 6016
	eMeshBoneOffsetPerBatch      = 6017
	eMeshMaxNumBonesPerBatch     = 6018
	eMeshNumBoneBatches          = 6019
	eMeshUnpackMatrix            = 6020

	# Light
	eLightTargetObjectIndex		     = 7000
	eLightColour                   = 7001
	eLightType                     = 7002
	eLightConstantAttenuation      = 7003
	eLightLinearAttenuation        = 7004
	eLightQuadraticAttenuation     = 7005
	eLightFalloffAngle             = 7006
	eLightFalloffExponent          = 7007

	# Camera
	eCameraTargetObjectIndex	     = 8000
	eCameraFOV                     = 8001
	eCameraFarPlane                = 8002
	eCameraNearPlane               = 8003
	eCameraFOVAnimation            = 8004

	# Mesh data block
	eBlockDataType			    = 9000
	eBlockNumComponents     = 9001
	eBlockStride            = 9002
	eBlockData              = 9003
