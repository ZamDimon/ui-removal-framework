//! This module provides the simulation scene plugin.
//!
//! This scene is applied when [`ScenesState::Simulation`] is active.

use crate::states::SimulationState;
use bevy::prelude::*;

pub(super) mod systems;

pub struct SimulationScenePlugin;

impl Plugin for SimulationScenePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            OnEnter(SimulationState::Active),
            systems::setup_scene_system,
        );
    }
}
