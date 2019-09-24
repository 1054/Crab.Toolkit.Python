#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# 
# crabspec quickPlot
# 
# usage:
#     execfile('/home/dzliu/Softwares/ipy/setup.py')
#     xarray
#     yarray
#     crabspec.quickPlot(xarray, yarray)
# 
# dependency:
#     Gnuplot
#     asciitable
#     
# 


def quickPlot(SpecDataFile, XVarColumn=1, YVarColumn=2, XErrColumn=0, YErrColumn=0, 
              SpecDataName="", XLabel="", YLabel="", XRange=[], YRange=[], XTickMajor=[], XTickMinor=[], YTickMajor=[], YTickMinor=[], XTickFormat="", YTickFormat="", 
              LineType="", LineColor="", LineWidth=2, PointType="", PointSize=2):
    
    # Use gnuplot
    
    if len(SpecDataFile)>0 and XVarColumn>0 and YVarColumn>0:
        
        gplot = Gnuplot.Gnuplot(debug=1)
        gplot('set terminal x11 font "Andika,20"')
        gplot('set grid')
        gplot('set xlabel "%s"'%(XLabel))
        gplot('set ylabel "%s"'%(YLabel))
        
        # determine TickFormat
        if len(XTickFormat)>0: 
            gplot('set format x "%s"'%(XTickFormat))
        if len(YTickFormat)>0: 
            gplot('set format y "%s"'%(YTickFormat))
        
        # determine XRange YRange
        ##if len(XRange) == 0:
        ##    XRange = [ min(XArray)-(max(XArray)-min(XArray))*0.1, max(XArray)+(max(XArray)-min(XArray))*0.15]
        ##else:
        ##    if len(XRange) != 2:
        ##        raise ValueError("XRange should be a two-element array!")
        ##if len(YRange) == 0:
        ##    YRange = [ min(YArray)-(max(YArray)-min(YArray))*0.1, max(YArray)+(max(YArray)-min(YArray))*0.15]
        ##else:
        ##    if len(YRange) != 2:
        ##        raise ValueError("YRange should be a two-element array!")
        
        ##gplot('set xrange [%s:%s]'%(XRange[0],XRange[1]))
        
        if len(XTickMajor) > 0:
            gplot('set xtics %s'%(XTickMajor))
        if len(XTickMinor) > 0:
            gplot('set mxtics %s'%(XTickMinor))
        if len(YTickMajor) > 0:
            gplot('set ytics %s'%(YTickMajor))
        if len(YTickMinor) > 0:
            gplot('set mytics %s'%(YTickMinor))
        
        # determine linetype
        WithLineType = 1
        if LineType.lower().find("solid")>=0: 
            WithLineType = 1
        if LineType.lower().find("dashed")>=0: 
            WithLineType = 2
        if LineType.lower().find("dotted")>=0: 
            WithLineType = 3
        if LineType.lower().find("dot-dash")>=0: 
            WithLineType = 4
        if LineType.lower().find("dot-dot-dash")>=0: 
            WithLineType = 5
        
        # determine linecolor
        WithLineColor = "#0060ad" # --- blue
        if len(LineColor)>1: 
            WithLineColor = LineColor
        
        # determine pointtype
        WithPointType = 4         # --- square
        if PointType.lower().find("dot")>=0: 
            WithPointType = 1
        if PointType.lower().find("star")>=0: 
            WithPointType = 3
        if PointType.lower().find("open square")>=0 or PointType.lower().find("square")>=0: 
            WithPointType = 4
        if PointType.lower().find("filled square")>=0: 
            WithPointType = 5
        
        gplot('set style line 1 lc rgb "%s" lt %d lw %s pt %d ps %s'%(WithLineColor,WithLineType,LineWidth,WithPointType,PointSize))
        
        if YErrColumn<=0:
            #### 
            #### <TODO> points -- discrete -- 
            #### use with candlesticks for financial data: date open low high close
            #### and use whisker with with candlesticks: x box_min whisker_min whisker_high box_high
            #### http://gnuplot.sourceforge.net/demo/candlesticks.html
            #### http://stackoverflow.com/questions/23270807/gnuplot-candlestick-red-and-green-fill
            #### http://www.uni-kassel.de/fb16/neuronale_netze/downloads/Gnu_Plot/Skripten/rgb_variable.html
            gplot('set xtics nomirror rotate by 90 right')
            gplot('set style boxplot candlesticks')
            gplot('set boxwidth 0.25') ### set boxwidth 0.2 absolute
            gplot('set style fill solid') ### set style fill solid noborder ### set style fill empty
            gplot('rgb(r,g,b) = 65536*int(r)+256*int(g)+int(b)')
            gplot('plot "%s" using ($0):2:5:3:4:($4>$2?rgb(255,172,172):rgb(172,255,172)):xtic(1) with candlesticks ls 1 lc rgb variable notitle'%(SpecDataFile)) ### ($0) is an index array
            #### gplot('set object 1 rect from graph 0,graph 0 to graph 0.1,graph 0.4 front') #### http://gnuplot.sourceforge.net/demo/rectangle.html
            #### gplot('plot "%s" using %d:%d:xtic(%d) title "%s" ls 1, \\'%(SpecDataFile,XVarColumn,YVarColumn,XVarColumn,SpecDataName))
            #### gplot('     ""   using %d:%d:%d with labels'%(XVarColumn,YVarColumn,XVarColumn))
            #### 
            #### <TODO> connect -- continuous
            #### gplot('plot "%s" using %d:%d title "%s" ls 1 with lines'%(SpecDataFile,XVarColumn,YVarColumn,SpecDataName))
            #### 
            #### <TODO> connect -- discrete
            #### gplot('set xtics nomirror rotate by 90 right')
            #### gplot('plot "%s" using %d:xtic(%d) title "%s" ls 1 with lines'%(SpecDataFile,YVarColumn,XVarColumn,SpecDataName))
            #### 
            #### <TODO> histogram -- continuous
            #### gplot('plot "%s" using %d:%d title "%s" ls 1 with boxes'%(SpecDataFile,XVarColumn,YVarColumn,SpecDataName))
            #### 
            #### <TODO> histogram -- continuous
            #### http://stackoverflow.com/questions/2471884/histogram-using-gnuplot
            #### gnuplot-surprising.blogspot.com/2011/09/statistic-analysis-and-histogram.html
            #### gplot('hist(x)=floor(x)+0.5')
            #### gplot('set boxwidth 0.9')
            #### gplot('plot "%s" using (hist($%d)):%d title "%s" ls 1 with boxes'%(SpecDataFile,XVarColumn,YVarColumn,SpecDataName))
            #### 
            #### <TODO> histogram -- discrete
            #### http://gnuplot.sourceforge.net/demo/histograms.html
            #### gplot('set style data histogram')
            #### gplot('set style histogram clustered gap 0')
            #### gplot('set xtics nomirror rotate by 90')
            #### gplot('plot "%s" using %d:xtic(%d) title "%s" ls 1'%(SpecDataFile,YVarColumn,XVarColumn,SpecDataName))
        else:
            gplot('set style data histogram')
            gplot('set xtics nomirror rotate by 90 right')
            gplot('set style histogram errorbars gap 0')
            gplot('plot "%s" using %d:%d:%d title "%s" with yerrorbars ls 1'%(SpecDataFile,XVarColumn,YVarColumn,YErrColumn,SpecDataName))
        
        print "crabspec.quickPlot: Plotted %s!"%(SpecDataFile)
        
        # gplot('plot "%s" using 1:2:3 title "%s-detected" with yerrorbars ls 1, '%(SledcoDat1,Source)\
        #      +'     "%s" using 1:3:(0):(-$3) title "%s-undetected" with vectors head filled ls 1, '%(SledcoDat2,Source)\
        #      +'     "%s" using ($1-0.1):3:(0.2):(0) notitle with vectors nohead filled ls 1 '%(SledcoDat2)\
        #      )
        
        return gplot



# http://www.tutorialspoint.com/python/python_database_access.htm
try:
    import Gnuplot
except ImportError: 
    print "Error! Could not import Gnuplot!"
try:
    import numpy
except ImportError: 
    print "Error! Could not import numpy!"

