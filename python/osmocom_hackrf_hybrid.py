#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Nick Østergaard.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr





#rxtxtest imports
import time

from gnuradio import blocks
from gnuradio import analog
from gnuradio import audio

import osmosdr

import top_block_rxtx_reduced
#rxtxtest imports end

class OptionalDriverMixin(object):
    def __init__(self):
        self.driver = None
        # must be set by subclass and contain self.driver
        self.driver_connection = None
    
    def enable_driver(self):
        self.__replace_driver(self.make_driver())
    
    def disable_driver(self):
        din, dout = self.driver_connection
        if din == self.driver:
            replacement = blocks.vector_source_c([])
        elif dout == self.driver:
            replacement = blocks.null_sink(gr.sizeof_gr_complex)
        else:
            raise Exception((self.driver, din, dout))
        self.__replace_driver(replacement)
    
    def __replace_driver(self, replacement):
        self.lock()
        din, dout = self.driver_connection
        self.disconnect(din, dout)
        if din == self.driver:
            din = replacement
        elif dout == self.driver:
            dout = replacement
        else:
            raise Exception((self.driver, din, dout))
        self.connect(din, dout)
        self.driver_connection = (din, dout)
        self.driver = replacement
        self.unlock()


class Rx(gr.top_block, OptionalDriverMixin):
    def __init__(self):
        gr.top_block.__init__(self, type(self).__name__)
        OptionalDriverMixin.__init__(self)
        
        # replace this with actual demodulator
        # this just proves there is data. mind the dc offset.
        sink = audio.sink(device_name='', sampling_rate=48000)
        decim = blocks.keep_one_in_n(gr.sizeof_gr_complex, 167)
        demod = blocks.complex_to_real()
        self.connect(decim, demod, sink)
        
        self.driver = blocks.vector_source_c([])
        self.driver_connection = (self.driver, decim)
        self.connect(*self.driver_connection)
    
    def make_driver(self):
        d = osmosdr.source('hackrf=0')
        # re-set device freq, rate, gain parameters here
        return d


class Tx(gr.top_block, OptionalDriverMixin):
    def __init__(self):
        gr.top_block.__init__(self, type(self).__name__)
        OptionalDriverMixin.__init__(self)
        
        # replace this with actual modulator
        const = analog.sig_source_c(1, analog.GR_CONST_WAVE, 0, 0, 1)
        
        self.driver = blocks.null_sink(gr.sizeof_gr_complex)
        self.driver_connection = (const, self.driver)
        self.connect(*self.driver_connection)
    
    
    def make_driver(self):
        d = osmosdr.sink('hackrf=0')
        d.set_center_freq(909e6)
        # re-set device freq, rate, gain parameters here
        return d


def switch(rx, tx, select):
    if (select):
        print("Transmit mode")
        rx.disable_driver()
        tx.enable_driver()
    else:
        print("Receive mode")
        tx.disable_driver()
        rx.enable_driver()

class osmocom_hackrf_hybrid(gr.basic_block):
    """
    docstring for block osmocom_hackrf_hybrid
    """
    def __init__(self, sample_rate, center_freq, freq_corr, dc_offset_mode, iq_balance_mode, gain_mode, rf_gain, if_gain, bb_gain, default_mode):
        gr.basic_block.__init__(self,
            name="osmocom_hackrf_hybrid",
            in_sig=[numpy.complex64],
            out_sig=[numpy.complex64])
        self.t = Tx()
        self.r = Rx()
        self.t.start()
        self.r.start()
        self.default_mode = default_mode
        switch(self.r, self.t, self.default_mode)

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        #buffer references
        in0 = input_items[0]
        out = output_items[0]

        #process data
        out[:]=in0[0:len(out)]

        #consume the inputs
        self.consume(0, len(out)) #consume port 0 input
        #self.consume_each(len(out)) //or shortcut to consume on all inputs

        #return produced
        return len(out)

    def set_mode(self, mode):
        self.default_mode = mode
        switch(self.r, self.t, mode)
        print("MODE WAS SET")

    def __exit__(self, exc_type, exc_value, traceback):
        print("__exit__")
    def __del__(self):
        print("__del__")

