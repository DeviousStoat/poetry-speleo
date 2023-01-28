from cleo.helpers import argument
from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin


class Main(Command):
    name = "speleo"

    description = "Get path to any dependency package directory in your poetry venv"

    arguments = [argument(name="package_name", description="The name of the package")]

    def handle(self) -> int:
        from poetry.utils.env import EnvManager

        package_name = self.argument("package_name")

        env = EnvManager(self.poetry).get()
        if not env.is_venv():
            return 1

        package_path = env.site_packages.path.joinpath(package_name)
        if not package_path.exists():
            raise RuntimeError(f"No package `{package_name}` found at {package_path}")

        self.info(str(package_path))

        return 0


class Speleo(ApplicationPlugin):
    @property
    def commands(self) -> list[type[Command]]:
        return [Main]
