"""Spectral models."""
import numpy as np
from astropy import units as u
from gammapy.utils.fitting import Parameter, Parameters
from gammapy.spectrum.models import SpectralModel


class Log10Parabola(SpectralModel):
    """Gammapy log parabola model matching Sherpa parametrisation.

    The difference to the `LogParabola` in Gammapy is that here
    `log10` is used, whereas in Gammapy natural `log` is used.

    We're doing this to make the comparison / debugging easier.

    * Sherpa: http://cxc.harvard.edu/sherpa/ahelp/logparabola.html
    * Gammapy: http://docs.gammapy.org/dev/api/gammapy.spectrum.models.LogParabola.html
    """

    def __init__(
        self,
        amplitude=1e-12 * u.Unit("cm-2 s-1 TeV-1"),
        reference=10 * u.TeV,
        alpha=2,
        beta=1,
    ):
        self.parameters = Parameters(
            [
                Parameter("amplitude", amplitude),
                Parameter("reference", reference, frozen=True),
                Parameter("alpha", alpha),
                Parameter("beta", beta),
            ]
        )

    @staticmethod
    def evaluate(energy, amplitude, reference, alpha, beta):
        """Evaluate the model (static function)."""
        try:
            xx = energy / reference
            exponent = -alpha - beta * np.log10(xx)
        except AttributeError:
            from uncertainties.unumpy import log10

            xx = energy / reference
            exponent = -alpha - beta * log10(xx)

        return amplitude * np.power(xx, exponent)


class Log10ParabolaEnergyScale(SpectralModel):
    """LogParabola with modified energy scale used in the systematics fit"""

    def __init__(
        self,
        amplitude=1e-12 * u.Unit("cm-2 s-1 TeV-1"),
        reference=1 * u.TeV,
        alpha=3,
        beta=1,
        z=0.12,
    ):

        self.parameters = Parameters(
            [
                Parameter("amplitude", amplitude),
                Parameter("reference", reference, frozen=True),
                Parameter("alpha", alpha),
                Parameter("beta", beta),
                Parameter("z", z),
            ]
        )

    @staticmethod
    def evaluate(energy, amplitude, reference, alpha, beta, z):
        """Evaluate the model (static function)."""
        scale_factor = 1 / (1 + z)
        scaled_energy = energy * scale_factor
        try:
            xx = (scaled_energy / reference).to("")
            exponent = -alpha - beta * np.log10(xx)
        except AttributeError:
            from uncertainties.unumpy import log10

            xx = scaled_energy / reference
            exponent = -alpha - beta * log10(xx)
        return amplitude * np.power(xx, exponent) * scale_factor
