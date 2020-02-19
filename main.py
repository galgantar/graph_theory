def update_path():
    import os
    import sys
    sys.path.insert(1, os.getcwd() + "\\lib")


def main():
    from gui import Gui

    gui = Gui(1200, 600)
    gui.run()


if __name__ == "__main__":
    update_path()
    main()
