from random import choice
qabc='акотирснпелвмдчьзубцгшяыщфхэюжйъё'
fieldsize=5#field size
voc_name = 'files/101_voc.txt'

voc = []
for s in list(open(voc_name, encoding="utf-8")):
  voc.append(s.strip())

def wordexist(word,field,setchar):
  for c in word:
    if not c in setchar:
      return([[]])
  chain=[]
  for i in range(fieldsize):
    for j in range(fieldsize):
      if word[0]==field[i][j]:
        chain.append([[i,j]])
  lw=1#index of liter
  while lw<len(word) and len(chain):
    newchain=[]
    for s in chain:
      last=s[-1]
      for i in range(max(0,last[0]-1),min(last[0]+1,fieldsize-1)+1):
        for j in range(max(0,last[1]-1),min(last[1]+1,fieldsize-1)+1):
          if (word[lw]==field[i][j]) and (not [i,j] in s):
            newchain.append(s+[[i,j]])
    chain=newchain.copy()
    lw+=1
  return([chain])

def decode(s):
  field=[]
  ms=int(s)
  mod=len(qabc)
  for i in range(fieldsize):
    row=[]
    for j in range(fieldsize):
      row.append(qabc[ms%mod])
      ms//=mod
    field.append(row[::-1])
  return(field[::-1])

def get_game(game_num = -1):
  vcg = list(open('files/games.txt'))
  if 0 <= game_num < len(vcg):
    return(decode(vcg[game_num]))
  else:
    return(decode(choice(vcg)))
