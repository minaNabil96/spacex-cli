# Launch Library 2 API endpoints filtered for SpaceX (Agency ID 121)

# Launches
LAUNCHES = "launch/"
# Note: In LL2 API, these are filters or separate queries
# For this implementation, we will use the base /launch/ endpoint with filters where possible
# or specific sub-endpoints if they exist in the dev version.
LAUNCH_UPCOMING = "launch/upcoming/"
LAUNCH_PREVIOUS = "launch/previous/"
LAUNCH_DETAIL = "launch/{id}/"

# Agency (Company)
COMPANY = "agencies/121/"

# Rockets & Capsules (Configurations)
ROCKETS = "config/launcher/"
CAPSULES = "config/spacecraft/"
