# Virtual gimbal-camera

This is a  project to be able to crop, zoom and stabilize a feed from a 180+ degree camera.


## Install

Do the following commands

Linux, macOS
```bash
git clone git@github.com:Clear-Sight/virtual-gimbal-camera.git
cd virtual-gimbal-camera/
```
and then
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
You will need to modify the `config.json` for setting upp the configuration that will work for you. 

## Dependencies

In order to use VGC you will need a integration tool to comunicate with VGC. 
A simple way of doing this is by using the [vgc-stream-debugger](https://github.com/Clear-Sight/vgc-stream-debugger). 
The debugger has the tools for communication with the vgc. The debugger is simple and can be extracted and integrated into a webserver for example.

## Run VGC

Linux, macOS
```bash
sh run.sh
# or 
python3 -m vgc
```

## Testing 
We use `pytest` for testing. Make sure that you are in a virtual environment with all the `requirements.txt` installed. Make sure that you are in the virtual-gimbal-camera directory, then you can simply run the command: 
```bash
pytest
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Clear-Sight/virtual-gimbal-camera/blob/development/README.md) file for details.

## Contributing
Contributing to the project is limited due to it bing a bachelor's project for a certian time peroid se the [contributing.md](https://github.com/Clear-Sight/drone-feed-cropping/blob/development/.github/contributing.md) for more ditalis. 

## Coding style 
The project follows the standard notation for Python [PEP8](https://pep8.org/).

## Acknowledgments
This project was requested by [Sjöräddningssällskapet](https://www.sjoraddning.se/) togheter with [Linköping University](https://liu.se/) as a bachelor's project for the [Department of Computer and Information Science](https://www.ida.liu.se/). 
