import sys
from config import init_config
from images import update_images

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        init_config()
    else:
        update_images()
    
if __name__ == "__main__":
    main()