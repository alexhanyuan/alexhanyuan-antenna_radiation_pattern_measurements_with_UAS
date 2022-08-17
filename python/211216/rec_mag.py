#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time

class rx_test_python(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Variables
        ##################################################
        self.wav_scaling = wav_scaling = 0.03
        self.samp_rate = samp_rate = 1000000
        self.num_samps = num_samps = 10000
        self.frequency = frequency = 447100000
        self.averages = averages = 10

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_gain(30, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('/home/alex/Desktop/hackrf_grc/211216/rx_test.wav', 1, samp_rate, 16)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(averages, wav_scaling, 4000, 1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, num_samps)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_head_0, 0))

    def get_wav_scaling(self):
        return self.wav_scaling

    def set_wav_scaling(self, wav_scaling):
        self.wav_scaling = wav_scaling
        self.blocks_moving_average_xx_0.set_length_and_scale(self.averages, self.wav_scaling)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_num_samps(self):
        return self.num_samps

    def set_num_samps(self, num_samps):
        self.num_samps = num_samps
        self.blocks_head_0.set_length(self.num_samps)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.osmosdr_source_0.set_center_freq(self.frequency, 0)

    def get_averages(self):
        return self.averages

    def set_averages(self, averages):
        self.averages = averages
        self.blocks_moving_average_xx_0.set_length_and_scale(self.averages, self.wav_scaling)



def main(top_block_cls=rx_test_python, options=None):
    top_block_cls=rx_test_python
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
