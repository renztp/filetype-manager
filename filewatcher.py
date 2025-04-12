import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from yaml import safe_load
import shutil
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
YAML_CONFIG = os.path.expanduser("~/Documents/config.yaml")



class ConfigReader:
    def __init__(self, path):
        try:
            with open(path, 'r') as file:
                self.config = safe_load(file)
        except FileNotFoundError:
            print("Error, Config file does not exist")

    def read_yaml(self):
        print(self.config)

    def get_by_filetype(self, filetype):
        filetypes_configs = self.config['filetypes']
        config_matched_filetype = filetype in filetypes_configs
        if config_matched_filetype:
            return self.config['filetypes'][filetype]

    def get_watch_directory(self):
        return os.path.expanduser(self.config['watch_directory'])


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            config_reader = ConfigReader(YAML_CONFIG)
            src_path = event.src_path;
            filetype = src_path.split(".")[-1]
            config_dest_path = config_reader.get_by_filetype(filetype)
            if config_dest_path:
                shutil.move(src_path, config_dest_path)
                logging.info(f"file: {src_path} moved to {config_dest_path}")
            # print(f"Created: {filetype}, File Type: {filetype[-1]}")

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"Modified: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            logging.info(f"Moved: {event.src_path} to {event.dest_path}")



def main():
    observer = Observer()
    event_handler = MyHandler()
    config_reader = ConfigReader(YAML_CONFIG)
    watch_directory = config_reader.get_watch_directory()
    if(not os.path.exists(watch_directory)):
        logging.error("Watch directory does not exist. Exiting...")
        return;
    logging.info("Starting to watch directory: %s", watch_directory)
    observer.schedule(event_handler, watch_directory, recursive=True)

    try:
        observer.start()
        logging.info("Observer started. Press Ctrl+C to stop.")
    except KeyboardInterrupt:
        logging.error("Stopping observer...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
