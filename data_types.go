package pyramidtrace

type project struct {
	name  string
	files []*file
}

type file struct {
	name      string
	functions []*function
	classes   []*class
}

type function struct {
	name      string
	functions []*function
}

type class struct {
	name      string
	functions []*function
}
