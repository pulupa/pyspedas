""" Tests of spinmodel construction and interpolation """
import unittest
from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose
from pytplot import get_data, store_data, time_string, del_data, cdf_to_tplot
from pyspedas.themis import state, get_spinmodel



class SpinmodelDataValidation(unittest.TestCase):
    """
    Compare spin models and interpolation results generated by IDL and Python.

    The corresponding IDL script takes a time range, probe, and eclipse correction level,
    then creates a tplot variable containing the test parameters.  IDL builds a spin model by calling
    thm_load_state for the given probe and time interval, and dumps all the segment parameters to tplot
    variables.  Then a spin model interpolation routine is called for a set of timestamps, and all the
    interpolated parameters are dumped to tplot variables.   The tplot outputs are saved in a cdf file or a
    tplot save file.

    On the python side, the validation file is read to get the test parameters.  The spin models are
    created with a call to themis.state(), then the test timestamps are passed to the spinmodel interpolation
    routine.   The Python and IDL tplot variables are each given their own prefix.

    After loading the necessary data, the various tests in this file compare the Python and IDL values
    for each of the spinmodel segment parameters, and interpolation results.
    """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates data file: projects/themis/spin/spinmodel_python_test.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.themis.config import CONFIG

        # Download tplot files
        remote_server = 'https://spedas.org/'
        # remote_name = 'testfiles/thm_cotrans_validate.cdf'
        remote_name = 'testfiles/tha_validate_spinmodel.cdf'
        datafile = download(remote_file=remote_name,
                            remote_path=remote_server,
                            local_path=CONFIG['local_data_dir'],
                            no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        # Load validation variables from the test file
        del_data('*')
        filename = datafile[0]
        cdf_to_tplot(filename)
        # pytplot.tplot_restore(filename)
        t_dummy, trange = get_data('parm_trange')
        t_dummy, probe_idx = get_data('parm_probe')
        t_dummy, correction_level = get_data('parm_correction_level')
        #print(trange)
        #print(time_string(trange))
        #print(probe_idx)
        int_idx = int(probe_idx)
        probes = ['a', 'b', 'c', 'd', 'e']
        int_corr_level = int(correction_level)
        probe = probes[int_idx]
        #print(probe)
        #print(int_corr_level)
        thm_data = state(trange=trange, probe=probe, get_support_data=True)
        cls.model = get_spinmodel(probe, int_corr_level)
        cls.model.make_tplot_vars('py_seg_')
        #pytplot.tplot_names()
        dummy_t, tst_times = get_data('interp_times')
        res = cls.model.interp_t(tst_times)
        store_data('py_spinphase', data={'x': tst_times, 'y': res.spinphase})
        store_data('py_spinper', data={'x': tst_times, 'y': res.spinper})
        store_data('py_spincount', data={'x': tst_times, 'y': res.spincount})
        store_data('py_t_last', data={'x': tst_times, 'y': res.t_last})
        store_data('py_eclipse_delta_phi', data={'x': tst_times, 'y': res.eclipse_delta_phi})
        store_data('py_segflags', data={'x': tst_times, 'y': res.segflags})

    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # pytplot.del_data('*')

    def test_seg_t1(self):
        pydata = get_data('py_seg_t1')
        idldata = get_data('seg_t1')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_t2(self):
        pydata = get_data('py_seg_t2')
        idldata = get_data('seg_t2')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_c1(self):
        pydata = get_data('py_seg_c1')
        idldata = get_data('seg_c1')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_c2(self):
        pydata = get_data('py_seg_c2')
        idldata = get_data('seg_c2')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_b(self):
        pydata = get_data('py_seg_b')
        idldata = get_data('seg_b')
        assert_allclose(pydata.y, idldata.y, rtol=1.0e-05)

    def test_seg_c(self):
        pydata = get_data('py_seg_c')
        idldata = get_data('seg_c')
        assert_allclose(pydata.y, idldata.y, rtol=1.0e-06)

    def test_seg_npts(self):
        pydata = get_data('py_seg_npts')
        idldata = get_data('seg_npts')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_maxgap(self):
        pydata = get_data('py_seg_maxgap')
        idldata = get_data('seg_maxgap')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_phaserr(self):
        pydata = get_data('py_seg_phaserr')
        idldata = get_data('seg_phaserr')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_idpu_spinper(self):
        pydata = get_data('py_seg_idpu_spinper')
        idldata = get_data('seg_idpu_spinper')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_initial_delta_phi(self):
        pydata = get_data('py_seg_initial_delta_phi')
        idldata = get_data('seg_initial_delta_phi')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_seg_segflags(self):
        pydata = get_data('py_seg_segflags')
        idldata = get_data('seg_segflags')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_interp_spinphase(self):
        pydata = get_data('py_spinphase')
        idldata = get_data('interp_spinphase')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-04)

    def test_interp_spinper(self):
        pydata = get_data('py_spinper')
        idldata = get_data('interp_spinper')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_interp_spincount(self):
        pydata = get_data('py_spincount')
        idldata = get_data('interp_spincount')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_interp_segflags(self):
        pydata = get_data('py_segflags')
        idldata = get_data('interp_segflags')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_interp_eclipse_delta_phi(self):
        pydata = get_data('py_eclipse_delta_phi')
        idldata = get_data('interp_eclipse_delta_phi')
        assert_allclose(pydata.y, idldata.y, atol=1.0e-06)

    def test_timerange(self):
        trange=self.model.get_timerange()
        print(time_string(trange[0]),time_string(trange[1]))

    def test_eclipse_times(self):
        start_times,end_times=self.model.get_eclipse_times()
        for i in range(len(start_times)):
            print(time_string(start_times[i]),time_string(end_times[i]))

if __name__ == '__main__':
    unittest.main()
