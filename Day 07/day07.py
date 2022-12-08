class Filesystem:
    def __init__(self, root_name):
        self.files = []
        self.folders = []
        self.root = self.Folder(root_name)
        self.folders.append(self.root)
        self.pwd = self.root

    class Folder:
        def __init__(self, name, parent=None):
            self.name = name
            self.parent = parent
            self.children = []
            self.size = None

        def add_child(self, child):
            self.children.append(child)

        def get_size(self):
            if self.size is None:
                self.size = sum([child.get_size() for child in self.children])
                return self.size
            else:
                return self.size

    class File:
        def __init__(self, name: str, size: int, parent):
            self.parent = parent
            self.size = size
            self.name = name

        def get_size(self):
            return self.size

    def add_folder(self, new_folder_name: str):
        new_folder = self.Folder(new_folder_name, self.pwd)
        self.folders.append(new_folder)
        self.pwd.add_child(new_folder)

    def add_file(self, file_name, file_size):
        new_file = self.File(file_name, file_size, self.pwd)
        self.pwd.add_child(new_file)
        self.files.append(new_file)

    def nav_down(self, down_folder_name: str):
        for child in self.pwd.children:
            if child.name == down_folder_name:
                self.pwd = child

    def nav_up(self):
        self.pwd = self.pwd.parent


def day07(filepath, delete_dir=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    filesystem = Filesystem('/')
    for line in lines[2:]:
        if line[:3] == 'dir':
            filesystem.add_folder(line.split()[-1])
        elif line[0].isdigit():
            filesystem.add_file(line.split()[1], int(line.split()[0]))
        elif line.strip() == '$ cd ..':
            filesystem.nav_up()
        elif line[:4] == '$ cd':
            filesystem.nav_down(line.split()[-1])
        else:
            pass

    if not delete_dir:
        total = 0
        for folder in filesystem.folders:
            if folder.get_size() <= 100000:
                total += folder.get_size()

        return total
    else:
        min_delete = filesystem.root.get_size() - 40000000
        min_delete_actual = 7000000000000
        for folder in filesystem.folders:
            if folder.get_size() > min_delete:
                if folder.get_size() < min_delete_actual:
                    min_delete_actual = folder.get_size()
        return min_delete_actual


def main():
    assert day07('test07') == 95437
    print(day07('input07'))

    assert day07('test07', True) == 24933642
    print(day07('input07', True))


if __name__ == '__main__':
    main()
