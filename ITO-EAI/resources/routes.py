from .groups import Groups

def initialize_routes(api):
    api.add_resource(Groups, "/groups/")