# Simulated World 🌎

*Second Programming Project*

## Description

This app is capable of reading creatures programmed in a language called *Instinct*. The creatures are placed on a terrain and left to their own devices: they can fight, feed, reproduce, and die. The app user will play God and observe their behavior from above.

## Parts of the Application ​​

- **Instinct language compiler and interpreter** 📜: reads a text file (with the .ins extension). Checks that it is lexically, syntactically, and semantically correct. Passes the interpretation to the *simulator*. Errors are reported by line number.

- **Simulated World** 🌎: a two-dimensional grid representing the terrain. On it, creatures and objects. Once the simulation begins, the world progresses in discrete turns called *ticks*. There are natural laws that must be respected: life decreases by one point each tick, whoever reaches 0 dies, whoever is attacked loses life, and whoever reaches their lifespan dies.

- **Visual Interface** 🖥️: The user loads the creatures, terrains, objects, and maps that exist in the repository, chooses an available map, places creatures where desired, presses play, and observes the simulation while accelerating, slowing down, or pausing time.

## License

[MIT](https://choosealicense.com/licenses/mit/)
