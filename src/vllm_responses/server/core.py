from typing import TYPE_CHECKING

from litestar.plugins import CLIPluginProtocol, InitPluginProtocol


if TYPE_CHECKING:
    from click import Group
    from litestar.config.app import AppConfig


class ApplicationCore(InitPluginProtocol, CLIPluginProtocol):
    """Application core configuration plugin.

    This class is responsible for configuring the main Litestar application with our routes, guards, and various plugins

    """

    def on_cli_init(self, cli: "Group") -> None:
        pass

    def on_app_init(self, app_config: "AppConfig") -> "AppConfig":
        from vllm_responses.domain.system.controllers import SystemController

        # routes
        app_config.route_handlers.extend(
            [
                SystemController,
            ]
        )

        return app_config
