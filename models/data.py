import numpy as np


class SpectralAnalyzeResult:

    def __init__(self, fft_result: np.array, fft_freq: np.array, fft_magnitude: np.array):
        self.__fft_result = fft_result
        self.__fft_freq = fft_freq
        self.__fft_magnitude = fft_magnitude

    @property
    def fft_result(self) -> np.array:
        return self.__fft_result

    @property
    def fft_freq(self) -> np.array:
        return self.__fft_freq

    @property
    def fft_magnitude(self) -> np.array:
        return self.__fft_magnitude


class SignalData:

    def __init__(self, x_data: np.array, y_data: np.array, x_label: np.array, y_label: np.array):
        self.__x_data = x_data
        self.__y_data = y_data
        self.__x_label = x_label
        self.__y_label = y_label
        self.__spectral_analyze_result = self.__spectral_analyze()

    @property
    def x_data(self) -> np.array:
        return self.__x_data

    @property
    def y_data(self) -> np.array:
        return self.__y_data

    @property
    def x_label(self) -> np.array:
        return self.__x_label

    @property
    def y_label(self) -> np.array:
        return self.__y_label

    @property
    def spectral_analyze_result(self) -> SpectralAnalyzeResult:
        return self.__spectral_analyze_result

    def calculate_stats(self) -> dict[str, float]:
        signal_array = np.array(self.__y_data)
        return {
            'Mean': np.mean(signal_array),
            'Median': np.median(signal_array),
            'Std Dev': np.std(signal_array),
            'Min': np.min(signal_array),
            'Max': np.max(signal_array),
            'Range': np.max(signal_array) - np.min(signal_array),
            'RMS': np.sqrt(np.mean(np.square(signal_array))),
            'Peak to Peak': np.max(signal_array) - np.min(signal_array)
        }

    def __spectral_analyze(self) -> SpectralAnalyzeResult:
        fft_result = np.fft.rfft(self.__y_data)
        fft_freq = np.fft.rfftfreq(len(self.__y_data), d=np.mean(np.diff(self.__x_data)))
        fft_magnitude = np.abs(fft_result)
        return SpectralAnalyzeResult(fft_result, fft_freq, fft_magnitude)


class LoadedSignalData(SignalData):

    def __init__(self, x_data: np.array, y_data: np.array, x_label: np.array, y_label: np.array, filename: str,
                 shape: np.array, columns: np.array):
        super().__init__(x_data=x_data, y_data=y_data, x_label=x_label, y_label=y_label)
        self.__filename = filename
        self.__shape = shape
        self.__columns = columns

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def shape(self) -> tuple[int, int]:
        return self.__shape

    @property
    def columns(self) -> np.array:
        return self.__columns


class FilteredSignalData(SignalData):

    def __init__(self, x_data: np.array, y_data: np.array, x_label: np.array, y_label: np.array, filter_type: str,
                 cutoff_freq: float, cutoff_freq_range: float, filter_order: int):
        super().__init__(x_data=x_data, y_data=y_data, x_label=x_label, y_label=y_label)
        self.__filter_type = filter_type
        self.__cutoff_freq = cutoff_freq
        self.__cutoff_freq_range = cutoff_freq_range
        self.__filter_order = filter_order

    @property
    def filter_type(self):
        return self.__filter_type

    @property
    def cutoff_freq(self):
        return self.__cutoff_freq

    @property
    def cutoff_freq_range(self):
        return self.__cutoff_freq_range

    @property
    def filter_order(self):
        return self.__filter_order
