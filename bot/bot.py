from helper import *
from random import randint


class Bot:

    def __init__(self):

        self.MAP_KEY = "map"
        # StorageHelper.write(self.MAP_KEY, 0)
        self.state = 0
        self.miniGameMap = None
        self.gameMap = None
        self.index = -2
        self.mineralTile = None
        # = StorageHelper.read(self.MAP_KEY)
        if self.gameMap == None:
            self.gameMap = {}

    def before_turn(self, playerInfo):
        self.PlayerInfo = playerInfo

        if (self.state == 0 and self.miniGameMap != None):

            self.targetTile = self.findFirstMineral(self.PlayerInfo)

            print("" + str(self.targetTile.x) + " " + str(self.targetTile.y))
            print("" + str(self.PlayerInfo.Position.x) + " " + str(self.PlayerInfo.Position.y))

            self.destination = self.a_star_to(self.targetTile, self.miniGameMap)
            self.state = 1
        elif (self.state == 2):
            self.targetTile = self.PlayerInfo.HouseLocation
            self.destination = self.a_star_to(self.targetTile, self.miniGameMap)
            self.state = 3

    def execute_turn(self, gameMap, visiblePlayers):
        self.miniGameMap = gameMap

        if (self.state == 1):
            self.index = self.index + 1

            if (self.index == len(self.destination) - 1):
                self.mineralTile = self.destination[self.index - 1]
                self.state = 10
                self.index = -2
            else:
                curMove = self.destination[self.index]
                print(str(self.destination[self.index].tile.Position.x) + " " + str(
                    self.destination[self.index].tile.Position.y))
                print(str(len(self.destination)))
                return create_move_action(Point(curMove.tile.Position.x - self.PlayerInfo.Position.x,
                                                curMove.tile.Position.y - self.PlayerInfo.Position.y))

        elif (self.state == 3):
            self.index = self.index + 1
            if (self.index == len(self.destination) - 1):
                self.state = 0
                temp = create_move_action(
                    Point(self.destination[self.index - 1].tile.Position.x - self.PlayerInfo.Position.x,
                          self.destination[self.index - 1].tile.Position.y - self.PlayerInfo.Position.y))
                self.index = -2
                return temp
            else:
                curMove = self.destination[self.index]
                print(str(self.destination[self.index].tile.Position.x) + " " + str(
                    self.destination[self.index].tile.Position.y))
                print(str(len(self.destination)))
                return create_move_action(Point(curMove.tile.Position.x - self.PlayerInfo.Position.x,
                                                curMove.tile.Position.y - self.PlayerInfo.Position.y))

        if (self.state == 10):
            if (gameMap.getTileAt(self.mineralTile.tile.Position).TileContent == TileContent.Resource):
                return create_collect_action(Point(self.mineralTile.tile.Position.x - self.PlayerInfo.Position.x,
                                                   self.mineralTile.tile.Position.y - self.PlayerInfo.Position.y))
            else:
                self.state = 2
                return create_empty_action()

    def after_turn(self):
        for i in range(self.miniGameMap.xMin, self.miniGameMap.xMin + 20):
            if not i in self.gameMap:
                self.gameMap[i] = {}
            for j in range(self.miniGameMap.yMin, self.miniGameMap.yMin + 20):
                self.gameMap[i][j] = self.miniGameMap.getTileAt(Point(i, j))
        # StorageHelper.write(self.MAP_KEY, self.gameMap)
        """
        Gets called after executeTurn
        """
        pass

    def findFirstMineral(self, playerInfo):
        mineral = None
        for x in range(self.miniGameMap.xMin, self.miniGameMap.xMax):
            for y in range(self.miniGameMap.yMin, self.miniGameMap.yMax):
                tile = self.miniGameMap.getTileAt(Point(x, y))
                if (tile.TileContent == TileContent.Resource):
                    if (mineral == None):
                        mineral = tile.Position
                    elif (Point.Distance(playerInfo.Position, tile.Position) < Point.Distance(playerInfo.Position,
                                                                                              mineral)):
                        mineral = tile.Position

        return mineral

    def calc_heuristic(self, case, endPoint):
        case.cost = abs(endPoint.x - case.tile.Position.x) + abs(endPoint.y - case.tile.Position.y)

    def a_star_to(self, endPoint, gameMap):
        open_list = {}
        closed_list = {}

        currentCase = None
        currentTile = self.PlayerInfo

        while (currentTile.Position.x != endPoint.x or currentTile.Position.y != endPoint.y):

            open_list = {}
            print(str(self.PlayerInfo.Position.x) + " " + str(self.PlayerInfo.Position.y))
            print("" + str(currentTile.Position.x) + " " + str(currentTile.Position.y) + str(len(closed_list)) + " " + (
                "None" if len(closed_list) < 2 else str(closed_list[len(closed_list) - 3].tile.Position.x)))

            nextCases = []

            curCase = Case(currentTile.Position, None if len(closed_list) < 1 else closed_list[len(closed_list) - 2])

            # Les cases adjacentes
            nextCases.append(Case(gameMap.getTileAt(Point(currentTile.Position.x, currentTile.Position.y - 1)),
                                  curCase))
            nextCases.append(Case(gameMap.getTileAt(Point(currentTile.Position.x, currentTile.Position.y + 1)),
                                  curCase))
            nextCases.append(Case(gameMap.getTileAt(Point(currentTile.Position.x - 1, currentTile.Position.y)),
                                  curCase))
            nextCases.append(Case(gameMap.getTileAt(Point(currentTile.Position.x + 1, currentTile.Position.y)),
                                  curCase))

            for case in nextCases:
                # Calcul heuristique
                self.calc_heuristic(case, endPoint)

                # Ajout ou modification
                if (case.tile in open_list):
                    if (open_list[case.tile].cost < case.cost):
                        open_list[case.tile] = case
                else:
                    if (
                            case.tile.TileContent == TileContent.Empty or case.tile.TileContent == TileContent.House or case.tile.TileContent == TileContent.Resource):
                        open_list[case.tile] = case

            lowest_cost = 100000000000000
            next_case = 0
            for case in open_list:
                if (open_list[case].cost < lowest_cost):
                    lowest_cost = open_list[case].cost
                    next_case = open_list[case]

            del open_list[next_case.tile]
            next_case.origin = currentCase
            closed_list[len(closed_list) - 1] = next_case

            currentTile = next_case.tile
            currentCase = next_case

        return closed_list

    def find_house(self):
        minPosX = self.PlayerInfo.Position.x - 10
        minPosY = self.PlayerInfo.Position.y - 10

        for i in range(minPosX, minPosX + 20):
            for j in range(minPosY, minPosY + 20):
                if (self.miniGameMap.getTileAt(Point(i, j)).TileContent == TileContent.House):
                    return self.miniGameMap.getTileAt(Point(i, j))


class Case:
    def __init__(self, tile, origin):
        self.tile = tile
        self.origin = None
        self.cost = 0
