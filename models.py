"""Domain classes for the Farm & Crop Insights project."""

from datetime import date


class FarmEntity:
    """Base class shared by domain entities."""

    def __init__(self, name: str):
        self.name = name

    def describe(self) -> str:
        return f"{self.__class__.__name__}: {self.name}"


class FarmPlot(FarmEntity):
    """A farm plot that grows a particular crop."""

    def __init__(self, name: str, location: str, crop_type: str, area_hectares: float, plot_id=None):
        super().__init__(name)
        self.plot_id = plot_id
        self.location = location
        self.crop_type = crop_type
        self.area_hectares = float(area_hectares)

    def describe(self) -> str:
        return (
            f"Plot #{self.plot_id or 'new'}: {self.name} | {self.crop_type} | "
            f"{self.area_hectares:.2f} ha | {self.location}"
        )


class CropObservation(FarmEntity):
    """A dated measurement recorded for a plot."""

    def __init__(self, plot_id: int, observation_date: str, rainfall_mm: float, yield_kg: float,
                 note: str = "", observation_id=None):
        super().__init__(name=f"Observation for plot {plot_id}")
        # Validate date at construction time.
        date.fromisoformat(observation_date)
        self.observation_id = observation_id
        self.plot_id = int(plot_id)
        self.observation_date = observation_date
        self.rainfall_mm = float(rainfall_mm)
        self.yield_kg = float(yield_kg)
        self.note = note

    def describe(self) -> str:
        return (
            f"Observation #{self.observation_id or 'new'} | Plot {self.plot_id} | "
            f"{self.observation_date} | rain {self.rainfall_mm:g} mm | "
            f"yield {self.yield_kg:g} kg"
        )
