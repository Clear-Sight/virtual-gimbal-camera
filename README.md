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
You will need to modifi the `config.json` for setting upp the configuration that will work for you. 

## Dependencies

In order to use VGC you will need integration tool to comunicate with VGC. 
A simpel way of doing this is by the [vgc-stream-debugger](https://github.com/Clear-Sight/vgc-stream-debugger). 
The dubbuger has the tools for comuniction with the vgc. The debugger is simpel and can extrated and integrated in to example a webserver. 

## Run VGC

Linux, macOS
```bash
sh run.sh
# or 
python3 -m vgc
```

## Testing 
We use `pytest` for testing. Make sure that you are in a vertual enverorment with all the `requirements.txt` installed. Make sure that you are in the virtual-gimbal-camera directory the you can simply run the comand: 
```bash
pytest
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Clear-Sight/virtual-gimbal-camera/blob/development/README.md) file for details

## Contributing
Contributing to the project is limited due to it bing a bachelor's project for a certian time peroid se the [contributing.md](https://github.com/Clear-Sight/drone-feed-cropping/blob/development/.github/contributing.md) for more ditalis. 

## Coding style 
The project follows the standard notation for python [PEP8](https://pep8.org/).

## Acknowledgments
This project was requested by [Sjöräddningssällskapet](https://www.sjoraddning.se/) togheter with [Linköping University](https://liu.se/) as a bachelor's project for the [Department of Computer and Information Science](https://www.ida.liu.se/). 
