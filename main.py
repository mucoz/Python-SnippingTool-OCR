import window, os
from logger import Logger as log
from configurator import Config


def main():

    log.start()
    Config.verify()
    log.info("Window is being created...")
    win = window.MainWindow()
    if os.path.exists("screenshot.png"):
        log.info("Screen shot will be deleted...")
        os.remove("screenshot.png")
        log.info("Screen shot has been deleted.")

    log.info("Window has been closed.")
    log.finish()


if __name__ == "__main__":
    main()
