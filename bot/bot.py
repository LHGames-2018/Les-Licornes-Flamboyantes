from helper import *
from random import randint

global GameMap

global calcule

class Bot:
    def __init__(self):
        GameMap = 0
        calcule = 0
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        """
        if(calcule == 0 and GameMap != 0):
            self.Destination = a_star_to(PlayerInfo.Position, Point(currentTilePosition.x, currentTilePosition.y + 2), GameMap)
            calcule = 1
        """
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        """
        curMove = Destination
        while(curMove.origin != null):
            curMove = curMove.origin
        
        create_move_action(Point(curMove.tile.Position.x - PlayerInfo.Position.x, curMove.tile.Position.y - PlayerInfo.Position.y))
        curMove.origin = null
        
        GameMap = gameMap
        """
        
        create_move_action(Point(0, -1))
        # Write your bot here. Use functions from aiHelper to instantiate your actions.
        #return create_move_action(Point(1, 0))

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass

    def findFirstMineral(self, playerInfo):
        mineral = None
        for x in range(self.GameMap.minX, self.GameMap.maxX):
            for y in range(self.GameMap.minY, self.GameMap.maxY):
                tile = self.GameMap.getTileAt(Point(x,y))
                if(tile.TileContent == 4):
                    if(mineral == None):
                        mineral = tile.Position
                    elif(Point.Distance(playerInfo.Position, tile.Position) < mineral):
                        mineral = tile.Position

        return mineral
						

    def calc_heuristic(self, case, endPoint):
        if(case.tile.TileContent == 0):
            return Point.Distance(Point(case.tile.Position.x, case.tile.Position.y), endPoint)
        else:
            return 100000000000000;

    
    def a_star_to(self, endPoint, gameMap):
        open_list = {}
        closed_list = {}
        
        currentTilePosition = self.PlayerInfo.position
        
        while(currentTilePosition is not endPoint):
            
            print(currentTilePosition.x + " " + currentTilePosition.y)
            
            curCase = Case(currentTilePosition, closed_list[len(closed_list)] if len(closed_list) != 0 else None)
            
            caseHaut = Case(gameMap.getTileAt(Point(currentTilePosition.x, currentTilePosition.y - 1)),
                            curCase)
            caseBas = Case(gameMap.getTileAt(Point(currentTilePosition.x, currentTilePosition.y + 1)),
                            curCase)
            caseGauche = Case(gameMap.getTileAt(Point(currentTilePosition.x - 1, currentTilePosition.y)),
                              curCase)
            caseDroite = Case(gameMap.getTileAt(Point(currentTilePosition.x + 1, currentTilePosition.y)),
                              curCase)
            
            self.calc_heuristic(caseHaut, endPoint)
            self.calc_heuristic(caseBas, endPoint)
            self.calc_heuristic(caseGauche, endPoint)
            self.calc_heuristic(caseDroite, endPoint)
            
            if(caseHaut.tile in open_list):
                if(open_list[caseHaut.tile].cost < caseHaut.cost):
                    open_list[caseHaut.tile] = caseHaut
            else:
                open_list[caseHaut.tile] = caseHaut
            
            if(caseBas.tile in open_list):
                if(open_list[caseBas.tile].cost < caseBas.cost):
                    open_list[caseBas.tile] = caseBas
            else:
                open_list[caseBas.tile] = caseBas
                
            if(caseGauche.tile in open_list):
                if(open_list[caseGauche.tile].cost < caseGauche.cost):
                    open_list[caseGauche.tile] = caseGauche
            else:
                open_list[caseGauche.tile] = caseGauche
                
            if(caseDroite.tile in open_list):
                if(open_list[caseDroite.tile].cost < caseDroite.cost):
                    open_list[caseDroite.tile] = caseDroite
            else:
                open_list[caseDroite.tile] = caseDroite
            
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
        

class Case:
    def __init__(self, tile, origin):
        self.tile = tile
        self.origin = 0
        self.cost = 0
