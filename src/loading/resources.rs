use bevy::{gltf::Gltf, prelude::*};

/// Structure containing all the simulation assets.
#[derive(Debug, Resource, Default)]
pub struct SimulationAssetHandles {
    pub terrain: TerrainAsset,
    pub skybox: SkyboxAsset,
}

/// Structure containing handles to the skybox textures.
#[derive(Debug, Default)]
pub struct SkyboxAsset {
    pub diffuse_map: Handle<Image>,
    pub specular_map: Handle<Image>,
}

impl SkyboxAsset {
    pub fn new(asset_server: &Res<AssetServer>, skybox_folder: &str) -> Self {
        Self {
            diffuse_map: asset_server.load(format!("{}/diffuse.png", skybox_folder)),
            specular_map: asset_server.load(format!("{}/specular.png", skybox_folder)),
        }
    }
}

/// Structure containing handles to the terrain scene.
#[derive(Debug, Default)]
pub struct TerrainAsset {
    pub gltf: Handle<Gltf>,
    pub scene: Handle<Scene>,
}
