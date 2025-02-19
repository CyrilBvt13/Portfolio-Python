from .groups import Groups
from .flows import FlowsRoute, FlowRoute, NewFlowRoute

def initialize_routes(api):
    api.add_resource(Groups, "/groups/")
    
    api.add_resource(FlowsRoute, "/flows/<group_id>")
    api.add_resource(NewFlowRoute, "/flow/")
    api.add_resource(FlowRoute, "/flow/<flow_id>")