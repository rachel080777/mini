# WebGME Configuration Settings
On `npm start`, the webgme app will load `config.default.js` which will override the configuration [defaults](https://github.com/webgme/webgme/tree/master/config).

If `NODE_ENV` is set, it will first try to load the configuration settings from `config/config.ENV.js` where `ENV` is the value of `NODE_ENV`. For example,
```
NODE_ENV=debug npm start
will load the configuration settings from `config/config.debug.js` if it exists and fallback to `config/config.default.js` otherwise



Thank you for the help all semster



# miniproject
This is my CS 6388 Model-Integrated Computing final project.

## Introduction
miniproject is a comprehensive design studio for creating and playing the Othello (Reversi) game. This studio includes game logic plugins, and a meta-model for an immersive gaming experience.

## Installation Instructions
Clone Repository:

git clone  https://github.com/rachel080777/mini.git
cd myproject

### Prerequisites
1. Node.js (version 20.9.0 LTS or higher)
2. Python3 (version 3.11.0 or higher, if applicable)
3.install mongo DB ( the lastest version) on docker and create a coonatiner 

### Steps 
1. Open the terminal and clone the repository 
```git remote add origin https://github.com/rachel080777/mini.git
git clone 
cd [repository directory/myminiproject]
```
2. Install dependencies

```
Ensure you have Node.js (version 20.9.0 LTS or higher) installed.
Install necessary packages:
npm install
npm install webgme
npm install webgme-bindings
pip3 install webgme-bindings

```
3.
Set Up MongoDB:
Download and install Docker Desktop from Docker's website.
https://www.docker.com/products/docker-desktop/
Create a Docker container for MongoDB:
Set Host path: ruiqingl/downloads/DB and Container path: /data/db.
Use the following command in the terminal:
docker run -d -p 27017:27017 -v ruiqingl/downloads/DB:/data/db mongo

4. Download/Install the latest version of mongo in Docker Image.
5. Create an image of mongo. For optional settings, please set the Host path as  do pwd and find it
```
ruiqingl/downloads/DB
```
and set the Container path as
```
/data/db
```
6. Start the Application:
Run the following command:

```
node app.js
```
7. Open your browser and navigate to [http://localhost:8888].

## Implementation Description

### Structure
* src/: Contains the source code for the studio.
* plugins/: Game logic plugins (Highlight valid tiles, Counting pieces, Flipping, Undo, Auto).
* visualizers/: Visualization components for the game.
* meta/: Meta-model for the game.

## Technologies Used
1. React.js for front-end visualization.
2. Node.js for back-end services.
3. WebGME for model integration.
4. Python for creating the plugins.


## Usage Description
the visulaization its not working but if you avagative to test branch instead of the master branch , all plug in should work. remember to update it to python3

### Playing the Game
1. Start a New Game:
* Click on 'New Game' to initialize a new Othello board.
2. Making Moves:
* Click on a valid tile to place your piece.
* The valid tiles are highlighted based on the current game state.
3. Game Progression:
* The game automatically counts and displays the number of pieces for each color.
* After each move, the board updates to reflect the new state.
4. Undo Functionality:
* Click 'Undo' to revert to the previous state.
5. Auto Play (Optional):
* Click 'Auto' to let the computer make a move.

### End of the Game
* The game concludes when no valid moves are available.
* The final score is displayed, indicating the winner.

## Repository Contents
* README.md: This documentation file.
* src/: Source code directory.

## Deployment
Follow the installation instructions to deploy the miniproject on your local machine. Ensure all dependencies are installed for a smooth setup.

## Additional Notes
Branch Selection:
If visualization isn't working, switch to the 'test' branch for functional plugins.
Python Version:
Ensure the plugins are updated to use Python 3.
