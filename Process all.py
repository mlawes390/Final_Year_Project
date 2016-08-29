import os
import subprocess
import shlex
import re
import datetime
from Autotonomous import gen_filename, rfcomms, acquisition


def main():
    config = {
            }
    acquisition(config)


if __name__ == "__main__":
    main()
