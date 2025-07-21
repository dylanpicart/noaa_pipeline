import graphene
from resolvers.buoy_resolver import resolve_buoy_data, BuoyData
from resolvers.pmn_resolver import resolve_pmn_data, PMNData
from resolvers.climate_resolver import resolve_climate_data, ClimateData
from resolvers.chlorophyll_resolver import resolve_chlorophyll_data, ChlorophyllData

class Query(graphene.ObjectType):
    get_buoy_data = graphene.List(
        BuoyData, station_id=graphene.String(required=True), limit=graphene.Int(default_value=100)
    )
    get_pmn_data = graphene.List(
        PMNData, limit=graphene.Int(default_value=100)
    )
    get_climate_data = graphene.List(
        ClimateData,
        dataset_id=graphene.String(required=True),
        location_id=graphene.String(required=True),
        start_date=graphene.DateTime(required=True),
        end_date=graphene.DateTime(required=True),
        limit=graphene.Int(default_value=100)
    )
    
    get_chlorophyll_data = graphene.List(
        ChlorophyllData,
        start_date=graphene.DateTime(required=True),
        end_date=graphene.DateTime(required=True),
        limit=graphene.Int(default_value=100)
    )


    def resolve_get_buoy_data(root, info, station_id, limit):
        return resolve_buoy_data(station_id, limit)

    def resolve_get_pmn_data(root, info, limit):
        return resolve_pmn_data(limit)

    def resolve_get_climate_data(root, info, dataset_id, location_id, start_date, end_date, limit):
        return resolve_climate_data(dataset_id, location_id, start_date, end_date, limit)
    
    def resolve_get_chlorophyll_data(root, info, start_date, end_date, limit):
        return resolve_chlorophyll_data(start_date, end_date, limit)

schema = graphene.Schema(query=Query)
