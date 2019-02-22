from nltk.tree import Tree
    
sent = []
def get_label(t):
    try:
        return t.label()
    except:
        return t
        
for x in open('skladnica_with_heads.txt'):
     L = []
     for w in unicode(x,'utf8').split():
            L.append(w.split('@')[0])
        
     sent.append(Tree.fromstring(' '.join(L)))    

def traverse_tree(t):
    if type(t) != unicode:
        head = t.label()
        children = [get_label(c) for c in t ]
        print '    ', head, '==>', ' '.join(children)
        for s in t:
            traverse_tree(s)
                  
for s in sent:
    print ' '.join(s.leaves())
    traverse_tree(s)
    print
    

 
