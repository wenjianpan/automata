from Tkinter import *
from tool import *
from math import *

class state:
    def __init__(self, x=None, y=None, obj_id=None, label=None, attr = None):
        self.point=(x,y)
        self.obj_id=obj_id              # view object id
        self.label=label
        self.index = 0
        self.label_obj_id = None
        self.trans_list = []
        self.attr = attr                # start, final, or none

    def setPoint(self, x, y):
        self.point=(x, y)

class transition:
    def __init__(self, obj_id=None, input_c=None):
        self.obj_id=obj_id
        self.peer_flag = None           # indicate for those two directions
        self.labels=[]                  # transition may have multiple labels 
        self.states_pair = []           #          transition
                                        # from--------------------->to
    def getFromState(self):
        return self.states_pair[0]
    
    def getToState(self):
        return self.states_pair[1]
        
class automata:
    def __init__(self, parent=None):
        canvas = Canvas(parent, width=500, height=500, bg= 'white')
        canvas.pack(expand=YES, fill=BOTH)
        parent.bind('<KeyPress>',        self.onOptions)
        self.canvas = canvas
        parent.title('Automata-1.0')
        parent.protocol('WM_DELETE_WINDOW', self.onQuit)
        self.realquit = parent.quit
        self.arrow_tool = ArrowTool(self.canvas, self)
        self.state_tool = StateTool(self.canvas, self)
        self.transition_tool = TransitionTool(self.canvas, self)
        self.kill_tool = KillTool(self.canvas, self)
        self.states = []        # states
        self.transitions = []   # transitions
        self.states_labels = []
        for i in range(100):
            self.states_labels.append(-1)

        #self.canvas.bind('<Button-1>', self.arrow_tool.mouseClicked)
        self.canvas.bind('<ButtonPress-1>',   self.arrow_tool.mousePressed)
        self.canvas.bind('<B1-Motion>',       self.arrow_tool.mouseDragged)
        self.canvas.bind('<ButtonRelease-1>', self.arrow_tool.mouseReleased)
        
    def onOptions(self, event):
        keymap = {
            's': lambda self: self.changeTool(self.state_tool), 
            'a': lambda self: self.changeTool(self.arrow_tool),  
            't': lambda self: self.changeTool(self.transition_tool),
            'k': lambda self: self.changeTool(self.kill_tool),
            'p': lambda self: self.dump(),
            }
        try:
            keymap[event.char](self)
        except KeyError:
            print 'no bind'
            
    def createState(self, x, y):
        found = 0
        for i in range(100):
            if self.states_labels[i] == -1:
                self.states_labels[i] = i
                found = 1
                break
        if found == 0:
            print "can't create more states"
            return None
            
        s = state(x, y)
        self.states.append(s)
        s.point = (x, y)   
        s.label = 'p' + str(self.states_labels[i])
        s.index = self.states_labels[i]
        self.repaintState(s)

        return s

    def createTransition(self, from_s, to_s):
        for t in self.transitions:
            if t.states_pair[0] == from_s and t.states_pair[1] == to_s:
                print "alread there"
                return t
            
        for t in self.transitions:
            if t.states_pair[0] == to_s and t.states_pair[1] == from_s:
                print "another direction"
                t.peer_flag = 1;
                trans = transition()
                trans.peer_flag = 2;
                trans.states_pair.append(from_s)
                trans.states_pair.append(to_s)
                from_s.trans_list.append(trans)
                to_s.trans_list.append(trans)
                self.transitions.append(trans)
                self.repaintTransition(trans)
                self.repaintTransition(t)
                return trans

        trans = transition()
        trans.states_pair.append(from_s)
        trans.states_pair.append(to_s)
        if from_s != to_s:
            from_s.trans_list.append(trans)
        to_s.trans_list.append(trans)
        self.transitions.append(trans)        
        # draw a line point from from_s to to_s
        self.repaintTransition(trans)
        return trans
        
    def addState(self, state):
        self.states.append(state)

    def addTransition(self, trans):
        self.transitions.append(trans)

    def removeState(self, state):
        self.states.remove(state)
        self.canvas.delete(state.obj_id)
        self.canvas.delete(state.label_obj_id)
        self.states_labels[state.index] = -1
        del state
        
    def removeTransition(self, trans):
        print "remove trans", trans
        if trans.states_pair[0]== trans.states_pair[1]:   # trans from self to self
            trans.states_pair[0].trans_list.remove(trans)
        else:
            for s in trans.states_pair: 
                s.trans_list.remove(trans)
        
        if trans.peer_flag != None:
            for t in self.transitions:
                if trans.states_pair[0]==t.states_pair[1] and trans.states_pair[1]==t.states_pair[0]:
                    # there are pair trans between two states
                    t.peer_flag = None
                    self.repaintTransition(t)
                    break
        self.transitions.remove(trans)
        self.canvas.delete(trans.obj_id)
        del trans

    def repaintState(self, s):
        if s.obj_id != None: self.canvas.delete(s.obj_id)
        if s.label_obj_id != None: self.canvas.delete(s.label_obj_id)
        s.obj_id = self.canvas.create_oval(s.point[0]-15, s.point[1]-15,
                    s.point[0]+15, s.point[1]+15,    
                    fill='yellow', width=1)
        s.label_obj_id = self.canvas.create_text(s.point[0],
                                                 s.point[1],
                                                 text=s.label)
        
    def repaintTransition(self, t):
        if t.obj_id:
            self.canvas.delete(t.obj_id)
        if t.states_pair[0] == t.states_pair[1]:    # point to myself
            t.obj_id = self.canvas.create_line(t.states_pair[0].point[0]-10, t.states_pair[0].point[1]-15*cos(asin(10.0/15.0)),    # start
                                    t.states_pair[1].point[0], t.states_pair[1].point[1]-45, 
                                    t.states_pair[1].point[0]+10, t.states_pair[1].point[1]-15*cos(asin(10.0/15.0)), # stop
                                    fill='black', width=1,
                                    arrow=LAST, smooth=True)
            return

        if t.states_pair[0].point[0] == t.states_pair[1].point[0]:  # x0 == x1
            #print "x0==x1"
            fpx = t.states_pair[0].point[0]
            tpx = t.states_pair[1].point[0]
            if t.states_pair[0].point[1] > t.states_pair[1].point[1]:
                fpy = t.states_pair[0].point[1] - 15
                tpy = t.states_pair[1].point[1] + 15
            elif t.states_pair[0].point[1] < t.states_pair[1].point[1]:
                fpy = t.states_pair[0].point[1] + 15
                tpy = t.states_pair[1].point[1] - 15
            else:
                fpy = t.states_pair[0].point[1] + 15
                tpy = t.states_pair[1].point[1] + 15

        elif t.states_pair[0].point[1] == t.states_pair[1].point[1]: # y0 == y1
            #print "y0==y1"
            fpy = t.states_pair[0].point[1]
            tpy = t.states_pair[1].point[1]
            if t.states_pair[0].point[0] > t.states_pair[1].point[0]:
                fpx = t.states_pair[0].point[0] - 15
                tpx = t.states_pair[1].point[0] + 15
            elif t.states_pair[0].point[0] < t.states_pair[1].point[0]:
                fpx = t.states_pair[0].point[0] + 15
                tpx = t.states_pair[1].point[0] - 15
            else:
                fpx = t.states_pair[0].point[0] + 15
                tpx = t.states_pair[1].point[0] + 15

        else:   # x0 != x1 and y0 != y1
            tan = float(t.states_pair[1].point[0]-t.states_pair[0].point[0])/float(t.states_pair[1].point[1]-t.states_pair[0].point[1])
            o =atan(tan) 
            if t.states_pair[0].point[1] > t.states_pair[1].point[1]:  #y
                fpy = t.states_pair[0].point[1] - abs(15*cos(o))
                tpy = t.states_pair[1].point[1] + abs(15*cos(o))
            elif t.states_pair[0].point[1] < t.states_pair[1].point[1]:
                fpy = t.states_pair[0].point[1] + abs(15*cos(o))
                tpy = t.states_pair[1].point[1] - abs(15*cos(o))
                
            if t.states_pair[0].point[0] > t.states_pair[1].point[0]:  #x
                fpx = t.states_pair[0].point[0] - abs(15*sin(o))
                tpx = t.states_pair[1].point[0] + abs(15*sin(o))
            elif t.states_pair[0].point[0] < t.states_pair[1].point[0]:
                fpx = t.states_pair[0].point[0] + abs(15*sin(o))
                tpx = t.states_pair[1].point[0] - abs(15*sin(o))
            
        if t.peer_flag == None:
            t.obj_id = self.canvas.create_line(fpx, fpy, tpx, tpy,
                                fill='black', width=1,
                                arrow=LAST, smooth=True)
            return
        elif t.peer_flag == 1:
            #print "peer flag 1"
            if fpx == tpx:
                #print "fpx == tpx"
                mdx = (fpx+tpx)/2 -10
                mdy = (fpy+tpy)/2 
            elif fpy == tpy:
                #print "fpy == tpy"
                mdx = (fpx+tpx)/2 
                mdy = (fpy+tpy)/2 -10
            else:
                tan = float(fpx-tpx)/float(fpy-tpy)
                o = atan(tan)
                if (fpx-tpx)/(fpy-tpy) > 0:
                    mdx = (fpx+tpx)/2 + abs(10*cos(o))
                    mdy = (fpy+tpy)/2 - abs(10*sin(o))
                else:
                    mdx = (fpx+tpx)/2 + abs(10*cos(o))
                    mdy = (fpy+tpy)/2 + abs(10*sin(o))
            
        elif t.peer_flag == 2:
            #print "peer flag 2"
            if fpx == tpx:
                #print "fpx == tpx"
                mdx = (fpx+tpx)/2 + 10
                mdy = (fpy+tpy)/2 
            elif fpy == tpy:
                #print "fpy == tpy"
                mdx = (fpx+tpx)/2 
                mdy = (fpy+tpy)/2 + 10
            else:
                tan = float(fpx-tpx)/float(fpy-tpy)
                o = atan(tan)
                #print o, abs(10*cos(o)), abs(10*sin(o))
                if (fpx-tpx)/(fpy-tpy) > 0:
                    mdx = (fpx+tpx)/2 - abs(10*cos(o))
                    mdy = (fpy+tpy)/2 + abs(10*sin(o))
                else:
                    mdx = (fpx+tpx)/2 - abs(10*cos(o))
                    mdy = (fpy+tpy)/2 - abs(10*sin(o))
                    
        else:
            print "This should not happen"
            
        t.obj_id = self.canvas.create_line(fpx, fpy, mdx, mdy, tpx, tpy,
                                    fill='black', width=1,
                                    arrow=LAST, smooth=True)
        return

    def transitionAtPoint(self, x, y):
        ids = self.canvas.find_overlapping(x-2, y-2, x+2, y+2)
        for id in ids:
            if id:
                for trans in self.transitions:
                    if id == trans.obj_id: return trans
        return None        
        
    def stateAtPoint(self, x, y):
        ids = self.canvas.find_overlapping(x-2, y-2, x+2, y+2)
        for id in ids:
            if id:
                for state in self.states:
                    if id == state.obj_id: return state
        return None              

    def editTransition(self, t):
        return

    def setInitialState(self):
        return

    def setFinalState(self):
        return

    def changeTool(self, tool):
        #self.canvas.bind('<Button-1>',        self.arrow_tool.mouseClicked)
        self.canvas.bind('<ButtonPress-1>',   tool.mousePressed)
        self.canvas.bind('<B1-Motion>',       tool.mouseDragged)
        self.canvas.bind('<ButtonRelease-1>', tool.mouseReleased)
        
    def onQuit(self):
        self.realquit()

    def dump(self):
        print "states:"
        for s in self.states:
            print s, s.label
            for _t in s.trans_list:
                print _t
        print "transitions:" 
        for t in self.transitions:
            print t
            for _s in t.states_pair:
                print _s, _s.label
        
    
        
if __name__ == '__main__':

    root = Tk()                                # make, run a automata object
    automata(root)
    root.mainloop()
    
        

    
