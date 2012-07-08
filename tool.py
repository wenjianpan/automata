class ArrowTool:
    def __init__(self, canvas, automata):
        self.Viewer = canvas
        self.Automata = automata
        self.lastClickedState = None
        self.lastClickedTransition = None
        self.initialPointClicked = None
        
    def mouseClicked(self, event):
        print "mouse clicked"
        trans = self.Automata.transitionAtPoint(event.x, event.y)
        if trans == None:
           return
        self.Automata.editTranstion(trans, event.x, event.y)

    def mousePressed(self, event):
        self.lastClickedState = self.Automata.stateAtPoint(event.x, event.y)
        if self.lastClickedState == None:
            self.lastClickedTransition = self.Automata.transitionAtPoint(event.x, event.y)
        elif self.lastClickedState != None:
            self.initialPointClicked = (event.x, event.y)
            return
        if self.lastClickedTransition != None:
            self.initialPointClicked = (event.x, event.y)
            self.fs=self.lastClickedTransition.getFromState()
            self.ts=self.lastClickedTransition.getToState()
            self.f_orig_p = (self.fs.point[0], self.fs.point[1])
            self.t_orig_p = (self.ts.point[0], self.ts.point[1])
            
    def mouseDragged(self, event):
        if self.lastClickedState != None:   # drag state
            self.lastClickedState.setPoint(event.x, event.y)
            self.Automata.repaintState(self.lastClickedState)
            for t in self.lastClickedState.trans_list:
                self.Automata.repaintTransition(t)
        elif self.lastClickedTransition != None:    # drag transition
            x=event.x-self.initialPointClicked[0]
            y=event.y-self.initialPointClicked[1]

            self.fs.setPoint(self.f_orig_p[0]+x, self.f_orig_p[1]+y)
            if self.fs!= self.ts:
                self.ts.setPoint(self.t_orig_p[0]+x, self.t_orig_p[1]+y)
                self.Automata.repaintState(self.ts)         # repaint the two states connected to the trans
                for t in self.ts.trans_list:
                    self.Automata.repaintTransition(t)                
            self.Automata.repaintState(self.fs)             # the transition will be also repainted
            for t in self.fs.trans_list:
                self.Automata.repaintTransition(t)
            
    def mouseReleased(self, event):
        self.lastClickedState = None
        self.lastClickedTransition = None

    
class StateTool:
    def __init__(self, canvas, automata):
        self.s = None
        self.Viewer = canvas
        self.Automata = automata
    
    def mousePressed(self, event):
        self.s = self.Automata.createState(event.x, event.y)

    def mouseDragged(self, event):
        if self.s:
            self.s.setPoint(event.x, event.y)
            self.Automata.repaintState(self.s)

    def mouseReleased(self, event):
        self.s = None
        return

class TransitionTool:
    def __init__(self, canvas, automata):
        self.first = None
        self.line = None
        self.Viewer = canvas
        self.Automata = automata
        
    def drawLine(self, x0, y0, x1, y1):
        self.line = self.Viewer.create_line(x0, y0, x1, y1, fill='grey', width=1)
        return

    def deleteLine(self, line):
        self.Viewer.delete(line)
        return
    
    def mousePressed(self, event):
        self.first = self.Automata.stateAtPoint(event.x, event.y)
        if self.first == None:
            return

    def mouseDragged(self, event):
        if self.first == None:
            return
        if self.line:
            self.deleteLine(self.line)
        self.drawLine(self.first.point[0], self.first.point[1], event.x, event.y)

    def mouseReleased(self, event):
        if self.first == None:
            return
        if self.line:
            self.deleteLine(self.line)
            self.line = None
        s=self.Automata.stateAtPoint(event.x, event.y)
        if s==None:
            return     # not end at another state
        trans = self.Automata.createTransition(self.first, s)  # end at another state, create a transition
        
        self.Automata.editTransition(trans)
        #repaintTransition()
        self.first = None
    

class KillTool:
    def __init__(self, canvas, automata):
        self.Viewer = canvas
        self.Automata = automata
    
    def mousePressed(self, event):
        to_remove = []
        state = self.Automata.stateAtPoint(event.x, event.y)
        if state != None:
            for trans in state.trans_list:
                #print "to remove", trans
                to_remove.append(trans)
            for trans in to_remove:
                self.Automata.removeTransition(trans)
                #print "after remove one"
            #print "remove state"
            self.Automata.removeState(state)
            return

        trans = self.Automata.transitionAtPoint(event.x, event.y)
        if trans != None:
            self.Automata.removeTransition(trans)
        return
    
    def mouseDragged(self, event):
        return
    
    def mouseReleased(self, event):
        return




        
