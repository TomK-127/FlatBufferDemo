# automatically generated by the FlatBuffers compiler, do not modify

# namespace: GalaxyMap

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class SpaceObject(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = SpaceObject()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsSpaceObject(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # SpaceObject
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # SpaceObject
    def Id(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # SpaceObject
    def Surface(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from GalaxyMap.SurfacePoint import SurfacePoint
            obj = SurfacePoint()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # SpaceObject
    def SurfaceLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # SpaceObject
    def SurfaceIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # SpaceObject
    def Distance(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def SpaceObjectStart(builder): builder.StartObject(3)
def Start(builder):
    return SpaceObjectStart(builder)
def SpaceObjectAddId(builder, id): builder.PrependInt32Slot(0, id, 0)
def AddId(builder, id):
    return SpaceObjectAddId(builder, id)
def SpaceObjectAddSurface(builder, surface): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(surface), 0)
def AddSurface(builder, surface):
    return SpaceObjectAddSurface(builder, surface)
def SpaceObjectStartSurfaceVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def StartSurfaceVector(builder, numElems):
    return SpaceObjectStartSurfaceVector(builder, numElems)
def SpaceObjectAddDistance(builder, distance): builder.PrependFloat32Slot(2, distance, 0.0)
def AddDistance(builder, distance):
    return SpaceObjectAddDistance(builder, distance)
def SpaceObjectEnd(builder): return builder.EndObject()
def End(builder):
    return SpaceObjectEnd(builder)