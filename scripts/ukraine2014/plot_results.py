#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv, sys, array
import ROOT
import math


def make_plots(title, input_files, close = True):

    turnout_arr = array.array('d')
    winner_arr =  array.array('d')



    h2 = ROOT.TH2D("h2", "weighted Poroshenko % vs turnout % (" + title + ");turnout,%;winner,%", 120,0, 120, 120, 0, 120)
    winner_valid = ROOT.TH2D("winner_invalid", "weighted winner % vs valid % (" + title + ");valid,%;winner,%", 80 ,90, 110, 110, 0, 110)

    total_winner = 0
    total = 0

    turnout_hist =  ROOT.TH1D("turnout_hist", "Distribution of electoral commissions by turnout (" + title + " );turnout ,%; Number of electoral commissions (0.5% bins)", 220,-0.25, 109.75)
    turnout_weighted_hist =  ROOT.TH1D("turnout_weighted_hist", "Distribution of electoral commissions by turnout (size weighted) (" + title + ");turnout,%;Number of electoral commissions (0.5% bins)", 220,-0.25, 109.75)

    winner_votes_hist =  ROOT.TH1D("winner_votes_hist", "Distribution of electoral commissions by Poroshenko votes (" + title + ");winner votes;Number of electoral commissions (--)", 10001,0, 10000)

    winner_votes_lastdigit_hist =  ROOT.TH1D("winner_votes_lastdigit_hist", "Distribution of electoral commissions by last digit of winner votes (" + title + ");last digit of winner votes;Number of electoral commissions (--)", 10,-0.5, 9.5)


    winner_weighted_hist =  ROOT.TH1D("winner_weighted_hist", "Distribution of electoral commissions by Poroshenko % (size weighted) (" + title + ");winner % ;Number of electoral commissions (0.5% bins)", 220, -0.25, 109.75)
    winner_hist =  ROOT.TH1D("winner_hist", "Distribution of electoral commissions by Poroshenko % (raw) (" + title + ");Poroshenko % ;Number of electoral commissions (0.5% bins)", 220, -0.25, 109.75)
    for fname in input_files:
        reader = csv.reader(open(fname), delimiter='\t')
        reader.next()
        for row in reader:


            values = map(float, row[4:])

            if values[6] != values[8]:
                print values[6], values[8]

            if values[1]:
                turnout = (values[8]) / values[1] * 100.0 # 9.К-во избирателей, принявших участие в голосовании / 2.К-во избирателей, внесенных в список
            else:
                turnout =  0


            if turnout:
                winner = values[21] / (values[8])* 100.0  # Порошенко / (9 К-во избирателей, принявших участие в голосовании)
                total_winner+= values[21]
                total += (values[8])

                valid = 1#values[9] / (values[9] + values[8])* 100.0
            else:
                winner = 0.0

            size = values[1]
            h2.Fill(turnout, winner, size)
            winner_valid.Fill(valid, winner, size)

            turnout_hist.Fill(turnout)
            turnout_weighted_hist.Fill(turnout,size)


            #~ if values[22] > 100:
            winner_weighted_hist.Fill(winner, size)
            winner_hist.Fill(winner)


            winner_votes_hist.Fill(values[21])
            winner_votes_lastdigit_hist.Fill(int(str(int(values[21]))[0]))

            turnout_arr.append(turnout)

            winner_arr.append(winner)


    #~ gr = ROOT.TGraph(len(turnout_arr), turnout_arr, winner_arr)
    #~ gr.Draw("A*")

    print total_winner, total
    print "Total winner: %2.2f%%"%(100.0 * total_winner/ total)
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
    h2_1.SetTitle("Fitted Poroshenko % mean value vs turnout (" + title + ")")
    h2_1.Draw()
    c01.SaveAs(title + "_2d_slices.png")


    #~ c1 = ROOT.TCanvas()
    #~ c1.cd()
#~
    #~ gaus_1 = ROOT.TF1("gaus_1","gaus",0, 55)
    #~ turnout_hist.Fit("gaus", "", "", 0, 54);
#~
    #~ turnout_hist.Draw()
    #~ c1.SaveAs(title + "_turnout.png")

    #~ TF1 *f1=gROOT->GetFunction("myfunc");
    #~ f1->SetParameters(800,1);


    c2 = ROOT.TCanvas()
    c2.cd()
    turnout_weighted_hist.Draw()
    c2.SaveAs(title + "_turnout_w.png")

    c3 = ROOT.TCanvas()
    c3.cd()
    winner_weighted_hist.GetXaxis().SetRangeUser(10,105)
    winner_weighted_hist.Draw()

    #~ g1 = ROOT.TF1("g1", "gaus", 0, 90)
    #~ g2 = ROOT.TF1("g2", "gaus", 0, 90)
    #~ bkg = ROOT.TF1("bkg", "gaus", 0, 90)
    #~ winner_weighted_hist.Fit("g1", "", "", 0, 30)
    #~ winner_weighted_hist.Fit("g2", "", "",  40, 90)
    #~ winner_weighted_hist.Fit("bkg", "", "",  0, 90)
    #~
    #~ total = ROOT.TF1("total", "gaus(0) + gaus(3)+gaus(6)", 0, 85)
    #~ total.SetParameters( g1.GetParameter(0),g1.GetParameter(1),g1.GetParameter(2),
                         #~ g2.GetParameter(0),g2.GetParameter(1),g2.GetParameter(2),
                         #~ bkg.GetParameter(0),bkg.GetParameter(1),bkg.GetParameter(2))
                         #~
    #~
    #~ winner_weighted_hist.Fit("total", "", "", 0,85)


    c3.SaveAs(title + "_winner_w.png")

    #~ c4 = ROOT.TCanvas()
    #~ c4.cd()
    #~ winner_hist.GetXaxis().SetRangeUser(10,105)
    #~ winner_hist.Draw()
    #~ c4.SaveAs(title + "_winner.png")

    #~ c5 = ROOT.TCanvas()
    #~ c5.cd()
    #~ winner_valid.Draw("COL CONT0")
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

