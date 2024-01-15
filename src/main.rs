use bevy::{
    prelude::*,
    log::{Level, LogPlugin}
};
use bevy_flycam::prelude::*;

pub(crate) mod states;

pub(crate) mod entities;
pub(crate) mod loading;
pub(crate) mod scene;

use loading::SimulationLoaderPlugin;
use scene::SimulationScenePlugin;

#[bevy_main]
fn main() {
    let mut app = App::new();
    app.add_state::<states::SimulationState>()
        .add_plugins(DefaultPlugins.set(LogPlugin {
            filter: "info,wgpu_core=warn,wgpu_hal=warn,bevy_gltf=error,mygame=debug".into(),
            level: Level::DEBUG,
        }))
        .add_plugins(NoCameraPlayerPlugin)
        .add_plugins(SimulationLoaderPlugin)
        .add_plugins(SimulationScenePlugin)
        .add_systems(Update, bevy::window::close_on_esc)
        .run();
}
