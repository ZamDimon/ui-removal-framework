//! Provides states for simulation scene.

use bevy::prelude::States;

#[derive(Debug, Clone, Eq, PartialEq, Hash, States, Default)]
pub enum SimulationState {
    /// Waiting until all required resources are loaded (meshes, etc.).
    #[default]
    Loading,
    /// The simulation is running.
    Active,
}
