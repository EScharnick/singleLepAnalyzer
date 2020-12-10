import os,sys
execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")

dirlist = [ 
'BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8',
'BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8',
'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8',
]

from ROOT import TFile, TH1

year = '2018'
if year == '2018':
    dirlist.append('BprimeBprime_M-900_TuneCP5_PSweights_13TeV-madgraph-pythia8')
    dirlist.append('TprimeTprime_M-900_TuneCP5_PSweights_13TeV-madgraph-pythia8')

for sample in dirlist:
    if year == '2018': sample = sample.replace('CP5_13TeV','CP5_PSweights_13TeV')
    print('---------------------'+sample+'--------------------------')
    runlist = EOSlistdir('/store/user/lpcljm/FWLJMET102X_MuRF'+year+'_Sep2020/'+sample+'/singleLep'+year+'/')
    if len(runlist) > 1: 
        print('PROBLEM: more than 1 crab directory, SKIPPING')
        continue
    integral = 0.0
    newpdf = 0.0
    if sample == 'BprimeBprime_M-1000_TuneCP5_PSweights_13TeV-madgraph-pythia8' and year == '2018':
	for i in range(1,14):		# loop to deal with BB1000 getting split into 13 files in 2018
	    rfile = TFile.Open('root://cmseos.fnal.gov//store/user/lpcljm/FWLJMET102X_MuRF'+year+'_Sep2020/'+sample+'/singleLep'+year+'/'+str(runlist[0])+'/0000/'+sample+'_'+str(i)+'.root')
	    hist = rfile.Get("mcweightanalyzer/weightHist")
	    integral = integral + hist.GetBinContent(5) + hist.GetBinContent(7)
	    newpdf = newpdf + hist.GetBinContent(3)
    else:
	rfile = TFile.Open('root://cmseos.fnal.gov//store/user/lpcljm/FWLJMET102X_MuRF'+year+'_Sep2020/'+sample+'/singleLep'+year+'/'+str(runlist[0])+'/0000/'+sample+'_1.root')
	hist = rfile.Get("mcweightanalyzer/weightHist")
	integral = hist.GetBinContent(5) + hist.GetBinContent(7)
	newpdf = hist.GetBinContent(3)

    print(str(round(newpdf,3))+'. # from integral '+str(integral))

    muhist = rfile.Get("mcweightanalyzer/muRFcounts")
    #print('MuRF nominal yield = '+str(round(muhist.GetBinContent(1),3)))

    muvars = []
    for ibin in range(1,muhist.GetNbinsX()+1): muvars.append(muhist.GetBinContent(ibin))
    muvars.sort()
    
    print('MuRF up yield = '+str(round(muvars[6],3)))
    print('MuRF dn yield = '+str(round(muvars[0],3)))
    
    pdfhist = rfile.Get("mcweightanalyzer/pdf4LHCcounts")
    #print('PDF nominal yield = '+str(round(pdfhist.GetBinContent(1),3)))

    pdfvars = []
    for ibin in range(1,pdfhist.GetNbinsX()+1): pdfvars.append(pdfhist.GetBinContent(ibin))
    pdfnominal = pdfvars[0]
    pdfvars.sort()

    errsqr = 0
    for ibin in range(1,pdfhist.GetNbinsX()+1): errsqr = errsqr + (pdfvars[ibin-1]-pdfnominal)*(pdfvars[ibin-1]-pdfnominal)
    err = pow(errsqr,0.5)

    print('error/pdfnominal = '+str(round(err/pdfnominal,3)))
    print('pdfnominal/error = '+str(round(pdfnominal/err,3)))
    print('(pdfnominal + error)/pdfnominal = '+str(round((pdfnominal + err)/pdfnominal,3)))
    print('pdfnominal/(pdfnominal + error) = '+str(round(pdfnominal/(pdfnominal + err),3)))
    print('(pdfnominal - error)/pdfnominal = '+str(round((pdfnominal - err)/pdfnominal,3)))
    print('pdfnominal/(pdfnominal - error) = '+str(round(pdfnominal/(pdfnominal - err),3)))

    print('MUup scale factor = '+str(round(muhist.GetBinContent(1)/muvars[6],3)))
    print('MUdn scale factor = '+str(round(muhist.GetBinContent(1)/muvars[0],3)))





