class AffineTrans(object):
    disExtent = [0,0,0,0]  #视图范围
    winExtent = [0,0]      #窗口范围
    scale = 1              #缩放比例

    def calcScale(self, disExt, winExt):
        self.disExtent = disExt
        self.winExtent = winExt    
        sx = (self.disExtent[2]-self.disExtent[0])*1.0/(self.winExtent[0])
        sy = (self.disExtent[3]-self.disExtent[1])*1.0/(self.winExtent[1])
        self.scale = sx if sx > sy else sy

    def D2L(self, x, y):
        point = [0, 0]
        point[0] = float(self.disExtent[0] + self.scale * x)
        point[1] = float(self.disExtent[1] + self.scale * y)
        return point

    def L2D(self, x, y):
        point = [0, 0]
        point[0] = int((x-self.disExtent[0])/self.scale)
        point[1] = int((y-self.disExtent[1])/self.scale)
        return point
