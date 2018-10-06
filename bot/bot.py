from helper import *
from random import randint



class Bot:


    def __init__(self):

        self.MAP_KEY = "map"
        #StorageHelper.write(self.MAP_KEY, 0)
        self.state = 0
        self.miniGameMap = None
        self.gameMap = None
        #= StorageHelper.read(self.MAP_KEY)
        if self.gameMap == None:
            self.gameMap = {}


    def before_turn(self, playerInfo):
        self.PlayerInfo = playerInfo
        
        if(self.state == 0 and self.miniGameMap != None):

            self.targetTile = self.findFirstMineral(self.PlayerInfo)

            print("" + str(self.targetTile.x) + " " + str(self.targetTile.y))
            print("" + str(self.PlayerInfo.Position.x) + " " + str(self.PlayerInfo.Position.y))

            self.destination = self.a_star_to(self.targetTile, self.miniGameMap)
            self.state = 1
        elif(self.state == 2):
            self.targetTile = self.find_house()
            self.destination = self.a_star_to(self.targetTile, self.miniGameMap)
            self.state = 3

    def execute_turn(self, gameMap, visiblePlayers):
        self.miniGameMap = gameMap
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
        for i in range(self.miniGameMap.xMin, self.miniGameMap.xMin + 20):
            if not i in self.gameMap:
                self.gameMap[i] = {}
            for j in range(self.miniGameMap.yMin, self.miniGameMap.yMin + 20):
                self.gameMap[i][j] = self.miniGameMap.getTileAt(Point(i, j))
        #StorageHelper.write(self.MAP_KEY, self.gameMap)
        """
        Gets called after executeTurn
        """
        pass

    def findFirstMineral(self, playerInfo):
        mineral = None
        for x in range(self.miniGameMap.xMin, self.miniGameMap.xMax):
            for y in range(self.miniGameMap.yMin, self.miniGameMap.yMax):
                tile = self.miniGameMap.getTileAt(Point(x,y))
                if(tile.TileContent == TileContent.Resource):
                    if(mineral == None):
                        mineral = tile.Position
                    elif(Point.Distance(playerInfo.Position, tile.Position) < Point.Distance(playerInfo.Position, mineral)):
                        mineral = tile.Position

        return mineral
						

    def calc_heuristic(self, case, endPoint):
        case.cost = (endPoint.x - case.tile.Position.x) + (endPoint.y - case.tile.Position.y)

    
    def a_star_to(self, endPoint, gameMap):
        open_list = {}
        closed_list = {}
        
        currentTilePosition = self.PlayerInfo.Position

        while(currentTilePosition.x != endPoint.x or currentTilePosition.y != endPoint.y):


            print("" + str(currentTilePosition.x) + " " + str(currentTilePosition.y))
            
            nextCases = []
            
            curCase = Case(currentTilePosition, None if len(closed_list) < 1 else closed_list[len(closed_list) - 2])
            
            # Les cases adjacentes
            nextCases.append(Case(gameMap.getTileAt(Point(currentTilePosition.x, currentTilePosition.y - 1)),
                            curCase))
            nextCases.append(Case(gameMap.getTileAt(Point(currentTilePosition.x, currentTilePosition.y + 1)),
                            curCase))
            nextCases.append(Case(gameMap.getTileAt(Point(currentTilePosition.x - 1, currentTilePosition.y)),
                              curCase))
            nextCases.append(Case(gameMap.getTileAt(Point(currentTilePosition.x + 1, currentTilePosition.y)),
                              curCase))
            
            for case in nextCases:
                # Calcul heuristique
                self.calc_heuristic(case, endPoint)
            
                # Ajout ou modification
                if(case.tile in open_list):
                    if(open_list[case.tile].cost < case.cost):
                        open_list[case.tile] = case
                else:
                    if(case.tile.TileContent == TileContent.Empty or case.tile.TileContent == TileContent.House):
                        open_list[case.tile] = case
            
            lowest_cost = 100000000000000
            next_case = 0
            for case in open_list:
                if(open_list[case].cost < lowest_cost):
                    lowest_cost = open_list[case].cost
                    next_case = open_list[case]
            
            del open_list[next_case.tile]
            closed_list[len(closed_list) - 1] = next_case
            
            currentTilePosition = next_case.tile.Position
        
        return closed_list[len(closed_list) - 1]

    def find_house(self):
        minPosX = self.PlayerInfo.Position.x - 10
        minPosY = self.PlayerInfo.Position.y - 10
        
        for i in range(minPosX, minPosX + 20):
            for j in range(minPosY, minPosY + 20):
                    if(self.miniGameMap.getTileAt(i, j).TileContent == TileContent.House):
                        return self.miniGameMap.getTileAt(i, j)
        

class Case:
    def __init__(self, tile, origin):
        self.tile = tile
        self.origin = 0
        self.cost = 0
