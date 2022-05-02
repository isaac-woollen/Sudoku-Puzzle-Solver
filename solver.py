#-------------------------------
# TODO : Return the solved board DONE
#-------------------------------

def solve(board):
  find = find_empty(board)      # Call the find_empty function
  if not find:                  # If the call returned false
    return board                 # The puzzle has been solved (May have to change back to 'return True')
  else: 
    row, col = find                  # Otherwise assign the variables to the values at that array element of empty space                       
  for i in range(1,10):              # For each possible answer in a slot
    if valid(board, i, (row, col)):  # Call the 'valid' function 
      board[row][col] = i            # If true, assign the array slot to calculated value
      if solve(board):               # Recurr the solve function          
        return board
          
      board[row][col] = 0            # If solve(board) can't return true, reset the value to 0 and return false
        
  return False
    
  
def valid (board, num, pos):
  #Check the row
  for i in range(len(board[0])):                # For each element in the row (x-dir)
    if board[pos[0]][i] == num and pos[1] != i: # if the position at the given array element is equal to the number in question 
      return False                              # AND a value in the column is not equal to the number in question, return false 

  #Check the column
  for i in range(len(board)):                   # For each element in the column (y-dir)
    if board[i][pos[1]] == num and pos[0] != i:
      return False

  #Check the box
  box_x = pos[1] // 3
  box_y = pos[0] // 3

  for i in range(box_y*3, box_y*3 + 3):        # From the start of the box to the end of it
    for j in range(box_x*3, box_x*3 + 3):      # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      if board[i][j] == num and (i,j) != pos:  # if any value in the rest of the box is equal to the number in question, return false
        return False

  return True
        
def print_board(board):
  for i in range (len(board)):        # For each element in the column, Check if it is at a new block. If so, print --- across the board
    if i % 3 == 0 and i != 0:         # For each element in the row, check if it is at a new block. If so, print | down the board
      print ("- - - + - - - + - - -")
    for j in range (len(board[0])):
      if j % 3 == 0 and j != 0:
        print("| ", end  = "")

      if j == 8:                  #At the next to end of the loop
        print(board[i][j])
      else:
        print(str(board[i][j]) + " ", end="")
  
def find_empty(board): 
  for i in range(len(board)):
    for j in range(len(board[0])):
     if board[i][j] == 0:
       return (i, j) # The index at which there is emptiness
  return None
