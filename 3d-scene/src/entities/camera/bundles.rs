//! Orbit camera bundles package
use std::ops::Range;

use bevy::{
    core_pipeline::{bloom::BloomSettings, Skybox},
    prelude::*,
};
use bevy_flycam::FlyCam;
use rand::Rng;

/// Bundle containing all the components (hdr, lighting, camera3d etc.) needed for the orbit camera.
#[derive(Bundle)]
pub struct MainCameraBundle {
    pub camera_3d_bundle: Camera3dBundle,
    pub environment_map_light: EnvironmentMapLight,
    pub fog_settings: FogSettings,
    pub bloom_settings: BloomSettings,
    pub skybox: Skybox,
    pub ui_config: UiCameraConfig,
    pub flycam: FlyCam,
}

pub(super) const BLOOM_INTENSITY: f32 = 0.25;
pub(super) const FOG_COLOR: Color = Color::rgba(0.05, 0.05, 0.05, 1.0);
pub(super) const FOG_FALLOFF_RANGE: (f32, f32) = (-10.0, 10000.0);

pub(super) const CAMERA_POS_X_RANGE: Range<f32> = 0.0..1000.0;
pub(super) const CAMERA_POS_Y: f32 = 200.0;
pub(super) const CAMERA_POS_Z_RANGE: Range<f32> = 0.0..1000.0;

impl MainCameraBundle {
    /// Based on the skyboxes's diffuse+specular maps, and the pinned entity,
    /// creates a new bundle for the orbit camera.
    pub fn new(diffuse_map: &Handle<Image>, specular_map: &Handle<Image>) -> Self {
        let mut rng = rand::thread_rng();

        let camera_position = Vec3::new(
            rng.gen_range(CAMERA_POS_X_RANGE),
            CAMERA_POS_Y,
            rng.gen_range(CAMERA_POS_Z_RANGE),
        );

        Self {
            camera_3d_bundle: Camera3dBundle {
                camera: Camera {
                    hdr: true,
                    ..default()
                },
                transform: Transform::from_translation(camera_position),
                ..default()
            },
            skybox: Skybox(diffuse_map.clone()),
            environment_map_light: EnvironmentMapLight {
                diffuse_map: diffuse_map.clone(),
                specular_map: specular_map.clone(),
            },
            fog_settings: FogSettings {
                color: FOG_COLOR,
                falloff: FogFalloff::Linear {
                    start: FOG_FALLOFF_RANGE.0,
                    end: FOG_FALLOFF_RANGE.1,
                },
                ..default()
            },
            ui_config: UiCameraConfig { show_ui: false },
            bloom_settings: BloomSettings {
                intensity: BLOOM_INTENSITY,
                ..Default::default()
            },
            flycam: FlyCam,
        }
    }
}
