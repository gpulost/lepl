
from unittest import TestCase


from lepl.graph \
    import ArgAsAttributeMixin, preorder, postorder, reset, ConstructorWalker, \
           Clone, make_proxy


class Node(ArgAsAttributeMixin):
    
    def __init__(self, label, *children):
        super(Node, self).__init__()
        self._arg(label=label)
        self._args(children=children)
        
    def __str__(self):
        return str(self.label)
    
    def __repr__(self):
        args = [str(self.label)]
        args.extend(map(repr, self.children))
        return 'Node(%s)' % ','.join(args)
    

def graph():
    return Node(1,
                Node(11,
                     Node(111),
                     Node(112)),
                Node(12))
        
        
class OrderTest(TestCase):
    
    def test_preorder(self):
        result = [node.label for node in preorder(graph())]
        assert result == [1, 11, 111, 112, 12], result
        
    def test_postorder(self):
        result = [node.label for node in postorder(graph())]
        assert result == [111, 112, 11, 12, 1], result
        
        
class ResetTest(TestCase):
    
    def test_reset(self):
        nodes = preorder(graph())
        assert next(nodes).label == 1
        assert next(nodes).label == 11
        reset(nodes)
        assert next(nodes).label == 1
        assert next(nodes).label == 11


class CloneTest(TestCase):
    
    def test_simple(self):
        g1 = graph()
        g2 = ConstructorWalker(g1)(Clone())
        assert repr(g1) == repr(g2)
        assert g1 is not g2
    
    def assert_same(self, text1, text2):
        assert self.__clean(text1) == self.__clean(text2), self.__clean(text1)
    
    def __clean(self, text):
        depth = 0
        result = ''
        for c in text:
            if c == '<':
                depth += 1
            elif c == '>':
                depth -= 1
            elif depth == 0:
                result += c
        return result

    def test_loop(self):
        (s, n) = make_proxy()
        g1 = Node(1,
                Node(11,
                     Node(111),
                     Node(112),
                     n),
                Node(12))
        s(g1)
        g2 = ConstructorWalker(g1)(Clone())
        self.assert_same(repr(g1), repr(g2))

    def test_loops(self):
        (s1, n1) = make_proxy()
        (s2, n2) = make_proxy()
        g1 = Node(1,
                Node(11,
                     Node(111, n2),
                     Node(112),
                     n1),
                Node(12, n1))
        s1(g1)
        s2(next(g1._children()))
        g2 = ConstructorWalker(g1)(Clone())
        self.assert_same(repr(g1), repr(g2))
        
    def test_loops_with_proxy(self):
        (s1, n1) = make_proxy()
        (s2, n2) = make_proxy()
        g1 = Node(1,
                Node(11,
                     Node(111, n2),
                     Node(112),
                     n1),
                Node(12, n1))
        s1(g1)
        s2(next(g1._children()))
        g2 = ConstructorWalker(g1)(Clone())
        g3 = ConstructorWalker(g2)(Clone())
        self.assert_same(repr(g1), repr(g3))
        print(repr(g3))