package main

import (
	"bytes"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strings"
)

type pythonType int

const (
	pString pythonType = iota
	pInt
	pFloat
	pBoolean
	pTuple
	pList
	pDict
)

var pythonPaths []string
var fileBuffers map[string]*bytes.Buffer

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
	Path      string
	Imports   map[string]string
	Functions map[string]*function
}

func getPythonPaths() {
	var output bytes.Buffer
	comm := exec.Command("python", "-c", "import sys;\nfor p in sys.path:\n\tprint p")
	comm.Stdout = &output
	if comm.Run() != nil {
		log.Fatal("Can't find python paths")
	}
	for _, v := range strings.Split(output.String(), "\n") {
		pythonPaths = append(pythonPaths, v)
	}
}

func getFileBuffer(filePath string) *bytes.Buffer {
	var newBuffer bytes.Buffer
	if r, ok := fileBuffers[filePath]; ok {
		return r
	}
	f, err := os.Open(filePath)
	defer f.Close()
	if err != nil {
		log.Fatal(err)
	}
	data, _ := ioutil.ReadAll(f)
	newBuffer.Write(data)
	fileBuffers[filePath] = &newBuffer
	return &newBuffer
}

func main() {
	getPythonPaths()
}
