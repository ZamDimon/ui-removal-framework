//! Provides the systems for the simulation scene that are related to [`SimulationState::Loading`] state.

use bevy::{
    asset::LoadState,
    gltf::Gltf,
    log,
    prelude::*,
    render::render_resource::{TextureViewDescriptor, TextureViewDimension},
};

use crate::states::SimulationState;

use super::resources::{SimulationAssetHandles, SkyboxAsset, TerrainAsset};

/// System for starting loading assets
pub(super) fn load_meshes_system(
    asset_server: Res<AssetServer>,
    mut simulation_asset_handles: ResMut<SimulationAssetHandles>,
) {
    *simulation_asset_handles = SimulationAssetHandles {
        terrain: TerrainAsset {
            gltf: asset_server.load("models/plane.glb"),
            ..default()
        },
        skybox: SkyboxAsset::new(&asset_server, "textures/skybox_3"),
    };
}

/// System for checking if all handles are loaded and moving to the next state if they are.
pub(super) fn check_handles_system(
    asset_server: Res<AssetServer>,
    assets_images: ResMut<Assets<Image>>,
    gltf_assets: ResMut<Assets<Gltf>>,
    materials_assets: ResMut<Assets<StandardMaterial>>,
    mut simulation_asset_handles: ResMut<SimulationAssetHandles>,
    mut next_state: ResMut<NextState<SimulationState>>,
) {
    let handles = [
        simulation_asset_handles.terrain.gltf.id(),
        simulation_asset_handles.skybox.diffuse_map.id(),
        simulation_asset_handles.skybox.specular_map.id(),
    ];

    if asset_server.get_group_load_state(handles) != LoadState::Loaded {
        return;
    }

    log::info!("All meshes are loaded");

    handle_skybox_texture(assets_images, &mut simulation_asset_handles.skybox);
    handle_terrain_scene(
        gltf_assets,
        materials_assets,
        &mut simulation_asset_handles.terrain,
    );

    next_state.set(SimulationState::Active);
}

/// This function checks whether the skybox texture's layer count is 1, and if it is,
/// it reinterprets the image as a cube map.
pub(super) fn handle_skybox_texture(
    mut assets_images: ResMut<Assets<Image>>,
    skybox: &mut SkyboxAsset,
) {
    let images_to_interpret = [&skybox.diffuse_map, &skybox.specular_map];

    for skybox_image in images_to_interpret {
        // Interpreting the skybox handle as a cube map
        let image = assets_images.get_mut(skybox_image).unwrap();
        if image.texture_descriptor.array_layer_count() == 1 {
            image.reinterpret_stacked_2d_as_array(
                image.texture_descriptor.size.height / image.texture_descriptor.size.width,
            );
            image.texture_view_descriptor = Some(TextureViewDescriptor {
                dimension: Some(TextureViewDimension::Cube),
                ..default()
            });
        }
    }
}

/// This function sets the reflectance and
/// perceptual roughness of the terrain material to 0.0 and 1.0
pub(super) fn handle_terrain_scene(
    mut gltf_assets: ResMut<Assets<Gltf>>,
    mut materials_assets: ResMut<Assets<StandardMaterial>>,
    terrain: &mut TerrainAsset,
) {
    let terrain_gltf = gltf_assets
        .get_mut(&terrain.gltf)
        .expect("terrain gltf file must be loaded at this point");

    for material_handle in terrain_gltf.materials.iter() {
        let Some(material) = materials_assets.get_mut(material_handle) else {
            continue;
        };

        // Setting reflectance and perceptual roughness to remove the shinessness of
        // the terrain mesh
        material.reflectance = 0.0;
        material.perceptual_roughness = 1.0;
        material.metallic = 0.0;
        material.alpha_mode = AlphaMode::Opaque;
    }

    terrain.scene = terrain_gltf.scenes[0].clone();
}
