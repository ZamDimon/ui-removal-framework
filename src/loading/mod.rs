//! Provides loader for simulation scene that loades required for scene assets.

use bevy::prelude::*;

use crate::states::SimulationState;

pub(crate) mod resources;
pub(crate) mod systems;

pub struct SimulationLoaderPlugin;

impl Plugin for SimulationLoaderPlugin {
    fn build(&self, app: &mut App) {
        // Load meshes.
        app.init_resource::<resources::SimulationAssetHandles>()
            .add_systems(
                OnEnter(SimulationState::Loading),
                systems::load_meshes_system,
            )
            // Wait until meshes are loaded, and then update inner state to next one.
            .add_systems(
                Update,
                systems::check_handles_system.run_if(in_state(SimulationState::Loading)),
            );
    }
}
