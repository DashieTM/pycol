#import "template.typ": *

#show: doc => conf(
  author: "Kaj Habegger & Fabio Lenherr",
  "PySnake",
  "Miniproject",
  doc,
)

#section[Introduction]
We decided to do a small reinforcement learning project.
As we have never done anything in terms of reinforcement learning before, we used this #link("https://www.youtube.com/watch?v=L8ypSXwyBds&list=WL&index=26")[video] as a starting point. It is a tutorial of creating a Snake game and design a reinforcement learning AI model which is able to play the game after some iterations.

#section[Tooling]
Like the guy in the tutorial we used Pytorch to design our AI model and Pygame to create our game. It is worth pointing out that we planned to use Pytorch anyway because we wanted to try out another tool than Tensorflow. Furthermore, Pytorch also supports AMD graphic cards and not only Nvidia graphic cards like Tensorflow. Pygame is a composition of Python modules like computer graphic and sound libraries. Creating a game with Pygame is straightforward.

#section[Making Of]

#subsection[The Game]
We wanted to create our own little game and not just copy the game from the tutorial we watched. Therefore, we designed a two dimensional game where the player is a small ball and has to collect or eat other balls. There are two different types of balls to eat; green and red ones. By collecting a green ball the player grows in size and diminishes when collecting red balls respectively. If the player has minimal size and collects a red ball the game is over. Touching the wall also ends the game. As the player grows each time eating a green ball it gets more difficult over time to avoid the wall as well as red balls.

#subsection[The AI]