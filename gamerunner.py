
import os
import StringIO
import pygame


compeditors = {}

compeditors["Dead on arrival"] = {"file" : "teams/Dead_on_arrival_inf2101_oblig2/src/labyrinth.py", "score" : 0}

#compeditors["CLP"] = {"file" : "teams/CLP_inf2101_oblig2/src/labyrinth.py", "score" : 0}

#compeditors["GRUPPE 3"] = {"file" : "teams/gruppe3_inf2101_oblig2/src/find_toby.py", "score" : 0}

#compeditors["HMA_030"] = {"file" : "teams/hma030_inf2101_oblig2/src/labyrinth.py", "score" : 0}

#compeditors["I_can_haz_cheezburger"] = {"file" : "teams/I_can_haz_cheezburger-INF2101-Oppg2/src/labyrinth.py", "score" : 0}

#compeditors["iro018 - jfa012"] = {"file" : "teams/iro018-jfa012_inf-2101_oblig2/src/labyrinth.py", "score" : 0}

#compeditors["jli018"] = {"file" : "teams/jli018_inf2101_oblig2/src/labyrinth.py", "score" : 0}

#compeditors["NomenNescio"] = {"file" : "teams/NomenNescio_inf2101_oppg2/src/labyrinth.py", "score" : 0}

pygame.display.init()
pygame.font.init()


myFont = pygame.font.SysFont("None", 40)


def update_score_board(screen):
  print "UPDATE BOARD"
  
  screen.fill((0,0,0))
  
  y = 10
  for key in compeditors.keys():
    screen.blit(myFont.render(key, 0, (255, 255, 255)), (10, y))
    screen.blit(myFont.render(str(compeditors[key]["score"]), 0, (255, 255, 255)), (400, y))
    y += 50

if __name__ == "__main__":
    
  screen = pygame.display.set_mode((640, 480), pygame.HWSURFACE, 32)
  
  update_score_board(screen)
  
  pygame.display.flip()
  
  print "Starting game rounds!"
  
  try:
    f = open("scoreBackup.txt", "w+")
  except:
    print "error opening file"
  
  
  running = True
  while(running):
    ans = raw_input("START NEW ROUNDS Y/N: ")
    print ans
    if ("y" in str(ans)):
      f.write("NEW ROUND\n") 
      for key in compeditors.keys():
    
	raw_input('Press enter to start ' + key)
	
	print "Running: " + key
	cmd = str("python %s" % (compeditors[key]["file"]))
      
	output = os.popen(cmd).read()
	output = StringIO.StringIO(output)
	
	# PARSE RESULT
	score = 0
	for line in output.readlines():
	  if "You found Toby" in line:
	    print "COMPLETED LEVEL"
	    score = raw_input('ENTER SCORE: ')
	    compeditors[key]["score"] += int(score)
	    
	    f.write(key + " score: " + str(compeditors[key]["score"]) + "\n")
	    
	    update_score_board(screen)
	  elif "You failed to find Toby" in line:
	    print "FAILED TO FIND TOBY"
	    f.write(key + "FAILED\n") 
	
	
	pygame.display.flip()
      
    else:
      running = False
    
  f.close()
    
  print output.readline()