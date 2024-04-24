from os.path import abspath, basename, dirname, join


# ##### PATH CONFIGURATION ################################

# fetch FastAPI's project directory
BASE_DIR = dirname(dirname(abspath(__file__)))

# the name of the whole site
SITE_NAME = basename(BASE_DIR)
