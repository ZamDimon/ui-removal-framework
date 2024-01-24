# :mountain: Simulation

Computer simulation written in [_Rust_](https://www.rust-lang.org/). Simulation is primarily done to provide the neural network with training data. The simulation is based on the [_Bevy_](https://bevyengine.org/) game engine.

## :page_with_curl: Prerequisites

- [`rustc`], [`cargo`] >= 1.71.0 - the simulation is written in _Rust_, so you need to install the Rust compiler and package manager.
- [`cargo-make`].

[`rustc`]: https://www.rust-lang.org/tools/install
[`cargo`]: https://doc.rust-lang.org/cargo/getting-started/installation.html
[`cargo-make`]: https://sagiegurari.github.io/cargo-make/

As we are using _Bevy_ for development, follow the [Bevy Linux Dependencies](https://github.com/bevyengine/bevy/blob/main/docs/linux_dependencies.md) page to install the required dependencies.

## :running_man: How to run?

Simply run

```bash
cargo run
```

Then you can fly around using <kbd>W</kbd>, <kbd>A</kbd>, <kbd>S</kbd>, <kbd>D</kbd> for moving in the horizontal plane and <kbd>Space</kbd> with <kbd>Shift</kbd> to move up and down.
