package pyramidtrace

const FUNCTION = 0
const CLASS = 1

var masterTree struct {
	projects []*project
}

func addProject(p *project) {
	masterTree.projects = append(masterTree.projects, p)
}

type project struct {
	name  string
	files []*file
}

func (p *project) addFile(f *file) {
	p.files = append(p.files, f)
}

type file struct {
	name    string
	members []*member
}

func (f *file) addMember(m *member) {
	f.members = append(f.members, m)
}

type member struct {
	mType   int
	name    string
	members []*member
}

func (m *member) addMember(f *member) {
	m.members = append(m.members, f)
}
