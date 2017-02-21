##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import qtip_graph as graph
import get_indices as results
from get_results import report_concat
from get_results import generate_result


def dump_result(Stor, directory, testcase):
    try:
        lower_s = testcase.lower()
        Stor.append(Paragraph(testcase, Style['h3']))
        l1 = report_concat(directory, lower_s)
        l = 1
        for a in l1:
            Stor.append(Paragraph(testcase + " result_" + str(l), Style['h5']))
            raw_string = generate_result(a, 0)
            replaced_string = raw_string.replace('\n', '<br/> ').replace(' ', '&nbsp;')
            Stor.append(Paragraph(replaced_string, Style['BodyText']))
            l = l + 1
    except OSError:
        print "Results for {0} not found".format(testcase)


doc = SimpleDocTemplate("../../results/QTIP_results.pdf", pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)
Stor = []
Style = getSampleStyleSheet()
Title = "QTIP Benchmark Suite"
Stor.append(Paragraph(Title, Style['Title']))
H1 = "Results"
Stor.append(Spacer(0, 36))
Stor.append(Paragraph(H1, Style['h2']))
compute = 0
storage = 0
network = 0
try:
    compute = results.get_index('compute_result')
except IOError:
    pass

try:
    storage = results.get_index('storage_result')
except IOError:
    pass
try:
    network = results.get_index('network_result')
except IOError:
    pass

Stor.append(Paragraph("Compute Suite:   %f" % compute, Style['h5']))
Stor.append(Paragraph("Storage Suite:   %f" % storage, Style['h5']))
Stor.append(Paragraph("Network Suite:   %f" % network, Style['h5']))
graph.plot_indices(compute, storage, network)
qtip_graph = ('qtip_graph.jpeg')
im = Image(qtip_graph, 5 * inch, 4 * inch)
Stor.append(im)
Stor.append(Spacer(0, 12))
Stor.append(Paragraph("Reference POD", Style['h5']))
ptext = "The Dell OPNFV Lab POD3  has been taken as the reference POD against which the reference results have been collected. The POD consists of 6 identical servers. The details of such a server are:"
Stor.append(Paragraph(ptext, Style['Normal']))
ptext = "<bullet>&bull;</bullet>Server Type: Dell PowerEdge R630 Server"
Stor.append(Paragraph(ptext, Style['Bullet']))
ptext = "<bullet>&bull;</bullet>CPU: Intel  Xeon E5-2698 @ 2300 MHz"
Stor.append(Paragraph(ptext, Style["Bullet"]))
ptext = "<bullet>&bull;</bullet>RAM: 128GB"
Stor.append(Paragraph(ptext, Style["Bullet"]))
ptext = "<bullet>&bull;</bullet>Storage SSD: 420GB"
Stor.append(Paragraph(ptext, Style["Bullet"]))
ptext = "<bullet>&bull;</bullet>Network Card: Intel 2P X520/2P I350 rNDC"
Stor.append(Paragraph(ptext, Style["Bullet"]))
ptext = "Servers interconnected through a DELL S4810 switch using a 10Gbps physical link"
Stor.append(Paragraph(ptext, Style["Bullet"]))
Stor.append(Spacer(0, 12))
ptext = "For Further  Details of the Reference POD hardware, please visit: https://wiki.opnfv.org/reference_pod_hardware_details"
Stor.append(Paragraph(ptext, Style['Normal']))
Stor.append(Spacer(0, 12))
ptext = "For Details of the Reference POD Results,  please visit: https://wiki.opnfv.org/reference_pod_qtip_results"
Stor.append(Spacer(0, 12))
Stor.append(Paragraph(ptext, Style['Normal']))
Stor.append(Paragraph("RAW Results", Style['h1']))
Stor.append(Paragraph("Compute Results", Style['h2']))

dump_result(Stor, "../../results/dhrystone/", "Dhrystone_bm")
dump_result(Stor, "../../results/dhrystone/", "Dhrystone_vm")

dump_result(Stor, "../../results/whetstone/", "Whetstone_bm")
dump_result(Stor, "../../results/whetstone/", "Whetstone_vm")

dump_result(Stor, "../../results/ramspeed/", "Ramspeed_bm")
dump_result(Stor, "../../results/ramspeed/", "Ramspeed_vm")

dump_result(Stor, "../../results/ssl/", "SSL_bm")
dump_result(Stor, "../../results/ssl/", "SSL_vm")

Stor.append(Paragraph("Network Results", Style['h2']))
dump_result(Stor, "../../results/iperf/", "IPERF_bm")
dump_result(Stor, "../../results/iperf/", "IPERF_vm")
dump_result(Stor, "../../results/iperf/", "IPERF_vm_2")

Stor.append(Paragraph("Storage Results", Style['h2']))
dump_result(Stor, "../../results/fio/", "fio_bm")
dump_result(Stor, "../../results/fio/", "fio_vm")


doc.build(Stor)
