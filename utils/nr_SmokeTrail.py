import maya.cmds as cmds

def smokeTrail():
    # creating a control and emitter for trail
    smokeTrailCtrl = cmds.circle(nr=[0, 1, 0], n='smokeTrail_ctrl')
    cmds.select(cl=True)
    trailEmitter = cmds.emitter(n="smokeTrailEmitter")
    cmds.parent(trailEmitter[0], smokeTrailCtrl[0])

    # creating particles and nucleus
    trailParticle = cmds.nParticle(n="trailParticle")
    nucleus = "nucleus1"

    cmds.connectDynamic(trailParticle[0], em=trailEmitter[0])

    # setting up emitter
    cmds.setAttr(trailEmitter[0] + ".visibility", 0)
    cmds.setAttr(trailEmitter[0] + ".rate", 500)

    # setting up particles
    cmds.setAttr(trailParticle[0] + "Shape.lifespanMode", 1)
    cmds.setAttr(trailParticle[0] + "Shape.particleRenderType", 8)
    cmds.setAttr(trailParticle[0] + "Shape.collide", 0)
    cmds.setAttr(trailParticle[0] + "Shape.radius", .5)

    # setting up nucleus
    cmds.setAttr(nucleus + ".gravity", 0)
    cmds.setAttr(nucleus + ".airDensity", 10)
    cmds.setAttr(nucleus + ".windDirectionX", 0)

    # adding additional attr on ctrl
    cmds.addAttr(smokeTrailCtrl[0], longName="trail", attributeType="enum", enumName="__________:")
    cmds.setAttr(smokeTrailCtrl[0] + ".trail", e=True, cb=True)

    cmds.addAttr(smokeTrailCtrl[0], ln="trailRadius", at="double", min=0, dv=.5)
    cmds.setAttr(smokeTrailCtrl[0] + ".trailRadius", e=True, k=True)

    cmds.addAttr(smokeTrailCtrl[0], ln="trailLength", at="double", min=0, dv=1)
    cmds.setAttr(smokeTrailCtrl[0] + ".trailLength", e=True, k=True)

    cmds.addAttr(smokeTrailCtrl[0], ln="trailVisibility", at="enum", enumName="off:on:", dv=1)
    cmds.setAttr(smokeTrailCtrl[0] + ".trailVisibility", e=True, k=True)


    # connecting new attrs
    cmds.connectAttr(smokeTrailCtrl[0] + ".trailRadius", trailParticle[0] + "Shape.radius", f=True)
    cmds.connectAttr(smokeTrailCtrl[0] + ".trailLength", trailParticle[0] + "Shape.lifespan", f=True)
    cmds.connectAttr(smokeTrailCtrl[0] + ".trailVisibility", trailParticle[0] + ".visibility", f=True)
    
    # cleaning up
    cmds.group(smokeTrailCtrl[0], trailParticle[0], nucleus, name="smokeTrail_GRP")

smokeTrail()
