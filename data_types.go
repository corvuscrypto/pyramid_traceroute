package pyramidtrace

// pyID (python object id) is [parent 0xXXXXXXXX identifier, 0xXXXXXXXX]
type pyID [2]uint32
type pythonType int

const (
	pString pythonType = iota
	pInt
	pFloat
	pBoolean
	pTuple
	pList
	pDict
	pObject
)

func (p pythonType) toString() string {
	var a = "pStringpIntpFloatpBooleanpTuplepListpDictpObject"
	var b = []uint8{0, 7, 11, 17, 25, 31, 36, 41}
	if int(p) == len(b)-1 {
		return a[41:]
	}
	return a[b[p]:b[p+1]]
}

type tracer []pyID

type class struct {
	FullPath   string
	Methods    map[string]*function
	Attributes map[string]*variable
}

type variable struct {
	FullPath string
	Type     pythonType
	Value    interface{}
}

type function struct {
	FullPath  string
	Functions map[string]*function
	Variables map[string]*variable
}

type pythonFile struct {
	tracer
	Path      string
	Imports   map[string]string
	Functions map[string]*function
	Classes   map[string]*class
}
