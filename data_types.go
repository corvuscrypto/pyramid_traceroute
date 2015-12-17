package pyramidtrace

// pyID (python object id) is [parent 0xXXXXXXXX identifier, 0xXXXXXXXX]

type pyID uint32
type pythonType int
type subTreeNode struct {
	Depth  int
	Tokens []*Token
}

var defMap = map[uint32]*Token{}

const (
	pFunc pythonType = iota
	pClass
)

type tracer []pyID

type Token struct {
	Type     int
	Parent   *Token
	Children []*Token
	Name     string
}

func (t Token) GetSubTree() string {
	var depthChar = "   "
	var depthPrefix = "|--"
	var currDepth = 0
	var treeString string
	a := t.walk(0)
	for _, v := range a {
		if v.Depth < currDepth {
			currDepth--
			depthPrefix = depthPrefix[3:]
		} else if v.Depth > currDepth {
			currDepth++
			depthPrefix = depthChar + depthPrefix
		}
		for _, s := range v.Tokens {
			treeString += depthPrefix + s.Name
		}
	}
	return "" //for now
}

func (t Token) walk(depth int) []subTreeNode {
	var a = []subTreeNode{}
	for _, v := range t.Children {
		a = append(a, v.walk(depth+1)...)
	}
	return a
}
