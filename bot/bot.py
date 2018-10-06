from helper import *
from random import randint



class Bot:
    def __init__(self):
        self.state = 0
        self.gameMap = 0

    def before_turn(self, playerInfo):
        self.PlayerInfo = playerInfo
        
        if(self.state == 0 and self.gameMap != 0):
            self.targetTile = find_house()
            self.destination = a_star_to(self.PlayerInfo.Position, Point(self.targetTile.Position.x, self.targetTile.Position.y))
            self.state = 1
        elif(self.state == 2):
            self.targetTile = find_house()
            self.destination = a_star_to(self.PlayerInfo.Position, Point(self.targetTile.Position.x, self.targetTile.Position.y))
            self.state = 3

    def execute_turn(self, gameMap, visiblePlayers):
        self.gameMap = gameMap
        
        if(self.state == 1):
            curMove = self.destination
            if(self.destination.origin == None):
                self.state = 2
                return create_collect_action(Point(self.destination.x - self.PlayerInfo.Position.x, self.destination.y - self.PlayerInfo.Position.y))
            while(curMove.origin != None):
                curMove = curMove.origin
                curMove.origin = None
                return create_move_action(Point(curMove.tile.Position.x - self.PlayerInfo.Position.x, curMove.tile.Position.y - self.PlayerInfo.Position.y))
        
        elif(self.state == 3):
            curMove = destination
            if(destination.origin == None):
                self.state = 0
                return create_move_action(Point(destination.tile.Position.x - PlayerInfo.Position.x, destination.tile.Position.y - PlayerInfo.Position.y))
            while(curMove.origin != None):
                curMove = curMove.origin
                curMove.origin = None
                return create_move_action(Point(curMove.tile.Position.x - PlayerInfo.Position.x, curMove.tile.Position.y - PlayerInfo.Position.y))


    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass

    def findFirstMineral(self, playerInfo):
        mineral = None
        for x in range(self.gameMap.minX, self.gameMap.maxX):
            for y in range(self.gameMap.minY, self.gameMap.maxY):
                tile = self.gameMap.getTileAt(Point(x,y))
                if(tile.TileContent == 4):
                    if(mineral == None):
                        mineral = tile.Position
                    elif(Point.Distance(playerInfo.Position, tile.Position) < mineral):
                        mineral = tile.Position

        return mineral
						

    def calc_heuristic(self, case, endPoint):
        case.cost = (endPoint.Position.x - case.tile.Position.x) + (endPoint.Position.y - case.tile.Position.y)

    
    def a_star_to(self, endPoint, gameMap):
        open_list = {}
        closed_list = {}
        
        currentTilePosition = self.PlayerInfo.position
        
        while(currentTilePosition != endPoint):
            
            print(currentTilePosition.x + " " + currentTilePosition.y)
            
            nextCases = []
            
            curCase = Case(currentTilePosition, closed_list[len(closed_list)] if len(closed_list) != 0 else null)
            
            # Les cases adjacentes
            nextCases[0] = Case(gameMap.getTileAt(Point(currentTilePosition.x, currentTilePosition.y - 1)),
                            curCase)
            nextCases[1] = Case(gameMap.getTileAt(Point(currentTilePosition.x, currentTilePosition.y + 1)),
                            curCase)
            nextCases[2] = Case(gameMap.getTileAt(Point(currentTilePosition.x - 1, currentTilePosition.y)),
                              curCase)
            nextCases[3] = Case(gameMap.getTileAt(Point(currentTilePosition.x + 1, currentTilePosition.y)),
                              curCase)
            
            for case in nextCases:
                # Calcul heuristique
                self.calc_heuristic(case, endPoint)
            
                # Ajout ou modification
                if(case.tile in open_list):
                    if(open_list[case.tile].cost < case.cost):
                        open_list[case.tile] = case
                else:
                    if(case.tile.TileContents == TileContents.Empty or case.tile.TileContents == TileContents.House):
                        open_list[case.tile] = case
            
            lowest_cost = 100000000000000
            next_case = 0
            for case in open_list:
                if(case.cost < lowest_cost):
                    lowest_cost = case.cost
                    next_case = case
            
            del open_list[next_case.tile]
            closed_list[len(closed_list)] = next_case
            
            currentTilePosition = next_case.tile.Position
        
        return closed_list[len(closed_list)]

    def find_house(self):
        minPosX = self.PlayerInfo.Position.x - 10
        minPosY = self.PlayerInfo.Position.y - 10
        
        for i in range(minPosX, minPosX + 20):
            for j in range(minPosY, minPosY + 20):
                    if(self.gameMap.getTileAt(i, j).TileContent == TileContent.House):
                        return self.gameMap.getTileAt(i, j)
        

class Case:
    def __init__(self, tile, origin):
        self.tile = tile
        self.origin = 0
        self.cost = 0
