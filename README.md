# Virtual gimbal-camera

This is a  project to be able to crop, zoom and stabilize a feed from a 180+ degree camera and send the video stream to a web server.


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
sudo sh install.sh
```
You will need to modify the `config.json` for setting upp the configuration that will work for you. You will mainly need to change the input and output domain for the video stream.

## Dependencies

In order to use VGC you will need a integration tool to comunicate with VGC.
A simple way of doing this is by using the [vgc-stream-debugger](https://github.com/Clear-Sight/vgc-stream-debugger).
The debugger has the tools for communication with the vgc. The debugger is simple and can be extracted and integrated into a web server for example. Checkout [Clear-Sight/flask-video-stream](https://github.com/Clear-Sight/flask-video-stream) for an example of how you can use a web server for streaming the video stream. 

## Run VGC

Linux, macOS
```bash
sh run.sh
# or
python3 -m vgc
```

## Releases

[virtual-gimbal-camera releases](https://github.com/Clear-Sight/virtual-gimbal-camera/releases) are available as tags on GitHub.

## Error logs

If you run in to problems you can checkout the `.logs/`
```bash
cd vgc/.logs/
tree
.
├── log.txt
├── vgc-04-21-2021.log
├── vgc-04-29-2021.log
├── vgc-05-03-2021.log
└── vgc-05-19-2021.log
```

## Testing
We use `pytest` for testing. Make sure that you are in a virtual environment with all the `requirements.txt` installed. Make sure that you are in the virtual-gimbal-camera directory, then you can simply run the command:
```bash
pytest
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Clear-Sight/virtual-gimbal-camera/blob/development/README.md) file for details.

## Contributing
Contributing to the project was limited due to it being a bachelor's project, after *2021-05-25* anyone can contribute, see the [contributing.md](https://github.com/Clear-Sight/drone-feed-cropping/blob/development/.github/contributing.md) for more digitalis. For contributors checkout our [contributors](https://github.com/orgs/Clear-Sight/people).

## Coding style
The project follows the standard notation for Python [PEP8](https://pep8.org/).
For ore style notation checkout [.pylintrc](https://github.com/Clear-Sight/virtual-gimbal-camera/blob/development/.pylintrc)

## Acknowledgments
This project was requested by [Sjöräddningssällskapet](https://www.sjoraddning.se/) togheter with [Linköping University](https://liu.se/) as a bachelor's project for the [Department of Computer and Information Science](https://www.ida.liu.se/).
