
import os
import StringIO


compeditors = {}

compeditors["Dead on arrival"] = "teams/Dead_on_arrival_inf2101_oblig2/src/labyrinth.py"

compeditors["CLP"] = "teams/CLP_inf2101_oblig2/src/labyrinth.py"

compeditors["GRUPPE 3"] = "teams/gruppe3_inf2101_oblig2/src/find_toby.py"

compeditors["HMA_030"] = "teams/hma030_inf2101_oblig2/src/labyrinth.py"

compeditors["I_can_haz_cheezburger"] = "teams/I_can_haz_cheezburger-INF2101-Oppg2/src/labyrinth.py"

compeditors["iro018 - jfa012"] = "teams/iro018-jfa012_inf-2101_oblig2/src/labyrinth.py"

compeditors["jli018"] = "teams/jli018_inf2101_oblig2/src/labyrinth.py"

compeditors["NomenNescio"] = "teams/NomenNescio_inf2101_oppg2/src/labyrinth.py"


if __name__ == "__main__":
  print "Starting game rounds!"
  
  for key in compeditors.keys():
    raw_input('Press enter to start ' + key)
    
    print "Running: " + key
    cmd = str("python %s" % (compeditors[key]))
  
    output = os.popen(cmd).read()
    output = StringIO.StringIO(output)
    
    print output.readlines()
    
    
  
  
  
  print output.readline()