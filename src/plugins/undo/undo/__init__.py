"""
This is where the implementation of the plugin code goes.
The undo-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('undo')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class undo(PluginBase):
  def main(self):


    #from tile and need to use get children to update it 
    
    #Counting pieces (3pts): at any state of the game, the studio should be able to count how many pieces per color are on the board.
      #Flippi`ts): Given the last piece put onto the board, a plugin should be able to come up with essentially the next state of the game, doing all the necessary flipping.
    #Undo (3pts): while it is not usually done in a game like this, we want to offer a function that can take the game back to the previous state, allowing the last user to make a different move. 
    
    #from game folder - that contain - have a current state pointer and change it to the last state 
    #game state have a previous state 
    #Auto: as a BONUS (5pts), you can implement some computer mechanism that can play the game, if this functionality is used, than it makes a valid move. Even better if the move it makes is an 'optimal' one, but that is not a requirement
    #find a valid state and make a move 
    
    #go through tile find valid and make move 
    #undo should be a separate plug in 
    active_node = self.active_node
    core = self.core
    logger = self.logger
    self.namespace = None
    META = self.META
    logger.debug('path: {0}'.format(core.get_path(active_node)))
    logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
    logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
    logger.error('guid: {0}'.format(core.get_guid(active_node)))
    #nodesList = core.load_sub_tree(core.get_parent(core.get_parent(core.get_parent(active_node))))
    nodesList = core.load_sub_tree(active_node)
    nodes = {}
    gameStates=[]
    #tile_node 
    for node in nodesList:
      nodes[core.get_path(node)] = node
    self.nodes = nodes
    currentStatePath= core.get_pointer_path(active_node,'currentState')
    currentState= nodes[currentStatePath]
    self.currentState = currentState
    

    states = []
    for path in nodes:
      node = nodes[path]
      name = core.get_attribute(node, 'name')
      if (core.is_instance_of(node, META['GameState'])):
        currentMove= nodes[core.get_pointer_path(node, "currentMove")]
        currentMoveColor = core.get_attribute(currentMove,'color')
        currentMoveTile = core.get_parent(currentMove)
        currentMoveTileRow = core.get_attribute(currentMoveTile, 'row')
        currentMoveTileColumn = core.get_attribute(currentMoveTile, 'column')
        currentPlayer = core.get_attribute(nodes[core.get_pointer_path(node, "currentPlayer")], 'name')
        states.append({"path": path, "name": name, "board": [[None for x in range(8)] for x  in range(8)], "currentPlayer" : currentPlayer,
        "currentMoveColor": currentMoveColor, "currentMoveTileRow": currentMoveTileRow, "currentMoveTileColumn": currentMoveTileColumn}) 
      if (core.is_instance_of(node, META['Tile'])):
        #logger.warn(node)
        for state in states:
          if state["path"][:4] == path[:4]:
            row = core.get_attribute(node, 'row')
            column = core.get_attribute(node, 'column')
            children = core.get_children_paths(node)
            flips = []
            childColor = None
            childPath = None
            if len(children) > 0:
              childPath = children[0]
              childColor = core.get_attribute(nodes[childPath], 'color')
              for path2 in nodes:
                node2 = nodes[path2]
                if (core.is_instance_of(node2, META['mightFlip'])):
                  srcTile = core.get_parent(nodes[core.get_pointer_path(node2, 'src')])
                  dstTile = core.get_parent(nodes[core.get_pointer_path(node2, 'dst')])
                  srcInfo = {'column': core.get_attribute(srcTile, 'column'), 'row':core.get_attribute(srcTile,'row')}
                  dstInfo = {'column': core.get_attribute(dstTile, 'column'), 'row':core.get_attribute(dstTile,'row')}

                  if node == srcTile:
                    flips.append(dstInfo)
                    
                    
                  
            state["board"][row][column] = {"color": childColor, "flips": flips}
            
    self.states = states
   
    #self.show_states()
    #self.next_move_viable()
    #self.makeNewState()
    #self.auto()
    #self.isHighlight()
    
    #logger.info(states)
    self.undo()
    
    #self.countingPieces()
   
    

  def show_states(self):
    for state in self.states:
      stateString = """[
      name: {}
      currentPlayer: {}
      currentMove: color:{}, row{}, column{}
      """.format(state["name"], state["currentPlayer"], state["currentMoveColor"], state["currentMoveTileRow"], state["currentMoveTileColumn"])
      boardString = "board:\n["
      for row in state["board"]:
        rowstring = "["
        for tile in row:
          rowstring += "[color: {}, flips{}]".format(tile["color"], tile["flips"])
          #rowstring += str(tile)
        rowstring += "]"
        boardString += rowstring
        boardString += "\n"
      boardString +="]\n]"
      stateString += boardString
      
      
  def next_move_viable(self,tile):
    self.valid = False
    self.to_flip = []
    META = self.META
    self.next_moves = {"black":"white", "white": "black"}
    flip_directions = [(0,1), (1,0), (1,1), (-1,-1), (1,-1), (-1,1), (-1,0), (0,-1)]
    logger = self.logger
    core = self.core
    currentTile = tile
    currentTileNodes = []
    self.currentTileNodes=currentTileNodes
    #board = core.current_node
    #board = core.get_parent(current_node)
    
    #gamestate = core.get_parent(board)
    current_move = self.nodes[core.get_pointer_path(self.currentState, "currentMove")]
    current_move_color = core.get_attribute(current_move, 'color')
    next_move_color = self.next_moves[current_move_color]
    self.next_move_color = next_move_color
    state_path = self.currentState["nodePath"]
    
    for state in self.states:
      if state_path == state['path']:
        board_ref = state['board']
        column = core.get_attribute(currentTile, 'column')
        row = core.get_attribute(currentTile, 'row')
        if board_ref[row][column]['color'] == None:
          for direction in flip_directions:
            to_flip = []
            rows = len(board_ref)
            columns = len(board_ref[0])
            
            
            #算新 indices
            newRow = row+ direction[0]
            
            newColumn = column + direction[1]
            
            if 0<= newRow < rows and 0<= newColumn < columns and board_ref[newRow][newColumn] is not None:
              
            
              if board_ref[row + direction[0]][column + direction[1]]['color'] == current_move_color:
                to_flip = [(row + direction[0], column + direction[1])]
                multiplier = 2
                while (row + (direction[0]*multiplier) > 0 and row + (direction[0]*multiplier) < 8) and (column + (direction[1]*multiplier) > 0 and column + (direction[1]*multiplier) < 8) and board_ref[row + direction[0]*multiplier][column + (direction[1]*multiplier)]!=None:
               
                  if board_ref[row + direction[0]*multiplier][column + (direction[1]*multiplier)]['color'] == next_move_color:
                    end_position = (row + direction[0]*multiplier, column + (direction[1]*multiplier))
                    for position in to_flip:
                      self.to_flip.append(position)
                    self.valid = True
                    #change count based on color 
                    #currentMove= nodes[core.get_pointer_path(node, "currentMove")]
                    #currentMoveColor = core.get_attribute(currentMove,'color')
                    self.currentTileNodes.append(currentTile)




                  to_flip.append((row + direction[0]*multiplier, column + (direction[1]*multiplier)))
                  multiplier +=1
    return self.valid, self.currentTileNodes,self.to_flip
  
  

  def makeNewState(self,autoTile,autoFlip):
    #import re
    #if not self.valid:
      #self.logger.error("THIS IS AN INVALID MOVE")
      #self.create_message(self.active_node, "THIS IS AN INVALID MOVE")
      #return
    #active_node = self.active_node
    core = self.core
    logger = self.logger
    META = self.META
    nodes = self.nodes
    #logger.info(self.to_flip)
    #parent_state = core.get_parent(core.get_parent(active_node))
    parentState = self.currentState
    game_folder = core.get_parent(parentState)
    #game_folder = core.get_parent(parent_state)
    self.autoRow = core.get_attribute(autoTile, 'row')
    self.autoColumn = core.get_attribute(autoTile, 'column')
    #core.create_node({'parent':game_folder, 'base': META["OthelloGameState"]})
    parentName = core.get_attribute(parentState, 'name')
    newName = parentName + "_1"
    try:
      for i, c in enumerate(parentName):
        if c.isdigit():
          number_index = i
          break
      stateNumber = int(parentName[number_index:]) + 1
      newName = parentName[:number_index] + f"{stateNumber}"
    except:
      pass
    copied_node = core.copy_node(parentState,game_folder)
    self.copied_node=copied_node
    core.set_pointer(copied_node,'previousState',parentState) #pointing the previous pointer to old gamestate
    core.set_pointer(game_folder,'currentState',copied_node)# pointing the current pointer to the new gamestate
    core.set_attribute(copied_node, 'name', newName)
    childPaths=core.get_children_paths(copied_node)
    oldPlayer = core.get_pointer_path(copied_node, "currentPlayer")
   
    for childPath in childPaths:
      child = core.load_by_path(self.root_node, childPath)
      if core.is_instance_of(child, META["Player"]):
        if not childPath == oldPlayer:
          core.set_pointer(copied_node, "currentPlayer", child)
      if core.is_instance_of(child, META["Board"]):
        board = child
        tilePaths = core.get_children_paths(board)
        for tilePath in tilePaths:
          tile = core.load_by_path(self.root_node, tilePath)
          if core.get_attribute(tile, 'row') ==self.autoRow and core.get_attribute(tile, 'column') ==self.autoColumn:
            created_piece = core.create_node({'parent':tile, 'base': META["Piece"]})
            core.set_pointer(copied_node, "currentMove", created_piece)
            core.set_attribute(created_piece, 'color', self.next_move_color)
          elif (core.get_attribute(tile, 'row'), core.get_attribute(tile, 'column')) in autoFlip:
            piece_path = core.get_children_paths(tile)[0]
            core.set_attribute(core.load_by_path(self.root_node, piece_path), 'color', self.next_move_color)
    
    
    #core.set_pointer(game_state, 'currentPlayer', player_node)
    self.util.save(self.root_node, self.commit_hash, self.branch_name)
    
  def isHighlight(self):
      #Highlight valid tiles for the next move (3pts): at each state of the game, 
      #the active player can only place their piece to specified tiles (where they would essentially initiate some color changes)
      #is valid for the next move add attribute to tile TzF - says valid next move or not
      validTileNodes = []
      validTiles = []
      validFlip = []
      active_node=self.currentState
      
      core = self.core
      logger = self.logger
      self.namespace = None
      META =self.META
      
      
      
      childPaths=core.get_children_paths(active_node)
      #oldPlayer = core.get_pointer_path(copied_node, "currentPlayer")
      for childPath in childPaths:
        child=core.load_by_path(self.root_node,childPath)
        if core.is_instance_of(child, META["Board"]):
          board = child
          tilePaths = core.get_children_paths(board)
          for tilePath in tilePaths:

            tile = core.load_by_path(self.root_node, tilePath)
            if core.is_instance_of(tile,META["Tile"]):

              valid,currentTiles,flip=self.next_move_viable(tile)

              if(valid==True):
                logger.debug('valid: {}'.format(valid))
                logger.debug('row:{0}'.format(core.get_attribute(tile,'row')))
                logger.debug('column:{0}'.format(core.get_attribute(tile,'column')))
                logger.info(flip)
                validTileNodes.append(tile)
                validFlip.append(flip)
      for i in validTileNodes:
        validTiles.append([core.get_attribute(i,'row'),core.get_attribute(i,'column')])
      logger.info(validTiles)
      return validTileNodes,validFlip
         
  def countingPieces(self):
      
      #Counting pieces (3pts): at any state of the game, the studio should be able to count how many pieces per color are on the board.
      
      active_node=self.currentState
      core = self.core
      logger = self.logger
      self.namespace = None
      META = self.META
      blackCount=0
      whiteCount=0
      countingList=self.core.get_children_paths(active_node)
    
    
      for count in countingList:
        child=self.nodes[count]

        if (self.core.is_instance_of(child, self.META['Board'])):
          for tile in self.core.get_children_paths(child):
            #self.logger.info(tile)
            tile=self.nodes[tile]
            for piecePath in self.core.get_children_paths(tile):
              piece=self.nodes[piecePath]           
              #check if color match then 
              if "black"==self.core.get_attribute(piece,'color'):
                blackCount=blackCount+1
              elif "white"==self.core.get_attribute(piece,'color'):
                whiteCount=whiteCount+1

      logger.info(blackCount)
      logger.info(whiteCount)

      return blackCount,whiteCount
      
    
    
  def undo(self):
      #undo should be a sepaate plug in
      #Undo (3pts): while it is not usually done in a game like this, we t to offer a function that can take the game back to the previous state, allowing the last user to make a different move. 
      
      
      
      active_node=self.active_node 
      core = self.core
      logger = self.logger
      self.namespace = None
      META = self.META
      nodesList = core.load_sub_tree(active_node)
    
      nodes = {}
      gameStates=[]
      for node in nodesList:
        nodes[core.get_path(node)] = node
         
      currentStatePath=core.get_pointer_path(active_node,'currentState')
      currentState=nodes[currentStatePath]
      logger.info(core.get_attribute(currentState,'name'))
      previousStatePath=core.get_pointer_path(currentState,'previousState')
      previousState=nodes[previousStatePath]
      core.set_pointer(active_node,'currentState',previousState)
      core.delete_node(currentState)
      self.util.save(self.root_node,self.commit_hash,self.branch_name)
      

    
    
    
    
    #from game folder - that contain - have a current state pointer and change it to the last state 
    #game state have a previous state 
    
  def auto(self): 
      
      #Auto: as a BONUS (5pts), you can implement some computer mechanism that can play the game, if this functionality is used, than it makes a valid move. Even better if the move it makes is an 'optimal' one, but that is not a requirement
      #find a valid state and make a move choose the first valid state you see and place it there
    
      #go through tile find valid and make move 
      from random import randrange
      active_node=self.currentState
      core = self.core
      logger = self.logger
      validTiles=[]
      self.namespace = None
      META = self.META
      tiles,flips=self.isHighlight()
      random_index = randrange(len(tiles))
      self.makeNewState(tiles[random_index],flips[random_index])
      
    
