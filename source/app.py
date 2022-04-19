from database import extract_data_qp, extract_data_rb
import qdarkstyle
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5 import QtWidgets,QtCore,QtGui, uic
import sys
import numpy as np
from Rabi  import process_rabi, renorm,rabifunc
from RB import fidelity_calculation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils import get_project_root
from scipy.stats import norm

thisdir = get_project_root()
qtdesignerfile = thisdir/'source'/'ui_files'/'DataAnalysisv1.ui'
Ui_MainWindow, junk = uic.loadUiType(qtdesignerfile)

class main_app(QMainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.rabi_initialize()

        #Setting up the buttons for the database
        self.ui.pBQP.clicked.connect(self.qp_connect)
        self.ui.pBCWESR.clicked.connect(self.cw_odmr_connect)
        self.ui.pBRB.clicked.connect(self.rb_connect)
        self.ui.get_data.clicked.connect(self.parse_data)
        self.ui.plot_rabi.clicked.connect(self.execute_rabi)
        self.ui.clear_plot_rabi.clicked.connect(self.clear_rabi_plot)
        self.ui.plot_rb.clicked.connect(self.execute_rb)
        self.ui.clear_plot_rb.clicked.connect(self.clear_plot_rb)
        self.ui.plot_sd.clicked.connect(self.execute_sd)
        self.ui.clear_plot_sd.clicked.connect(self.clear_plot_sd)
        self.ui.plot_sd_threshold.clicked.connect(self.set_sd_threshold)

        #Setting up rabi tab
        figrabi = Figure()
        figrabi.set_facecolor("pink")
        self.ui.mplDataPlotRabi = FigureCanvas(figrabi)
        self.ui.mplDataPlotRabi.setParent(self.ui.mplwidgetrabi)
        self.ui.mplDataPlotRabi.axes = figrabi.add_subplot(111)
        self.ui.mplDataPlotRabi.axes.grid(True)
        self.ui.mplDataPlotRabi.axes.set_title("Analyze Rabi")
        self.ui.mplDataPlotRabi.axes.set_xlabel("Time")
        self.ui.mplDataPlotRabi.axes.set_ylabel("Counts")
        self.ui.mplDataPlotRabi.axes.set_facecolor("black")
        self.ui.mplDataPlotRabi.setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), self.ui.mplwidgetrabi.size()))
        self.rabiplot = None
        self.rabi_color_counter = -1

        figrb = Figure()
        figrb.set_facecolor("pink")
        self.ui.mplDataPlotRb = FigureCanvas(figrb)
        self.ui.mplDataPlotRb.setParent(self.ui.mplwidgetrb)
        self.ui.mplDataPlotRb.axes = figrb.add_subplot(111)
        self.ui.mplDataPlotRb.axes.grid(True)
        self.ui.mplDataPlotRb.axes.set_title("Analyze RB")
        self.ui.mplDataPlotRb.axes.set_xlabel("Truncation Lengths #")
        self.ui.mplDataPlotRb.axes.set_ylabel("Fidelity %")
        self.ui.mplDataPlotRb.axes.set_facecolor("black")
        self.ui.mplDataPlotRb.setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), self.ui.mplwidgetrb.size()))
        self.rb_color_counter = -1

        figsd = Figure()
        figsd.set_facecolor("pink")
        self.ui.mplDataPlotSd = FigureCanvas(figsd)
        self.ui.mplDataPlotSd.setParent(self.ui.mplwidgetsd)
        self.ui.mplDataPlotSd.axes = figsd.add_subplot(111)
        self.ui.mplDataPlotSd.axes.set_facecolor("black")
        self.ui.mplDataPlotSd.axes.set_title("State Discrimination")
        self.ui.mplDataPlotSd.setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), self.ui.mplwidgetsd.size()))
        self.sd_color_counter = -1




        #Type of experiment youre analyzing
        self.exp = None


    #Initializing parameters
    def intialize(self):
        self.key = None
        self.date = None
        self.data_id = None
        self.sample = None
        self.count_time = None
        self.reset_time = None
        self.avg = None
        self.threshold = None
        self.aom_delay = None
        self.mw_delay = None
        self.type = None
        self.start = None
        self.stepsize = None
        self.steps = None
        self.pts = None
        self.srs = None
        self.avgcount = None
        self.sample_name = None
        self.nv_name = None
        self.waveguide = None
        self.nv_depth = None
        self.nv_counts = None


    #Setting type of experiment
    def qp_connect(self):
        self.exp = 'quantumpulse'

    def cw_odmr_connect(self):
        self.exp = 'cwodmr'

    def rb_connect(self):
        self.exp = 'rb'

    #Getting the data you inputted
    def get_data(self):

        self.intialize()

        if(self.ui.key.text() != ""):
            self.key = int(self.ui.key.text())

        if(self.ui.sample.text() != ""):
            self.sample = float(self.ui.sample.text())

        if(self.ui.count_time.text() != ""):
            self.count_time = float(self.ui.count_time.text())

        if(self.ui.reset_time.text() != ""):
            self.reset_time = float(self.ui.reset_time.text())

        if(self.ui.avg.text() != ""):
            self.avg = float(self.ui.avg.text())

        if(self.ui.threshold.text() != ""):
            self.threshold = float(self.ui.threshold.text())

        if(self.ui.aom_delay.text() != ""):
            self.aom_delay = float(self.ui.aom_delay.text())

        if(self.ui.mw_delay.text() != ""):
            self.mw_delay = float(self.ui.mw_delay.text())

        if(self.ui.start.text() != ""):
            self.start = float(self.ui.start.text())

        if(self.ui.stepsize.text() != ""):
            self.stepsize = float(self.ui.stepsize.text())

        if(self.ui.steps.text() != ""):
            self.steps = float(self.ui.steps.text())

        if(self.ui.avgcount.text() != ""):
            self.avgcount = float(self.ui.avgcount.text())

        if(self.ui.type.text() != ""):
            self.type = self.ui.type.text()

        if(self.ui.date.text() != ""):
            self.date = self.ui.date.text()

        if(self.ui.data_id.text() != ""):
            self.data_id = self.ui.data_id.text()

        if(self.ui.pts.text() != ""):
            self.pts = self.ui.pts.text()

        if(self.ui.srs.text() != ""):
            self.srs = self.ui.srs.text()

        if(self.ui.sample_name.text() != ""):
            self.sample_name = self.ui.sample_name.text()

        if(self.ui.nv_name.text() != ""):
            self.nv_name = self.ui.nv_name.text()

        if(self.ui.waveguide.text() != ""):
            self.waveguide = self.ui.waveguide.text()

        if(self.ui.nv_depth.text() != ""):
            self.nv_depth = self.ui.nv_depth.text()

        if(self.ui.nv_counts.text() != ""):
            self.nv_counts = self.ui.nv_counts.text()


    def parse_data(self):
        self.ui.info_database.clear()
        self.ui.info_database.setFontPointSize(16)
        self.get_data()

        if(self.exp == "quantumpulse"):
            data = extract_data_qp(date = self.date, data_id = self.data_id, key = self.key, sample = self.sample, count_time = self.count_time,
                                   reset_time = self.reset_time,avg = self.avg, threshold = self.threshold, aom_delay = self.aom_delay,
                                   mw_delay = self.mw_delay,Type = self.type, start = self.start, stepsize = self.stepsize, steps = self.steps,
                                   avgcount = self.avgcount,pts = self.pts,srs = self.srs, sample_name = self.sample_name, nv_name = self.nv_name,
                                   waveguide = self.waveguide, nv_depth = self.nv_depth,nv_counts = self.nv_counts)

            for i in range(len(data.key)):

                color = self.select_color(i)
                self.ui.info_database.setTextColor((QtGui.QColor(color)))

                display = "Key: %s,  Date: %s,  Data ID: %s,  Sample: %s,  Count Time: %s,  Reset Time: %s," \
                          "  Avg: %s,  Threshold: %s,  AOM Delay: %s,  MW Delay: %s,  Type: %s,  Start: %s," \
                          "  StepSize: %s,  Steps: %s  \nPTS: %s,  \nSRS: %s,  \nMetadata: \n%s" \
                          "\n\n" % (data.key[i], data.date[i],data.data_id[i],data.sample[i], data.count_time[i],
                                  data.reset_time[i], data.avg[i], data.threshold[i], data.aom_delay[i],
                                  data.mw_delay[i],data.type[i], data.start[i], data.stepsize[i],
                                  data.steps[i], data.pts[i], data.srs[i], data.metadata[i])

                self.ui.info_database.append(display)

        elif(self.exp == "rb"):
            data = extract_data_rb(date = self.date, data_id = self.data_id, key = self.key, sample = self.sample, count_time = self.count_time,
                                   reset_time = self.reset_time,avg = self.avg, threshold = self.threshold, aom_delay = self.aom_delay,
                                   mw_delay = self.mw_delay,Type = self.type, start = self.start, stepsize = self.stepsize, steps = self.steps,
                                   avgcount = self.avgcount,pts = self.pts,srs = self.srs, sample_name = self.sample_name, nv_name = self.nv_name,
                                   waveguide = self.waveguide, nv_depth = self.nv_depth,nv_counts = self.nv_counts)

            for i in range(len(data.key)):

                color = self.select_color(i)
                self.ui.info_database.setTextColor((QtGui.QColor(color)))

                display = "Key: %s,  Date: %s,  Data ID: %s,  Sample: %s,  Count Time: %s,  Reset Time: %s," \
                          "  Avg: %s,  Threshold: %s,  AOM Delay: %s,  MW Delay: %s,  Type: %s,  Start: %s," \
                          "  StepSize: %s,  Steps: %s  \nPTS: %s,  \nSRS: %s,  \nMetadata: \n%s" \
                          "\n\n" % (data.key[i], data.date[i],data.data_id[i],data.sample[i], data.count_time[i],
                                    data.reset_time[i], data.avg[i], data.threshold[i], data.aom_delay[i],
                                    data.mw_delay[i],data.type[i], data.start[i], data.stepsize[i],
                                    data.steps[i], data.pts[i], data.srs[i], data.metadata[i])

                self.ui.info_database.append(display)


        elif(self.exp == "cwodmr"):
            pass

        else:
            print("Select type of data to analyze")


    def select_color(self, i):
        colors = ["yellow","red","purple","pink","green","cyan"]
        color = colors[i%6]
        return color

    def rabi_initialize(self):
        self.ui.a1_rabi.setText("-0.1")
        self.ui.a2_rabi.setText("0.1")
        self.ui.a3_rabi.setText("25e-9")
        self.ui.a4_rabi.setText("0.0")
        self.ui.a5_rabi.setText("0.1e9")

    def get_rabi_params(self):

        a1 = float(self.ui.a1_rabi.text())
        a2 = float(self.ui.a2_rabi.text())
        a3 = float(self.ui.a3_rabi.text())
        a4 = float(self.ui.a4_rabi.text())
        a5 = float(self.ui.a5_rabi.text())

        rabiguess = [a1,a2,a3,a4,a5]

        return rabiguess

    def get_rabi_data(self):

        rabi_key = int(self.ui.key_rabi.text())
        rabi_data = extract_data_qp(key=rabi_key)


        sig_arr = np.array([float(x) for x in rabi_data.sig_data[0]])
        ref_arr = np.array([float(x) for x in rabi_data.ref_data[0]])
        num_avgs = float((rabi_data.avg[0]))
        start = float(rabi_data.start[0])
        stepsize = float(rabi_data.stepsize[0])

        return (sig_arr,ref_arr,num_avgs,start,stepsize)

    def execute_rabi(self):

        self.rabi_color_counter += 1
        data = self.get_rabi_data()

        guess = self.get_rabi_params()
        content = process_rabi(data)
        xdata,ydata,renormdat,renormerr,popt,perr,yerr = renorm(content,guess)

        theoretical_x = np.linspace(min(xdata),max(xdata),10000)
        theoretical_y = rabifunc(theoretical_x,popt[0],popt[1],popt[2],popt[3],popt[4])


        self.ui.info_rabi.setFontPointSize(14)
        color = self.select_color(self.rabi_color_counter)
        self.ui.info_rabi.setTextColor((QtGui.QColor(color)))
        self.ui.info_rabi.append("Rabi fit uncertainties are: %s"% str(list(perr)))
        self.ui.info_rabi.setTextColor((QtGui.QColor(color)))
        self.ui.info_rabi.append(("Rabi fit parameters are: %s" % str(list(popt))))


        self.plot_rabi(xdata,ydata,theoretical_x,theoretical_y,yerr)

    def plot_rabi(self,xdata,ydata,theoreticalx,theoretical_y,err):

        color = self.select_color(self.rabi_color_counter)
        self.rabiplot, = self.ui.mplDataPlotRabi.axes.plot(theoreticalx,theoretical_y,color="blue",label='theoretical')
        self.ui.mplDataPlotRabi.axes.errorbar(xdata,ydata,yerr = err,c = color,fmt="o",label = 'data')
        self.ui.mplDataPlotRabi.axes.legend()
        self.ui.mplDataPlotRabi.draw()

    def clear_rabi_plot(self):

        self.ui.info_rabi.clear()
        self.ui.mplDataPlotRabi.figure.clear()
        self.ui.mplDataPlotRabi.axes = self.ui.mplDataPlotRabi.figure.add_subplot(111)
        self.ui.mplDataPlotRabi.axes.grid(True)
        self.ui.mplDataPlotRabi.axes.set_title("Analyze Rabi")
        self.ui.mplDataPlotRabi.axes.set_xlabel("Time")
        self.ui.mplDataPlotRabi.axes.set_ylabel("Counts")
        self.ui.mplDataPlotRabi.axes.set_facecolor("black")
        self.rabiplot = None
        self.ui.mplDataPlotRabi.draw()

    def execute_rb(self):

        self.rb_color_counter += 1
        rb_key = int(self.ui.key_rb.text())
        rb_data = extract_data_rb(key=rb_key)
        threshold = float(self.ui.threshold_rb.text())
        sig_all = rb_data.sig_data[0]
        ref_all = rb_data.ref_data[0]
        Ne = int(rb_data.avg[0])
        x_all = rb_data.lengths[0]
        expected_state_all = rb_data.final_states[0]
        content = threshold,sig_all,ref_all,Ne,x_all,expected_state_all

        lengths,fidelity,c = fidelity_calculation(content)

        color = self.select_color(self.rb_color_counter)
        self.ui.info_rb.setTextColor((QtGui.QColor(color)))
        self.ui.info_rb.append("Fidelties are %s"% str(fidelity))

        self.plot_rb(np.array(lengths),np.array(fidelity)*100,c)

    def plot_rb(self,xdata,ydata,c):
        color = self.select_color(self.rb_color_counter)
        self.ui.mplDataPlotRb.axes.set_xlim(min(xdata)-1,max(xdata)+1)
        self.ui.mplDataPlotRb.axes.scatter(xdata, ydata, c = color)
        self.ui.mplDataPlotRb.axes.plot(xdata,c,color='blue', linestyle='--')
        self.ui.mplDataPlotRb.draw()

    def clear_plot_rb(self):

        self.ui.info_rb.clear()
        self.ui.mplDataPlotRb.figure.clear()
        self.ui.mplDataPlotRb.axes = self.ui.mplDataPlotRb.figure.add_subplot(111)
        self.ui.mplDataPlotRb.axes.grid(True)
        self.ui.mplDataPlotRb.axes.set_title("Analyze RB")
        self.ui.mplDataPlotRb.axes.set_xlabel("Truncation Lengths #")
        self.ui.mplDataPlotRb.axes.set_ylabel("Fidelity %")
        self.ui.mplDataPlotRb.axes.set_facecolor("black")
        self.ui.mplDataPlotRb.draw()


    def execute_sd(self):

        key0 = int(self.ui.key_sd_0.text())
        key1 = int(self.ui.key_sd_1.text())

        data0 = extract_data_qp(key=key0)
        data1 = extract_data_qp(key=key1)

        sig0 = np.array([float(x) for x in data0.sig_data[0]])
        ref0 = np.array([float(x) for x in data0.ref_data[0]])

        sig1 = np.array([float(x) for x in data1.sig_data[0]])
        ref1 = np.array([float(x) for x in data1.ref_data[0]])

        data0 = (sig0-ref0)/ref0
        data1 = (sig1-ref1)/ref1

        self.plot_sd(data0,data1)


    def plot_sd(self,data0,data1):

        n0, bins0, patches0 = self.ui.mplDataPlotSd.axes.hist(data0, bins=25, color='green', lw=0.5, edgecolor='black', density=True, label='$ |m_s = 0>$')
        n1, bins1, patches1 = self.ui.mplDataPlotSd.axes.hist(data1, bins=25, color='red', lw=0.5, edgecolor='black', density=True, label='$ |m_s = 1>$')

        mu0, sigma0 = norm.fit(data0)
        mu1, sigma1 = norm.fit(data1)
        y0 = norm.pdf(bins0, mu0, sigma0)
        y1 = norm.pdf(bins1, mu1, sigma1)


        self.ui.mplDataPlotSd.axes.plot(bins0, y0, 'b-', lw=2)
        self.ui.mplDataPlotSd.axes.plot(bins1, y1, 'b-', lw=2)

        self.ui.mplDataPlotSd.axes.legend()

        self.ui.mplDataPlotSd.draw()

    def clear_plot_sd(self):

        self.ui.info_sd.clear()
        self.ui.mplDataPlotSd.figure.clear()
        self.ui.mplDataPlotSd.axes = self.ui.mplDataPlotSd.figure.add_subplot(111)
        self.ui.mplDataPlotSd.axes.set_facecolor("black")
        self.ui.mplDataPlotSd.axes.set_title("State Discrimination")
        self.ui.mplDataPlotSd.draw()

    def set_sd_threshold(self):

        self.sd_color_counter += 1

        color = self.select_color(self.sd_color_counter)
        self.ui.info_sd.setTextColor((QtGui.QColor(color)))
        self.ui.info_sd.setFontPointSize(20)

        threshold = float(self.ui.threshold_sd.text())
        self.ui.mplDataPlotSd.axes.axvline(x=threshold, ls = ":", color=color,label='Threshold')

        self.ui.mplDataPlotSd.axes.legend()
        self.ui.info_sd.append("Threshold set to: %s" % str(threshold))

        self.ui.mplDataPlotSd.draw()
















if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(sheet)
    my_app = main_app()
    my_app.show()
    sys.exit(app.exec_())
