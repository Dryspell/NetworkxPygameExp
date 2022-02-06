import random

import pandas as pd
import pygame
import networkx as nx
import numpy as np
import pandas
from pyparsing import col

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0,0,0)
SPECIALCOLOR = (255,0,0)

X = 800
Y = 600

def getNodeDataByName(name,nodes):
    for node in nodes:
        if node['name'] == name:
            return node

class Node:
    name = ""
    nodeCoords = ()
    rectCoords = ()
    color = ()
    neighbors = []
    edges = []
    cellSize = 5       

    def __init__(self,name,nodes,matrix,cellSize):
        self.name = name
        self.nodeCoords = ()
        self.rectCoords = ()
        self.color = BLUE
        neighbors = []
        self.cellSize = cellSize

        #generateNeighbors()
        adjData = matrix[self.name]
        adjDF = pd.DataFrame(adjData)
        edgeData = adjDF.loc[adjDF.iloc[:, 0] == 1].index.values
        for edge in edgeData:
            for node in nodes:
                if node.name == edge:
                    self.edges.append(edge)
                    self.neighbors.append(node)
                    node.edges.append(edge)
                    node.neighbors.append(self)
                    # pygame.draw.line(display_surface,BLACK,self.nodeCoords,node.nodeCoords)
                    break
        
    
    def assignRandomPos(self,nodesToAvoid):
        radius = self.cellSize
        nodeInGoodPosition = True
        self.nodeCoords = (float(random.random())*0.9*X + 0.05*X, float(random.random()) * 0.9*Y + 0.05*Y)
        self.rectCoords = (self.nodeCoords[0] + (-0.45 * self.cellSize),
                            self.nodeCoords[1] + (-0.45 * self.cellSize), .9 * self.cellSize,
                            .9 * self.cellSize)
        if len(nodesToAvoid) < 2:
            return
        for j in range(len(nodesToAvoid)):
            distance = np.linalg.norm(np.subtract(nodesToAvoid[j].nodeCoords, self.nodeCoords))
            if distance < radius:
                self.assignRandomPos(nodesToAvoid)
                return

class Widget():
    centerCoords = ()
    checkpoints = []
    vector = ()
    direction = ()
    shift = ()
    minLerpCounter = 0
    counter = minLerpCounter
    maxLerpCounter = 1000
    lerpFrequency = 20
    size = 5
    movement = 10

    triangleCoords = [[1,0],
                    [np.cos(np.pi *(2/3)), np.sin(np.pi*(2/3))],
                    [np.cos(np.pi *(4/3)), np.sin(np.pi*(4/3))]]
    
    def __init__(self,size, movement, checkpoints):
        self.checkpoints = checkpoints
        self.centerCoords = checkpoints[0].nodeCoords
        self.minLerpCounter = 0
        counter = self.minLerpCounter
        self.maxLerpCounter = 1000
        self.lerpFrequency = 20
        self.size = 5
        self.movement = 10

        self.vector = np.subtract(self.checkpoints[0].nodeCoords,self.checkpoints[1].nodeCoords)
        self.direction = self.vector / np.linalg.norm(self.vector)
        self.shift = np.multiply(movement, self.direction)
    
        for i in range(len(self.triangleCoords)):
            self.triangleCoords[i] = [self.triangleCoords[i][0] * size, self.triangleCoords[i][1]*size]
            self.triangleCoords[i] = [self.triangleCoords[i][0] + self.centerCoords[0][0], self.triangleCoords[i][1]+self.centerCoords[0][1]]

    def animateWidget(self):
        raise NotImplementedError

    def updateWidget(self):
        self.counter +=1
        for i in self.triangleCoords:
            for j in self.triangleCoords[i]:
                x = self.triangleCoords[i][j][0]
                y = self.triangleCoords[i][j][1]
                self.triangleCoords[i][j] = pygame.math.Vector2((x,y)).lerp(self.checkpoints[1].nodeCoords,self.counter / self.maxLerpCounter)

    def drawWidget(self,display_surface):
        pygame.draw.polygon(display_surface, BLACK, self.triangleCoords)
