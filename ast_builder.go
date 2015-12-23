package pyramidtrace

import (
	"bytes"
	"log"
	"os/exec"
	"strconv"
	"strings"
)

type astFunc struct {
	depth int
	name  string
}

func getPythonAST() {
	var pythonTokens = []*astFunc{}
	var output bytes.Buffer
	comm := exec.Command("python", "./py_files/ast_parser.py", "/home/dev04/Documents/work-projects/loans-webapp/")
	comm.Stdout = &output
	err := comm.Run()
	if err != nil {
		log.Fatal(err)
	}
	for _, v := range strings.Split(output.String(), "\n") {
		if v == "" {
			continue
		}
		//split comma
		tuple := strings.Split(v, ",")
		depth, _ := strconv.Atoi(tuple[0])
		pythonTokens = append(pythonTokens, &astFunc{depth, tuple[1]})
	}
	var i = 0
	recurseAST(&i, 0, pythonTokens, nil)
}

func recurseAST(i *int, parentIndex int, pt []*astFunc, parent interface{}) {
	parentDepth := pt[parentIndex].depth
	if parentDepth == -1 {
		parent = &project{pt[*i].name, []*file{}}
		addProject(parent.(*project))
		*i++
	}
	var lastElement interface{}
	for *i < len(pt) {
		depth := pt[*i].depth
		if depth == parentDepth+1 {
			lastElement = addToParent(pt[*i], parent)
			*i++
		} else if depth < parentDepth+1 {
			return
		} else if depth > parentDepth+1 {
			recurseAST(i, *i-1, pt, lastElement)
		} else {
			return
		}
	}
}

func addToParent(child *astFunc, parent interface{}) interface{} {
	if child.depth == 0 {
		nparent := parent.(*project)
		nchild := &file{child.name, []*member{}}
		nparent.addFile(nchild)
		return nchild
	} else if child.depth == 1 {
		nparent := parent.(*file)
		nchild := &member{0, child.name, []*member{}}
		nparent.addMember(nchild)
		return nchild
	} else {
		nparent := parent.(*member)
		nchild := &member{0, child.name, []*member{}}
		nparent.addMember(nchild)
		return nchild
	}
}

func Trace() {
	getPythonAST()
}
