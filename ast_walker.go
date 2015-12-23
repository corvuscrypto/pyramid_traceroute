package pyramidtrace

func walk() {

}

func walkMasterTree() {
	var finalString = ""
	var project = masterTree.projects[0]
	for _, file := range project.files {
		//walk(file, &finalString)
	}
}
