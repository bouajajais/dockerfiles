import sys
from config import init_config
from images import update_images, list_images

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        init_config()
    elif len(sys.argv) > 1 and sys.argv[1] in ("images", "list"):
        keywords = sys.argv[2:]
        list_images(keywords)
    else:
        update_images()
    
if __name__ == "__main__":
    main()