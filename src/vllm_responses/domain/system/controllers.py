from litestar import Controller, Response, get


class SystemController(Controller):
    tags = ["System"]

    @get(
        path="/system/health",
        operation_id="SystemHealth",
        name="system:health",
        cache=False,
        summary="System Health",
        description="Execute a health check.",
    )
    async def health(self) -> Response[bytes]:
        # TODO: check vllm engine status
        return Response(content=b"")

    @get(
        path="/system/ping",
        operation_id="SystemPing",
        name="system:ping",
        cache=False,
        summary="System Ping",
        description="Return a simple ping response.",
    )
    async def ping(self) -> Response[str]:
        return Response(content="pong")
