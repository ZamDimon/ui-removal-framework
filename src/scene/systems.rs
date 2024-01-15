//! This module provides system for state of the simulation scene when
//! [`SimulationState`] is active.

use bevy::prelude::*;

use crate::entities::{camera::bundles::MainCameraBundle, terrain::bundles::TerrainBundle};
use crate::loading::resources::SimulationAssetHandles;

/// System for setuping the scene
pub fn setup_scene_system(
    mut commands: Commands,
    simulation_asset_handles: Res<SimulationAssetHandles>,
) {
    // Add terrain and an infinite collider slightly above it
    commands.spawn(TerrainBundle::new(&simulation_asset_handles));

    // Add orbit camera
    commands.spawn(MainCameraBundle::new(
        &simulation_asset_handles.skybox.diffuse_map.clone(),
        &simulation_asset_handles.skybox.specular_map.clone(),
    ));
}
