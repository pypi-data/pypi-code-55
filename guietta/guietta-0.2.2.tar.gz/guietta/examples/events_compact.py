# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui, Quit

def do_eval(gui, *args):
    print(gui)
    gui.result = eval(gui.expr)


gui = Gui(
    
  [  'Enter expression:', E('expr')  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )

print(gui.Eval.slot)

gui.Eval.slot = do_eval
gui.expr.slot['textEdited'] = do_eval

gui.run()

# GUI widgets are available after window closing,
print(gui.result)

    