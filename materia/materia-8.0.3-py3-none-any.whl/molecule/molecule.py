from __future__ import annotations
from typing import Any

import materia as mtr
import pickle
import rdkit, rdkit.Chem

__all__ = ["Molecule"]


def first(flist, default=None):
    """ Try each function in `flist` until one does not throw an exception, and
    return the return value of that function. If all functions throw exceptions,
    return `default` 

    Args: 
        flist - list of functions to try
        default - value to return if all functions fail

    Returns:
        return value of first function that does not throw exception, or
        `default` if all throw exceptions.

    TODO: Also accept a list of (f, (exceptions)) tuples, where f is the
    function as above and (exceptions) is a tuple of exceptions that f should
    expect. This allows you to still re-raise unexpected exceptions.
    """
    # from https://stackoverflow.com/a/13874877

    for f in flist:
        try:
            return f()
        except:
            continue
    else:
        return default


class Molecule:
    def __init__(self, structure) -> None:
        super().__setattr__("properties", {})
        if isinstance(structure, mtr.Structure):
            self.structure = structure
        elif isinstance(structure, str):
            self.structure = first(
                [
                    lambda: mtr.Structure.read(structure),
                    lambda: mtr.Structure.generate(smiles=structure),
                    lambda: mtr.Structure.retrieve(name=structure),
                ]
            )

        self.charge = rdkit.Chem.GetFormalCharge(self.structure.to_rdkit())
        self.multiplicity = (sum(self.structure.atomic_numbers) + self.charge) % 2 + 1

    def _from_file(self, structure):
        try:
            return mtr.Structure.read
        except:
            return False

    def save(self, filepath: str) -> None:
        """
        Pickle molecule to a given save file.

        Args:
            filepath: Path to file in which the molecule will be pickled. Can be an absolute or a relative path.
        """
        with open(mtr.expand(filepath), "wb") as f:
            pickle.dump(obj=self, file=f)

    @staticmethod
    def load(filepath: str) -> Molecule:
        """
        Load molecule from a pickle file.

        Args:
            filepath: Path to pickle file from which the molecule will be loaded. Can be an absolute or a relative path.

        Returns:
            Molecule retrieved from pickle file.

        """
        with open(mtr.expand(filepath), "rb") as f:
            mol = pickle.load(file=f)

        return mol

    def __getattr__(self, name: str) -> Any:
        if name == "properties":
            return self.properties
        try:
            return self.properties[name]
        except KeyError:
            return getattr(self.structure, name)

    def __setattr__(self, name: str, value) -> None:
        self.properties[name] = value

    # @property
    # def mass(self) -> mtr.Qty:
    #     value = sum(self.atomic_masses.value)
    #     unit = self.atomic_masses.unit

    #     return value * unit

    # # STRUCTURE
    #
    # @property
    # def structure(self):
    #     return self.properties['structure']
    #
    # @structure.setter
    # def structure(self, value):
    #     self.properties['structure'] = value
    #
    # # GEOMETRY
    #
    # @property
    # def volume(self):
    #     return self.properties['volume']
    #
    # @volume.setter
    # def volume(self, value):
    #     self.properties['volume'] = mtr.Volume(volume=value)
    #
    # @property
    # def energy(self):
    #     return self.properties['energy']
    #
    # @energy.setter
    # def energy(self, value):
    #     # FIXME: should this be the raw value or a mtr wrapper?
    #     self.properties['energy'] = value
    #
    # # EXCITATION ENERGIES
    #
    # @property
    # def excitation_energies(self):
    #     return self.properties['excitation_energies']
    #
    # @excitation_energies.setter
    # def excitation_energies(self, value):
    #     self.properties['excitation_energies'] = value
    #     #excitation_energies,oscillator_strengths = value
    #     #self.properties['excitation_energies'] = mtr.ExcitationEnergies(excitation_energies=excitation_energies,oscillator_strengths=oscillator_strengths)
    #
    # # DIPOLE MOMENT
    #
    # @property
    # def dipole(self):
    #     return self.properties['dipole']
    #
    # @dipole.setter
    # def dipole(self, value):
    #     self.properties['dipole'] = mtr.Dipole(dipole_moment=value)
    #
    # # TIME-DEPENDENT DIPOLE MOMENT
    #
    # @property
    # def tddipole_x(self):
    #     return self.properties['tddipole_x']
    #
    # @tddipole_x.setter
    # def tddipole_x(self, value):
    #     self.properties['tddipole_x'] = mtr.TDDipole(time=value['time'],tddipole=value['tddipole'])
    #
    # @property
    # def tddipole_y(self):
    #     return self.properties['tddipole_y']
    #
    # @tddipole_y.setter
    # def tddipole_y(self, value):
    #     self.properties['tddipole_y'] = mtr.TDDipole(time=value['time'],tddipole=value['tddipole'])
    #
    # @property
    # def tddipole_z(self):
    #     return self.properties['tddipole_z']
    #
    # @tddipole_z.setter
    # def tddipole_z(self, value):
    #     self.properties['tddipole_z'] = mtr.TDDipole(time=value['time'],tddipole=value['tddipole'])
    #
    # # POLARIZABILITY
    #
    # @property
    # def polarizability(self):
    #     return self.properties['polarizability']
    #
    # @polarizability.setter
    # def polarizability(self, value):
    #     self.properties['polarizability'] = value#mtr.Polarizability(polarizability_tensor=value)
    #
    # # TIME-DEPENDENT POLARIZABILITY
    #
    # @property
    # def td_polarizability_xx(self):
    #     return self.properties['td_polarizability_xx']
    #
    # @td_polarizability_xx.setter
    # def td_polarizability_xx(self, value):
    #     self.properties['td_polarizability_xx'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def td_polarizability_xy(self):
    #     return self.properties['td_polarizability_xy']
    #
    # @td_polarizability_xy.setter
    # def td_polarizability_xy(self, value):
    #     self.properties['td_polarizability_xy'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def td_polarizability_xz(self):
    #     return self.properties['td_polarizability_xz']
    #
    # @td_polarizability_xz.setter
    # def td_polarizability_xz(self, value):
    #     self.properties['td_polarizability_xz'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def td_polarizability_yx(self):
    #     return self.properties['td_polarizability_yx']
    #
    # @td_polarizability_yx.setter
    # def td_polarizability_yx(self, value):
    #     self.properties['td_polarizability_yx'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def td_polarizability_yy(self):
    #     return self.properties['td_polarizability_yy']
    #
    # @td_polarizability_yy.setter
    # def td_polarizability_yy(self, value):
    #     self.properties['td_polarizability_yy'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def td_polarizability_yz(self):
    #     return self.properties['td_polarizability_yz']
    #
    # @td_polarizability_yz.setter
    # def td_polarizability_yz(self, value):
    #     self.properties['td_polarizability_yz'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def td_polarizability_zx(self):
    #     return self.properties['td_polarizability_zx']
    #
    # @td_polarizability_zx.setter
    # def td_polarizability_zx(self, value):
    #     self.properties['td_polarizability_zx'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def td_polarizability_zy(self):
    #     return self.properties['td_polarizability_zy']
    #
    # @td_polarizability_zy.setter
    # def td_polarizability_zy(self, value):
    #     self.properties['td_polarizability_zy'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def td_polarizability_zz(self):
    #     return self.properties['td_polarizability_zz']
    #
    # @td_polarizability_zz.setter
    # def td_polarizability_zz(self, value):
    #     self.properties['td_polarizability_zz'] = mtr.TDPolarizability(time=value['time'],td_polarizability=value['td_polarizability'])
    #
    # @property
    # def permittivity(self):
    #     if 'volume' not in self.properties:
    #         raise AttributeError('Volume not present in self.properties. Try computing volume first.')
    #     if 'polarizability' not in self.properties:
    #         raise AttributeError('Polarizability not present in self.properties. Try computing polarizability first.')
    #
    #     volume = self.volume
    #     volume.convert(new_unit=mtr.au_volume)
    #
    #     polarizability = self.polarizability
    #     polarizability.convert(new_unit=mtr.au_volume)
    #
    #     # this is an approximation!
    #     number_density = 1/volume
    #
    #     return self._clausius_mossotti(number_density=number_density,polarizability=polarizability)
    #
    # def _clausius_mossotti(self, number_density, polarizability):
    #     # polarizability should be given as polarizability volume (computed in CGS) in cubic bohr
    #     X = 4*scipy.constants.pi*number_density*polarizability/3
    #
    #     return (mtr.Qty(value=1,unit=mtr.unitless) + 2*X)/(mtr.Qty(value=1,unit=mtr.unitless) - X)
    #
    # # FIXME: should add an option/method for LRTDDFT later
    # @property
    # def absorption_spectrum(self, **kwargs):
    #     if 'dynamic_dipole_moment' not in self.properties:
    #         raise AttributeError('Dynamic dipole moment not present in self.properties. Try computing dynamic dipole moment first.')
    #
    #     _,mu_x_fft_imag = self.tddipole_x.fourier_transform()
    #     mu_x_fft_imag /= self.tddipole_x.applied_field
    #     mu_x_fft_real,mu_x_fft_imag = mu_x.fourier_transform()
    #     mu_x_fft_imag.y /= self.properties['dynamic_dipole_moment']['rttddftmodule0']['kickx']['E_max']
    #     #mu_y_fft = mu_y.fourier_transform()
    #     #mu_y_fft.y /= self.properties['dynamic_dipole_moment']['E_max']
    #     #mu_z_fft = mu_z.fourier_transform()
    #     #mu_z_fft.y /= self.properties['dynamic_dipole_moment']['E_max']
    #
    #     #trace = dataseries.Spectrum(x=mu_x.x,y=(mu_x.y+mu_y.y+mu_z.z)/3)
    #
    #     #print(trace.x.unit,trace.y.unit)
    #
    #     #from signalanalyzer import SignalAnalyzer
    #
    #     #sa = SignalAnalyzer(time=dynamic_dipole_moment.x,signal=dynamic_dipole_moment.y,**kwargs)
    #
    #     #return sa.analyze_signal()
