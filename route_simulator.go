package main

import (
	"bytes"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strings"
)

var pythonPaths []string
var fileBuffers map[string]*bytes.Buffer

type function struct {
	Name      string
	Functions map[string]*function
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
