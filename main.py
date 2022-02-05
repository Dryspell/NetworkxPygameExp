import random

import pandas as pd
import pygame
import networkx as nx
import numpy as np
import pandas

# G = nx.grid_graph(dim=(3,3))
# print(nx.to_pandas_adjacency(G))
# print(nx.to_dict_of_lists(G))
# print(nx.to_dict_of_dicts(G))

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

def generateGraph(k):
    dimG = 1
    G = nx.grid_graph(dim=(k, k))
    # G = nx.complete_graph(k)
    matrix = nx.to_pandas_adjacency(G)

    for i in range(int(np.ceil(0.5 * len(matrix)))):
        if i * i >= len(matrix):
            dimG = i
            # print(dimG)
            break


    nodeData = {'name': "",
                'adjData': "",
                'nodeCoords': (),
                'rectCoords': (),
                'color': "",
                'edgeData' : [],
                'edgeVectors':{}}
    nodes = []

    for i in range(len(matrix)):
        nodeData['name'] = matrix.index[i]
        nodeData['adjData'] = matrix[nodeData['name']]
        col = 1 + (i % dimG)
        row = 1 + np.floor(i / dimG)
        cellSize = min(.8 * X, .8 * Y) / dimG

        # nodeData['nodeCoords'] = ((float(col * cellSize), float(row * cellSize)))
        # nodeData['nodeCoords'] = (float(random.random()) * dimG * cellSize, float(random.random()) * dimG * cellSize)
        def assignRandomPos():
            radius = cellSize
            nodeInGoodPosition = True
            nodeData['nodeCoords'] = (float(random.random())*0.9*X + 0.05*X, float(random.random()) * 0.9*Y + 0.05*Y)
            if len(nodes) < 2:
                return
            for j in range(len(nodes)):
                distance = np.linalg.norm(np.subtract(nodes[j]['nodeCoords'], nodeData['nodeCoords']))
                print(distance)
                if distance < radius:
                    assignRandomPos()
                    return

        assignRandomPos()

        nodeData['rectCoords'] = (nodeData['nodeCoords'][0] + (-0.45 * cellSize),
                                       nodeData['nodeCoords'][1] + (-0.45 * cellSize), .9 * cellSize,
                                       .9 * cellSize)
        nodeData['color'] = BLUE

        adjDF = pd.DataFrame(nodeData['adjData'])
        nodeData['edgeData'] = adjDF.loc[adjDF.iloc[:, 0] == 1].index.values

        nodes.append(nodeData.copy())

    nodesDF = pd.DataFrame(nodes)
    for node in nodes:
        for edge in node['edgeData']:
            node['edgeVectors'][edge] = (node['nodeCoords'], (getNodeDataByName(edge,nodes)['nodeCoords']))
            # print(node['edgeVectors'])
    return nodes

def drawGraph(nodes,pathData, display_surface):
    for node in nodes:
        pygame.draw.rect(display_surface, node['color'], node['rectCoords'])
        for edge in node['edgeData']:
            pygame.draw.line(display_surface,(0,0,0),node['edgeVectors'][edge][0], node['edgeVectors'][edge][1])

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

