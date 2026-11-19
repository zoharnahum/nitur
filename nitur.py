#https://github.com/zoharnahum/nitur
import os
import time
import logging
import shutil

imgs = ('jpg','jpeg','png')

log_file = open("activity.log", "a", encoding="utf-8")
file_handler = logging.StreamHandler(log_file)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(message)s")
)
logger = logging.getLogger("folder_monitor")
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(file_handler)
logger.propagate = False


def get_files():
    '''
    :return: returns files in path if path exist
    '''
    files = {}
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            try:
                files[path] = (
                    os.path.getsize(path),
                    os.path.getmtime(path)
                )
            except OSError:
                pass
    return files

def log_action(action, path):
    '''
    :param action:
    :param path:
    :return:
    '''
    message = f"{action}: {path}"
    print(message, flush=True)
    logger.info(message)

exited = False
while True:
    folder = input("Enter folder path or exit to quit ")
    photosFolder = input("Enter photos folder ")
    if folder == "exit":
        exited = True
        break
    elif not os.path.exists(folder):
        continue
    break
if not exited:
    previous = get_files()

while not exited:
    time.sleep(1)
    current = get_files()
    old_paths = set(previous)
    new_paths = set(current)
    deleted = list(old_paths - new_paths)
    created = list(new_paths - old_paths)
    # Detect possible renames
    for old_path in deleted[:]:
        for new_path in created[:]:
            if previous[old_path] == current[new_path]:
                log_action(
                    "RENAMED",
                    f"{old_path} -> {new_path}"
                )
                deleted.remove(old_path)
                created.remove(new_path)
                break
    # Detect created files
    for path in created:
        log_action("CREATED", path)
        for path in created:
            log_action("CREATED", path)
            if path.lower().endswith(imgs):
                os.makedirs(photosFolder, exist_ok=True)
                dest_path = os.path.join(photosFolder, os.path.basename(path))
                if not os.path.exists(dest_path):
                    shutil.copy2(path, dest_path)

    # Detect deleted files
    for path in deleted:
        log_action("DELETED", path)
    # Detect modifications
    for path in old_paths & new_paths:
        if previous[path] != current[path]:
            log_action("MODIFIED", path)
    previous = current


log_file.close()



