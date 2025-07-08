import inspect
from typing import Any


async def _resolve_services(self):
        """
        Resolves services defined in the view.
        
        This method looks for a dictionary of service definitions
        in the view and initializes them, allowing for both synchronous
        and asynchronous service factories.
        """

        attr_name = getattr(self, "services_attr", "services")
        service_defs = getattr(self, attr_name, None)

        if not isinstance(service_defs, dict):
            return  # nothing to resolve

        resolved = {}

        # Iterate over the service definitions and resolve each one.
        # If a service definition is callable, it will be called to get the value.
        # If the value is awaitable, it will be awaited.
        # If an exception occurs during resolution, it will raise a RuntimeError
        # with a message indicating which service failed to initialize.
        if not service_defs:
            return
        
        if not isinstance(service_defs, dict):
            raise TypeError(f"Expected 'services' to be a dictionary, got {type(service_defs).__name__}")
        
        if not all(isinstance(key, str) for key in service_defs.keys()):
            raise TypeError("All keys in 'services' must be strings")
        
        if not all(callable(factory) or isinstance(factory, (str, int, float, bool, dict, list)) for factory in service_defs.values()):
            raise TypeError("All values in 'services' must be callable or basic types (str, int, float, bool, dict, list)")
        
        for key, factory in service_defs.items():
            try:
                if callable(factory):
                    value = factory()
                else:
                    value = factory

                if inspect.isawaitable(value):
                    value = await value

                resolved[key] = value

            except Exception as e:
                raise RuntimeError(f"Failed to initialize service '{key}': {e}")

        setattr(self, attr_name, resolved)