def animatePath(coords,size,movement, display_surface):
    if len(coords) < 2:
        return

    vector = np.subtract(coords[1],coords[0])
    direction = vector / np.linalg.norm(vector)
    shift = np.multiply(movement, direction)
    # print(shift)

    triangleCoords = [[1,0],
                      [np.cos(np.pi *(2/3)), np.sin(np.pi*(2/3))],
                      [np.cos(np.pi *(4/3)), np.sin(np.pi*(4/3))]]
    # print(triangleCoords)
    for i in range(len(triangleCoords)):
        triangleCoords[i] = [triangleCoords[i][0] * size, triangleCoords[i][1]*size]
        triangleCoords[i] = [triangleCoords[i][0] + coords[0][0], triangleCoords[i][1]+coords[0][1]]

    widgets = {}
    widgets['coords'] = []
    widgets['counters'] = [0]
    widgets['index'] = []
    COUNTERMAX = 1000
    FREQUENCY = 20
    try:
        while True:
            if widgets['counters'][0] % FREQUENCY == 0:
                widgets['counters'].append(0)
                widgets['coords'].append(triangleCoords)
                widgets['index'].append(len(widgets['coords']) - 1)
            for i in range(len(widgets['coords'])):
                for j in range(len(widgets['coords'][i])):
                    x = widgets['coords'][i][j][0]
                    y = widgets['coords'][i][j][1]
                    # print(x,y)
                    widgets['coords'][i][j] = pygame.math.Vector2((x,y)).lerp(coords[1],widgets['counters'][i]/COUNTERMAX)
                    widgets['counters'][i] +=1
                    if widgets['counters'][i] >= COUNTERMAX:
                        return
                    # # print(widget)
                    # for i in range(len(widgets['coords'][k])):
                    #     widgets['coords'][i] = [widgets['coords'][i][0] + shift[0], widgets['coords'][i][1]+shift[1]]
                    # print(widget)
                    pygame.draw.polygon(display_surface, BLACK, widgets['coords'][i])
            (yield)
    except GeneratorExit:
        return

def drawClock(text, display_surface):
    font = pygame.font.SysFont('Consolas', 30)
    display_surface.blit(font.render(text, True, (0, 0, 0)), (0.15 * X, 0.9 * Y))

def randomStep(pathData, nodes, display_surface):
    if not pathData:
        pathData['path'] = {}
        pathData['pathString'] = ""
        pathData['animators'] = []
        pathData['pathCoords'] = []
        hasUnique = False
        for node in nodes:
            if node['color'] == SPECIALCOLOR:
                hasUnique = True
                unique = node
            else:
                node['color'] = BLUE
        if not hasUnique:
            hasUnique = True
            unique = nodes[random.randint(0,len(nodes)-1)]
            unique['color'] = SPECIALCOLOR
            pathData['path'][0] = unique

    else:
        unique = pathData['path'][len(pathData['path'])-1]
        nextStep = getNodeDataByName(unique['edgeData'][random.randint(0,len(unique['edgeData'])-1)],nodes)
        pathData['pathCoords'].append(nextStep['nodeCoords'])
        # print(nextStep)
        pathData['pathString'] += "\n"+str(np.subtract(nextStep['nodeCoords'],unique['nodeCoords']))
        nextStep['color'] = SPECIALCOLOR
        pathData['path'][len(pathData['path'])] = nextStep

    path = pathData['path']
    for index in pathData['path']:
        r = (((index + 1) / len(path))* SPECIALCOLOR[0]) + (((len(path)-index - 1) / len(path))* BLUE[0])
        g = (((index + 1) / len(path))* SPECIALCOLOR[1]) + (((len(path)-index - 1) / len(path))* BLUE[1])
        b = (((index + 1) / len(path))* SPECIALCOLOR[2]) + (((len(path)-index - 1) / len(path))* BLUE[2])
        pathData['path'][index]['color'] = (r,g,b)
    if len(pathData['pathCoords']) > 1:
        lastEdge = [pathData['pathCoords'][-2],pathData['pathCoords'][-1]]

        if len(pathData['animators']) >0:
            pathData['animators'][-1].close()
        pathData['animators'].append(animatePath(lastEdge,20,10,display_surface))
        pathData['animators'][-1].__next__()
    return pathData

def main():
    pygame.init()

    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('GraphTesting')

    # font = pygame.font.Font('freesansbold.ttf', 32)
    # text = font.render('GeeksForGeeks', True, green, blue)
    # textRect = text.get_rect()
    # textRect.center = (X // 2, Y // 2)

    pathData = {}
    nodes = generateGraph(10)

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
                pathData = randomStep(pathData,nodes,display_surface)
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