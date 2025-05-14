import unittest

import numpy as np

from models.data import SpectralAnalyzeResult, SignalData, LoadedSignalData, FilteredSignalData


class TestSpectralAnalyzeResult(unittest.TestCase):

    def setUp(self):
        self.fft_result = np.array([1 + 2j, 3 + 4j, 5 + 6j])
        self.fft_freq = np.array([0.1, 0.2, 0.3])
        self.fft_magnitude = np.array([2.23606798, 5, 7.81024968])
        self.result = SpectralAnalyzeResult(self.fft_result, self.fft_freq, self.fft_magnitude)

    def test_properties(self):
        # Given
        # When
        # Then
        np.testing.assert_array_equal(self.result.fft_result, self.fft_result)
        np.testing.assert_array_equal(self.result.fft_freq, self.fft_freq)
        np.testing.assert_array_equal(self.result.fft_magnitude, self.fft_magnitude)


class TestSignalData(unittest.TestCase):

    def setUp(self):
        self.x_data = np.linspace(0, 1, 100)
        self.y_data = np.sin(2 * np.pi * 10 * self.x_data)
        self.x_label = "Time (s)"
        self.y_label = "Amplitude"
        self.signal = SignalData(self.x_data, self.y_data, self.x_label, self.y_label)

    def test_properties(self):
        # Given
        # When
        # Then
        np.testing.assert_array_equal(self.signal.x_data, self.x_data)
        np.testing.assert_array_equal(self.signal.y_data, self.y_data)

        self.assertEqual(self.signal.x_label, self.x_label)
        self.assertEqual(self.signal.y_label, self.y_label)
        self.assertIsInstance(self.signal.spectral_analyze_result, SpectralAnalyzeResult)

    def test_calculate_stats(self):
        # Given
        # When
        stats = self.signal.calculate_stats()

        # Then
        expected_keys = ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Range', 'RMS', 'Peak to Peak']
        for key in expected_keys:
            self.assertIn(key, stats)

        self.assertAlmostEqual(stats['Mean'], np.mean(self.y_data), places=6)
        self.assertAlmostEqual(stats['Median'], np.median(self.y_data), places=6)
        self.assertAlmostEqual(stats['Std Dev'], np.std(self.y_data), places=6)
        self.assertAlmostEqual(stats['Min'], np.min(self.y_data), places=6)
        self.assertAlmostEqual(stats['Max'], np.max(self.y_data), places=6)
        self.assertAlmostEqual(stats['Range'], np.max(self.y_data) - np.min(self.y_data), places=6)
        self.assertAlmostEqual(stats['RMS'], np.sqrt(np.mean(np.square(self.y_data))), places=6)
        self.assertAlmostEqual(stats['Peak to Peak'], np.max(self.y_data) - np.min(self.y_data), places=6)

    def test_spectral_analyze(self):
        # Given
        # When
        result = self.signal.spectral_analyze_result

        # Then
        expected_freq = np.fft.rfftfreq(len(self.y_data), d=np.mean(np.diff(self.x_data)))
        np.testing.assert_array_almost_equal(result.fft_freq, expected_freq)

        expected_fft = np.fft.rfft(self.y_data)
        np.testing.assert_array_almost_equal(result.fft_result, expected_fft)

        expected_magnitude = np.abs(expected_fft)
        np.testing.assert_array_almost_equal(result.fft_magnitude, expected_magnitude)


class TestLoadedSignalData(unittest.TestCase):

    def setUp(self):
        self.x_data = np.linspace(0, 1, 100)
        self.y_data = np.sin(2 * np.pi * 10 * self.x_data)
        self.x_label = "Time (s)"
        self.y_label = "Amplitude"
        self.filename = "test_signal.csv"
        self.shape = (100, 2)
        self.columns = np.array(["Time", "Amplitude"])

        self.loaded_signal = LoadedSignalData(
            self.x_data, self.y_data, self.x_label, self.y_label,
            self.filename, self.shape, self.columns
        )

    def test_properties(self):
        # Given
        # When
        # Then
        np.testing.assert_array_equal(self.loaded_signal.x_data, self.x_data)
        np.testing.assert_array_equal(self.loaded_signal.y_data, self.y_data)
        np.testing.assert_array_equal(self.loaded_signal.columns, self.columns)

        self.assertEqual(self.loaded_signal.x_label, self.x_label)
        self.assertEqual(self.loaded_signal.y_label, self.y_label)
        self.assertEqual(self.loaded_signal.filename, self.filename)
        self.assertEqual(self.loaded_signal.shape, self.shape)

        self.assertIsInstance(self.loaded_signal, SignalData)


class TestFilteredSignalData(unittest.TestCase):

    def setUp(self):
        self.x_data = np.linspace(0, 1, 100)
        self.y_data = np.sin(2 * np.pi * 10 * self.x_data)
        self.x_label = "Time (s)"
        self.y_label = "Amplitude"
        self.filter_type = "lowpass"
        self.cutoff_freq = 20.0
        self.cutoff_freq_range = 5.0
        self.filter_order = 4

        self.filtered_signal = FilteredSignalData(
            self.x_data, self.y_data, self.x_label, self.y_label,
            self.filter_type, self.cutoff_freq, self.cutoff_freq_range, self.filter_order
        )

    def test_properties(self):
        # Given
        # When
        # Then
        np.testing.assert_array_equal(self.filtered_signal.x_data, self.x_data)
        np.testing.assert_array_equal(self.filtered_signal.y_data, self.y_data)

        self.assertEqual(self.filtered_signal.x_label, self.x_label)
        self.assertEqual(self.filtered_signal.y_label, self.y_label)
        self.assertEqual(self.filtered_signal.filter_type, self.filter_type)
        self.assertEqual(self.filtered_signal.cutoff_freq, self.cutoff_freq)
        self.assertEqual(self.filtered_signal.filter_order, self.filter_order)

        self.assertIsInstance(self.filtered_signal, SignalData)


if __name__ == '__main__':
    unittest.main()
