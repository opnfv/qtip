from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import qtip_graph  as graph
import get_indices as results 
doc = SimpleDocTemplate("../../results/QTIP_results.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)

Stor=[]
Style=getSampleStyleSheet()
Title="QTIP Benchmark Suite"
Stor.append(Paragraph(Title,Style['Title']))
H1="Results"
Stor.append(Spacer(0,36))
Stor.append(Paragraph(H1, Style['h2']))
compute=0
storage=0
network=0
try:
    compute=results.get_index('compute_result')
except IOError:
    pass

try:
    storage=results.get_index('storage_result')
except IOError:
    pass
try:
    network=results.get_index('network_result')
except IOError:
    pass

Stor.append(Paragraph("Compute Suite:   %f" %compute, Style['h5']))
Stor.append(Paragraph("Storage Suite:   %f" %storage, Style['h5'])) 
Stor.append(Paragraph("Netowrk Suite:   %f" %network, Style['h5']))
graph.plot_indices(compute,storage,network)
qtip_graph=('qtip_graph.jpeg')
im=Image(qtip_graph, 5*inch,4*inch)
Stor.append(im)
Stor.append(Spacer(0, 12))
ptext="For Details of the Reference POD hardware, please visit: https://wiki.opnfv.org/reference_pod_hardware_details"
Stor.append(Paragraph(ptext,Style['Normal']))
Stor.append(Spacer(0, 12))
ptext="For Details of the Reference POD Results, please visit: https://wiki.opnfv.org/reference_pod_qtip_results"
Stor.append(Paragraph(ptext,Style['Normal']))
doc.build(Stor)
