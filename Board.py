def generateValidBoard(mode):
  board = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
  ]
  base  = 3
  side  = base*base
    
  # pattern for a baseline valid solution
  def pattern(r,c): return (base*(r%base)+r//base+c)%side
    
  # randomize rows, columns and numbers (of valid base pattern)
  from random import sample
  def shuffle(s): return sample(s,len(s)) 
  rBase = range(base) 
  rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
  cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
  nums  = shuffle(range(1,base*base+1))
    
    # produce board using randomized baseline pattern
  board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
  if mode == 0:
    empties = 25
  elif mode == 1:
    empties = 45
  else:
    empties = 55
  squares = side*side
  #empties = squares * 2//d 
  for p in sample(range(squares),empties):
        board[p//side][p%side] = 0
  return board