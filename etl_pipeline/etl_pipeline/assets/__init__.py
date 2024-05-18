from dagster import load_assets_from_modules, file_relative_path

from . import bronze, silver, gold, platium, ml, eda


bronze_layer_assets = load_assets_from_modules([bronze])
silver_layer_assets = load_assets_from_modules([silver])
gold_layer_assets = load_assets_from_modules([gold])
platinum_layer_assets = load_assets_from_modules([platium])
ml_layer_assets = load_assets_from_modules([ml])
eda_layer_assets = load_assets_from_modules([eda])
