import cv2
from .primes import primes
from .io.inputAdapter import InputAdapter


__version__ = "0.1.0"


def main():
    print(primes(100))



if __name__ == '__main__':
    main()
