from dmr.openapi import OpenAPIConfig

openapi_config = OpenAPIConfig(
    title="Deploy-or-Not-as-a-Service",
    version="1.0.0",
    summary="Should you deploy today? Let the API decide.",
    description=("A joke API that tells you whether to deploy, with extra suspicion on Fridays."),
)
