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

class osmocom_hackrf_hybrid(gr.basic_block):
    """
    docstring for block osmocom_hackrf_hybrid
    """
    def __init__(self, sample_rate, center_freq, freq_corr, dc_offset_mode, iq_balance_mode, gain_mode, rf_gain, if_gain, bb_gain, default_mode):
        gr.basic_block.__init__(self,
            name="osmocom_hackrf_hybrid",
            in_sig=[numpy.complex64],
            out_sig=[numpy.complex64])

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

