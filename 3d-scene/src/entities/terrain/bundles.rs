//! Bundles needed for terrain spawning

use bevy::prelude::*;

use crate::loading::resources::SimulationAssetHandles;

/// Bundle for the terrain entity.
#[derive(Bundle)]
pub struct TerrainBundle {
    pub scene: SceneBundle,
}

pub(super) const TERRAIN_POSITION: Vec3 = Vec3::new(-9.0, -15.0, -0.0);

impl TerrainBundle {
    pub fn new(asset_handles: &Res<SimulationAssetHandles>) -> Self {
        Self {
            scene: SceneBundle {
                scene: asset_handles.terrain.scene.clone(),
                transform: Transform {
                    translation: TERRAIN_POSITION,
                    ..default()
                },
                ..default()
            },
        }
    }
}
