# Traffic-Simulator
[WORK IN PROGRESS] Graphical simulation of traffic in Python.

A simulation of traffic, inspired by (the little) traffic on Interstate 95 in Maine, near Colby College.

I created this in PyCharm Community Edition. This project needs Zelle's Graphics package installed in the project interpreter:

In PyCharm CE, go to Preferences... > Project: Freeway Simulator > Project Interpreter. Press the plus sign in the bottom left corner and search "Graphics." You want the package created by John Zelle. Install the package, and then the program should run correctly. Poke around and change up the file, take a look, hopefully I explained each function well! There are many different variables at the beginning of the file that can be changed!

PLANNED UPDATES:

-Ability to simulate without graphics, but on a much larger scale

-Different scenarios, demonstrating the functionality of the simulation

POTENTIAL UPDATES:

-Ability for user to change the parameters through the GUI and reset the simulation 

-Traffic cops

-Two-way traffic

-Better graphics (would take a really long time)

MISTAKES THAT I MADE THAT I WILL IMPROVE UPON IN MY NEXT PROJECT:

(1) -----
I didn't make this program modular enough, meaning I should have used multiple files (i.e. a file for the Lanes, another for the Vehicles, etc.). This issue stemmed from the fact that I hadn't programmed in Python since last summer, and so part of creating this project involved me relearning how Python works. Making this program modular would reduce dependency issues and make the code much easier to read and debug and understand.

This issue came up while I was figuring out how to create scenarios. It doesn't seem like I will be able to create an individual scenario without copy-pasting the entire code into the file of the scenario. To fix this mistake, I would have to pretty much rewrite the whole thing, but if I am to rewrite the whole thing I might as well rewrite it in a different language and/or use a better, more advanced, smoother graphics engine.

Is rewriting this simulation a possibility for the future? Absolutely. It will have to be a wholly new project. But for right now (within the next >year), at my current stage as a computer programmer, I feel as if it would be most beneficial for me to explore different topics so I can get practice with creating as many types of software as possible. 
