import cv2
from . import primes
from . import buffer
from . import io
from . import config

__version__ = "0.1.0"


def main():
    print(primes.primes(100))



if __name__ == '__main__':
    if config.CONFIG['debug']:
        main()
