#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv, sys, array
import ROOT
import math


def make_plots(title, input_files, close = True):

    appearance_arr = array.array('d')
    edro_arr =  array.array('d')





    h2 = ROOT.TH2D("h2", "weighted Putin % vs turnout % (" + title + ");turnout,%;EdRo,%", 120,0, 120, 120, 0, 120)
    edro_valid = ROOT.TH2D("edro_invalid", "weighted EdRo % vs valid % (" + title + ");valid,%;EdRo,%", 80 ,90, 110, 110, 0, 110)

    total_edro = 0
    total = 0

    appearance_hist =  ROOT.TH1D("appearance_hist", "Distribution of electoral commissions by turnout (" + title + " );turnout ,%; Number of electoral commissions (0.5% bins)", 220,0, 110)
    appearance_weighted_hist =  ROOT.TH1D("appearance_weighted_hist", "Distribution of electoral commissions by turnout (weighted) (" + title + ");turnout,%;Number of electoral commissions (0.5% bins)", 220,0, 110)

    edro_votes_hist =  ROOT.TH1D("edro_votes_hist", "Distribution of electoral commissions by Putin votes (" + title + ");EdRo votes;Number of electoral commissions (--)", 10001,0, 10000)

    edro_votes_lastdigit_hist =  ROOT.TH1D("edro_votes_lastdigit_hist", "Distribution of electoral commissions by last digit of EdRo votes (" + title + ");last digit of edro votes;Number of electoral commissions (--)", 10,-0.5, 9.5)


    edro_weighted_hist =  ROOT.TH1D("edro_weighted_hist", "Distribution of electoral commissions by Putin % (weighted) (" + title + ");EdRo % ;Number of electoral commissions (0.5% bins)", 220, 0, 110)
    edro_hist =  ROOT.TH1D("edro_hist", "Distribution of electoral commissions by Putin % (raw) (" + title + ");Putin % ;Number of electoral commissions (0.5% bins)", 220, 0, 110)
    for fname in input_files:
        reader = csv.reader(open(fname))
        for row in reader:
            values = map(float, row[4:])
            if values[0]:
                appearance = (values[2] + values[3] + values[4]) / values[0] * 100.0
            else:
                appearance =  0
            if appearance:
                edro = values[22] / (values[9] + values[8])* 100.0
                total_edro+= values[22]
                total += (values[9] + values[8])

                valid = values[9] / (values[9] + values[8])* 100.0
            else:
                edro = 0.0

            h2.Fill(appearance, edro, values[0])
            edro_valid.Fill(valid, edro, values[0])

            appearance_hist.Fill(appearance)
            appearance_weighted_hist.Fill(appearance,values[0])


            if values[22] > 100:
                edro_weighted_hist.Fill(edro, values[0])
            edro_hist.Fill(edro)


            edro_votes_hist.Fill(values[22])
            edro_votes_lastdigit_hist.Fill(int(str(int(values[22]))[0]))

            appearance_arr.append(appearance)

            edro_arr.append(edro)


    #~ gr = ROOT.TGraph(len(appearance_arr), appearance_arr, edro_arr)
    #~ gr.Draw("A*")

    print total_edro, total
    print "Total edro: %2.2f%%"%(100.0 * total_edro/ total)
    c0 = ROOT.TCanvas()
    c0.cd()
    h2.Draw("COL CONT0")
    #~ raw_input()
    #~ sys.exit(0)
    h2.FitSlicesY()
    c0.SaveAs(title + "_2d.png")

    c01 = ROOT.TCanvas()
    c01.cd()

    h2_1 = ROOT.gDirectory.Get("h2_1")
    h2_1.GetXaxis().SetRangeUser(0,100)
    h2_1.GetYaxis().SetRangeUser(0,100)
    h2_1.SetTitle("Fitted Putin % mean value vs turnout (" + title + ")")
    h2_1.Draw()
    c01.SaveAs(title + "_2d_slices.png")


    #~ c1 = ROOT.TCanvas()
    #~ c1.cd()
#~
    #~ gaus_1 = ROOT.TF1("gaus_1","gaus",0, 55)
    #~ appearance_hist.Fit("gaus", "", "", 0, 54);
#~
    #~ appearance_hist.Draw()
    #~ c1.SaveAs(title + "_apearance.png")

    #~ TF1 *f1=gROOT->GetFunction("myfunc");
    #~ f1->SetParameters(800,1);


    c2 = ROOT.TCanvas()
    c2.cd()
    appearance_weighted_hist.Draw()
    c2.SaveAs(title + "_apearance_w.png")

    c3 = ROOT.TCanvas()
    c3.cd()
    edro_weighted_hist.GetXaxis().SetRangeUser(10,105)
    edro_weighted_hist.Draw()

    #~ g1 = ROOT.TF1("g1", "gaus", 0, 90)
    #~ g2 = ROOT.TF1("g2", "gaus", 0, 90)
    #~ bkg = ROOT.TF1("bkg", "gaus", 0, 90)
    #~ edro_weighted_hist.Fit("g1", "", "", 0, 30)
    #~ edro_weighted_hist.Fit("g2", "", "",  40, 90)
    #~ edro_weighted_hist.Fit("bkg", "", "",  0, 90)
    #~
    #~ total = ROOT.TF1("total", "gaus(0) + gaus(3)+gaus(6)", 0, 85)
    #~ total.SetParameters( g1.GetParameter(0),g1.GetParameter(1),g1.GetParameter(2),
                         #~ g2.GetParameter(0),g2.GetParameter(1),g2.GetParameter(2),
                         #~ bkg.GetParameter(0),bkg.GetParameter(1),bkg.GetParameter(2))
                         #~
    #~
    #~ edro_weighted_hist.Fit("total", "", "", 0,85)


    c3.SaveAs(title + "_edro_w.png")

    #~ c4 = ROOT.TCanvas()
    #~ c4.cd()
    #~ edro_hist.GetXaxis().SetRangeUser(10,105)
    #~ edro_hist.Draw()
    #~ c4.SaveAs(title + "_edro.png")

    #~ c5 = ROOT.TCanvas()
    #~ c5.cd()
    #~ edro_valid.Draw("COL CONT0")
    #~ c5.SaveAs(title + "_valid_2d.png")

    if close:
        c0.Close()
        c01.Close()
        c1.Close()
        c2.Close()
        c3.Close()
        c4.Close()
        c5.Close()
    else:
        raw_input()

if __name__ == '__main__':
    title = sys.argv[1]
    input_files = sys.argv[2:]
    make_plots(title, input_files, close = False)

