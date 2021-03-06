#!/usr/bin/env python
# -*- coding: utf-8 -*- 
class KMean:
    def __init__(self):
        """Attributes
            delta -- 判定两点重合的最小距离
            distance -- 计算两点距离
            center --- 计算一组点的中心
        """
        self.delta = 0.001
        #需要用户实现
        def distance(p1,p2):
            raise KMeanError('Not implemented: distance')  
            
        def center(points):
            raise KMeanError('Not implemented: center')
        self.distance = distance
        self.center = center
        
    def run(self,points,k,seeds):
        """执行划分，并返回划分的信息，直接调用此方法返回最终结果
        Param:
            points -- 需要划分的点的数组[p1,p2,p3,...]
            k -- 参数k，分成k个区域
            seeds -- 种子点的数组[s1,s2,...]，seeds中的点和points中的点为统一数据类型。len(seeds) == k
        Return: 
            返回划分好的节点列表，类型如：[(p1,p2,..),(p3,p4,..),..]
        """   
        #迭代种子
        iterSeeds = list(seeds)
        #是否继续迭代
        flag = True
        #划分后的分组
        groups = []
        while flag:
            groupIndexs = self._runOnce(points,k,iterSeeds)
            groups = [[points[index] for index in group] for group in groupIndexs]
            tmpSeeds = []
            for group in groups:
                if len(group) != 0:
                    tmpSeeds.append(self.center(group))
                else:
                    tmpSeeds.append(iterSeeds[groups.index(group)])
            flag = False
            for i in range(len(iterSeeds)):
                if self.distance(iterSeeds[i],tmpSeeds[i]) > self.delta:
                    flag = True
                    break
            iterSeeds = tmpSeeds
        return groups           
        

    def _runOnce(self,points,k,seeds):
        """执行一次划分，并返回分类的信息
        Param:
            points -- 需要划分的点的数组[p1,p2,p3,...],数组的每个元素都要实现distance方法来确定和另外一个点的距离
                如：p1.distance(p2)返回p1 到 p2 的距离
            k -- 参数k，分成k个区域
            seeds -- 种子点的数组[s1,s2,...]，seeds中的点和points中的点为统一数据类型。len(seeds) == k
        Return: 
            返回划分好的节点列表，类型如：[[p1_index,p2_index,..],[p3_index,p4_index,..],..],每个划分里存储的是位置
        """
        if not k == len(seeds):
            raise KMeanError('k must equals len(seeds)')
        #存放划分结果的数组，长度为k，初始化都为空
        groups = [[] for x in range(k)]
        for i in range(len(points)):
            pos = self._minDistancePoint(points[i],seeds)
            groups[pos].append(i)
        return groups
        
        
    
    def _minDistancePoint(self,point,points):
        """找出points中离point最近的点
        Return
            最近的点所在的位置.
        """    
        if len(points) <= 0:
            raise KMeanError('len(points must > 0)')
        #minDistance: 目前最近的点的距离
        #minPos: 目前最近点在数组中的位置
        minDistance = 0
        minPos = -1
        for i in range(len(points)):
            tpoint = points[i]
            tdistance = self.distance(tpoint,point)
            if minPos == -1 or tdistance < minDistance:
                minDistance = tdistance
                minPos = i
        return minPos
         
            
class KMeanError(Exception):
    """
        Attributes:
            message -- 错误信息            
    """
    def __init__(self,message = ''):
        self.message = message
        