class Path():
    parentNodes = []
    pathNodes = {}
    pathEdges = []
    pathWidgets = {}
    animators = []

    def __init__(self,nodes,start=()):
        parentNodes = nodes
        pathNodes = {}
        pathEdges = []
        pathWidgets = {}
        animators = []
        self.addNode(start)
        if (start == ()):
            self.pathNodes[0] = nodes[random.randint(0,len(nodes)-1)]
        print(self.pathNodes)
    
    def getLast(self,negIndex=1):
        return self.pathNodes[len(self.pathNodes)-negIndex]

    def addNode(self,node):
        self.pathNodes[len(self.pathNodes)] = node
        if len(self.pathNodes)>1:
            lastEdge = [self.getLast(1).nodeCoords,self.getLast(2).nodeCoords]
            self.pathEdges.append([self.getLast(1),self.getLast(2)])
            self.pathWidgets[len(self.pathEdges)] = []
            # self.animators.append(animatePath(lastEdge,20,10))
            # self.animators[-1].__next__()

    def randomStep(self):
        print(self.pathNodes)
        nextStep = self.getLast(1).neighbors[random.randint(0,len(self.getLast(1).neighbors)-1)]
        self.addNode(nextStep)
        self.updateColors()

    def updateColors(self):
        for node in self.pathNodes:
            index = self.pathNodes.index(node)
            r = (((index + 1) / len(path))* SPECIALCOLOR[0]) + (((len(path)-index - 1) / len(path))* BLUE[0])
            g = (((index + 1) / len(path))* SPECIALCOLOR[1]) + (((len(path)-index - 1) / len(path))* BLUE[1])
            b = (((index + 1) / len(path))* SPECIALCOLOR[2]) + (((len(path)-index - 1) / len(path))* BLUE[2])
            node.color = (r,g,b)

    def genAnimationWidgets(self, size, movement):
        for edge in self.pathWidgets.index:
            self.pathWidgets[edge].append(Widget(size,movement,edge[0].nodeCoords))

def generateGraph(k):
    dimG = 1
    G = nx.grid_graph(dim=(k, k))
    # G = nx.complete_graph(k)
    matrix = nx.to_pandas_adjacency(G)

    for i in range(int(np.ceil(0.5 * len(matrix)))):
        if i * i >= len(matrix):
            dimG = i
            break

    nodes = []
    for i in range(len(matrix)):
        col = 1 + (i % dimG)
        row = 1 + np.floor(i / dimG)
        cellSize = min(.8 * X, .8 * Y) / dimG

        newNode = Node(matrix.index[i],nodes,matrix,cellSize)
        newNode.assignRandomPos(nodes)
        nodes.append(newNode)
    
    return nodes

def drawGraph(nodes,pathData, display_surface):
    for node in nodes:
        pygame.draw.rect(display_surface, node.color, node.rectCoords)
        for neighbor in node.neighbors:
            pygame.draw.line(display_surface,(0,0,0),node.nodeCoords,neighbor.nodeCoords)

    font = pygame.font.Font('freesansbold.ttf', 32)
    try:
        for index in pathData['path']:
            textLog = font.render(str(pathData['path'][index]['name']), True, BLACK)
            textRect = textLog.get_rect()
            textRect.center = (0.9 * X, (index / len(pathData['path']))* 0.9*Y + 0.05*Y)
            display_surface.blit(textLog, textRect)

            textPathLabel = font.render(str(index), True, WHITE)
            textRect = textPathLabel.get_rect()
            textRect.center = pathData['path'][index]['nodeCoords']
            display_surface.blit(textPathLabel, textRect)

            if index >= 2:
                try:
                    pathData['animators'][index-2].send(None)
                except StopIteration:
                    continue
    except (KeyError):
        return
    # try:
    #     text = font.render(pathData['pathString'], True, WHITE, BLUE)
    #     textRect = text.get_rect()
    #     textRect.center = (0.95*X,0.5*Y)
    #     display_surface.blit(text, textRect)
    # except (KeyError):
    #     return


# def animatePath(nodes, pathData, display_surface, mode):
#     if mode == "LAST":
#
#     if mode == "ALL":
#         for index in pathData:

def drawClock(text, display_surface):
    font = pygame.font.SysFont('Consolas', 30)
    display_surface.blit(font.render(text, True, (0, 0, 0)), (0.15 * X, 0.9 * Y))

def main():
    pygame.init()

    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('GraphTesting')

    pathData = {}
    nodes = generateGraph(10)
    path = Path(nodes)

    clock = pygame.time.Clock()
    counter, text = 10, '10'.rjust(3)
    TAKERANDOMSTEP = 25
    ANIMATESTEP = 26
    pygame.time.set_timer(TAKERANDOMSTEP, 1000)
    pygame.time.set_timer(ANIMATESTEP, 17)

    pause = False

    # infinite loop
    running = True
    while running:
        if not pause and pygame.key.key_code('space') in pygame.key.get_pressed():
            pause = True
        elif pause and pygame.key.key_code('space') in pygame.key.get_pressed():
            pause = False

        # display_surface.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == TAKERANDOMSTEP and not pause:
                path.randomStep()
                # pathData = randomStep(pathData,nodes,display_surface)
                draw()
            if event.type == ANIMATESTEP:
                draw()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        def draw():
            display_surface.fill(WHITE)
            drawClock(text,display_surface)
            drawGraph(nodes,pathData,display_surface)
            pygame.display.flip()

        pygame.display.flip()
        clock.tick(60)

        # pygame.display.update()

main()