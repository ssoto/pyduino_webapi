# Pyduino WebAPI

A basic Flask web project displaying the status of a Arduino device.

## About
Currently we need to support two type of components:

* Relays
* Sensors

These are accessed via a web API. Depending on how you start this app, here are some of the URL endpoints that are available on port 8000:

* `GET` - `/`
* `GET` - `/<element_type>/<element_id>`
* `GET` - `/data/<element_type>/`
* `GET` - `/data/<element_type>/<id>`
* `GET` - `/turnon`  To turn on an LED
* `GET` - `/turnoff`  To turn off an LED

*Please see the code for full details on interacting with these endpoints.*

## Current Project Status
Here is a list of some of the tasks that have been done and are in progress for the project.

* [x] Arduino board is instantiated using a yml field (you can see example in project root dir): Done
* [x] Show each component status: Done using random.randint() ;)
* [ ] Write adapter class for each component type: pending
* [ ] Write basic web forms to switch relays: pending

## Contributing
Jump in and open a [pull request on github](https://github.com/ssoto/pyduino_webapi/pulls)! :)

## Development
Here are the steps to get started with development of this project.

### Setup
1. `python3 -m venv .venv` To create your virtual environment
  * *Note that this is a one-time step! You only need to do this in the very beginning of the project.*
2. `source .venv/bin/activate` To start the virtual environment
3. `pip install -r requirements.txt` To install the project dependencies

### Running the project

TBD

### Running tests

There are unit tests in this project to ensure that bugs don't creep in as we do development. To run the test
simply....

TBD 
