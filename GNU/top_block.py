#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Lab1
# Generated: Tue May  3 01:09:32 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Lab1")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.frequ = frequ = 525.2e6
        self.threshold = threshold = -60
        self.samp_rate = samp_rate = 2.048e6
        self.freq = freq = frequ
        self.fft_size = fft_size = 1024

        ##################################################
        # Blocks
        ##################################################
        _threshold_sizer = wx.BoxSizer(wx.VERTICAL)
        self._threshold_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_threshold_sizer,
        	value=self.threshold,
        	callback=self.set_threshold,
        	label="Threshold",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._threshold_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_threshold_sizer,
        	value=self.threshold,
        	callback=self.set_threshold,
        	minimum=-100,
        	maximum=0,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_threshold_sizer)
        self.notebook = self.notebook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook.AddPage(grc_wxgui.Panel(self.notebook), "Spectrum")
        self.notebook.AddPage(grc_wxgui.Panel(self.notebook), "Output")
        self.Add(self.notebook)
        self.wxgui_numbersink2_0_0 = numbersink2.number_sink_f(
        	self.notebook.GetPage(1).GetWin(),
        	unit="signal present",
        	minval=0,
        	maxval=1,
        	factor=1.0,
        	decimal_places=0,
        	ref_level=0,
        	sample_rate=samp_rate,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label="Signal Detection",
        	peak_hold=False,
        	show_gauge=True,
        )
        self.notebook.GetPage(1).Add(self.wxgui_numbersink2_0_0.win)
        self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
        	self.notebook.GetPage(1).GetWin(),
        	unit="dB",
        	minval=-120,
        	maxval=0,
        	factor=1.0,
        	decimal_places=0,
        	ref_level=0,
        	sample_rate=samp_rate,
        	number_rate=15,
        	average=True,
        	avg_alpha=30e-3,
        	label="Level",
        	peak_hold=False,
        	show_gauge=True,
        )
        self.notebook.GetPage(1).Add(self.wxgui_numbersink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.notebook.GetPage(0).GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=30e-3,
        	title="Spectrum",
        	peak_hold=False,
        	win=window.rectangular,
        )
        self.notebook.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(0, 0)
        self.rtlsdr_source_0.set_gain(30, 0)
        self.rtlsdr_source_0.set_if_gain(30, 0)
        self.rtlsdr_source_0.set_bb_gain(5, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        _frequ_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frequ_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_frequ_sizer,
        	value=self.frequ,
        	callback=self.set_frequ,
        	label="Frequency Slider",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._frequ_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_frequ_sizer,
        	value=self.frequ,
        	callback=self.set_frequ,
        	minimum=478e6,
        	maximum=862e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_frequ_sizer)
        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, (window.rectangular(1024)), True, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, 1024)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(-100, -60, threshold)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_nlog10_ff_1 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1024)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 1048580)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_nlog10_ff_1, 0))
        self.connect((self.blocks_nlog10_ff_1, 0), (self.wxgui_numbersink2_0, 0))
        self.connect((self.blocks_nlog10_ff_1, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.wxgui_numbersink2_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_fftsink2_0, 0))


# QT sink close method reimplementation

    def get_frequ(self):
        return self.frequ

    def set_frequ(self, frequ):
        self.frequ = frequ
        self.set_freq(self.frequ)
        self._frequ_slider.set_value(self.frequ)
        self._frequ_text_box.set_value(self.frequ)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self._threshold_slider.set_value(self.threshold)
        self._threshold_text_box.set_value(self.threshold)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq)
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()

