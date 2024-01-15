use bevy::{
    log::{Level, LogPlugin},
    prelude::*,
};
use bevy_flycam::prelude::*;

pub(crate) mod states;
pub(crate) mod entities;
pub(crate) mod loading;
pub(crate) mod scene;

use loading::SimulationLoaderPlugin;
use scene::SimulationScenePlugin;

pub(crate) const DEFAULT_CAMERA_SPEED: f32 = 40.0;

#[bevy_main]
fn main() {
    let mut app = App::new();
    app.add_state::<states::SimulationState>()
        .add_plugins(DefaultPlugins.set(LogPlugin {
            filter: "info,wgpu_core=warn,wgpu_hal=warn,bevy_gltf=error,mygame=debug".into(),
            level: Level::DEBUG,
        }))
        // Camera settings
        .insert_resource(MovementSettings {
            speed: DEFAULT_CAMERA_SPEED,
            ..Default::default()
        })
        .add_plugins(NoCameraPlayerPlugin)
        // Internal plugins
        .add_plugins(SimulationLoaderPlugin)
        .add_plugins(SimulationScenePlugin)
        .add_systems(Update, bevy::window::close_on_esc)
        .run();
}
