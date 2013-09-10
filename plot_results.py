#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv, sys, array
import ROOT
import math


def make_plots(title, input_files, close = True, party_num = 14, party_name = "ruling party"):
	ROOT.gStyle.SetOptFit(1)

	turnout_arr = array.array('d')
	rp_arr =  array.array('d')





	h2 = ROOT.TH2D("h2", "weighted " + party_name + " % vs turnout % (" + title + ");turnout,%;" + party_name + ",%", 105,0, 104, 105, 0, 104)
	rp_valid = ROOT.TH2D("rp_invalid", "weighted " + party_name + " % vs valid % (" + title + ");valid,%;" + party_name + ",%", 80 ,90, 110, 110, 0, 110)

	total_rp = 0
	total = 0

	turnout_hist =  ROOT.TH1D("turnout_hist", "Distribution of electoral commissions by turnout (" + title + " );turnout ,%; Number of electoral commissions (0.5% bins)", 220,0, 110)

	rp_abs_rate =  ROOT.TH1D("rp_abs_rate", "rp_abs_rate (" + title + " );turnout * " + party_name + " %; Number of electoral commissions (0.5% bins)", 220,0, 110)
	rp_abs_rate2 = ROOT.TH2D("h2", "weighted " + party_name + " abs % vs turnout % (" + title + ");turnout,%;turnout * " + party_name + ",%", 105,0, 104, 105, 0, 104)



	turnout_weighted_hist =  ROOT.TH1D("turnout_weighted_hist", "Distribution of electoral commissions by turnout (weighted) (" + title + ");turnout,%;Total electoral commissions size (0.5% bins)", 220,0, 110)

	rp_votes_hist =  ROOT.TH1D("rp_votes_hist", "Distribution of electoral commissions by " + party_name + " votes (" + title + ");" + party_name + " votes;Number of electoral commissions (--)", 10001,0, 10000)

	rp_votes_lastdigit_hist =  ROOT.TH1D("rp_votes_lastdigit_hist", "Distribution of electoral commissions by last digit of " + party_name + " votes (" + title + ");last digit of rp votes;Number of electoral commissions (--)", 10,-0.5, 9.5)


	rp_weighted_hist =  ROOT.TH1D("rp_weighted_hist", "Distribution of electoral commissions by " + party_name + " % (weighted) (" + title + ");" + party_name + " % ;Total electoral commissions size (0.5% bins)", 220, 0, 110)
	rp_hist =  ROOT.TH1D("rp_hist", "Distribution of electoral commissions by " + party_name + " % (raw) (" + title + ");" + party_name + " % ;Number of electoral commissions (0.5% bins)", 220, 0, 110)
	for fname in input_files:
		reader = csv.reader(open(fname))
		for row in reader:
			values = map(float, row[4:])


			if not values[0]:
				continue

			turnout = (values[2] + values[3]) / values[0] * 100.0


			total_ballots = values[7] + values[8]
			if total_ballots:


				rp = values[party_num] / (total_ballots)* 100.0 #
				total_rp+= values[party_num]
				total += total_ballots

				valid = values[8] / total_ballots * 100.0
			else:
				rp = 0.0

			h2.Fill(turnout, rp, values[0])
			rp_valid.Fill(valid, rp, values[0])

			turnout_hist.Fill(turnout)
			turnout_weighted_hist.Fill(turnout,values[0])


			if values[party_num] > 00:
				rp_weighted_hist.Fill(rp, values[0])
			rp_hist.Fill(rp)


			rp_votes_hist.Fill(values[party_num])
			rp_votes_lastdigit_hist.Fill(int(str(int(values[party_num]))[0]))

			rp_abs_rate.Fill(turnout * rp / 100, values[0])
			rp_abs_rate2.Fill(turnout, turnout * rp / 100, values[0])
			turnout_arr.append(turnout)

			rp_arr.append(rp)


	#~ gr = ROOT.TGraph(len(turnout_arr), turnout_arr, rp_arr)
	#~ gr.Draw("A*")

	print total_rp, total
	print "Total rp: %2.2f%%"%(100.0 * total_rp/ total)
	c0 = ROOT.TCanvas()
	c0.cd()
	h2.Draw("COL CONT0")
	print "Correlation factor: ", h2.GetCorrelationFactor()
	#~ raw_input()
	#~ sys.exit(0)
	h2.FitSlicesY()
	c0.SaveAs(title + "_2d.png")

	c01 = ROOT.TCanvas()
	c01.cd()

	h2_1 = ROOT.gDirectory.Get("h2_1")
	h2_1.GetXaxis().SetRangeUser(0,100)
	h2_1.GetYaxis().SetRangeUser(0,100)
	h2_1.SetTitle("Fitted " + party_name + " % mean value vs turnout (" + title + ")")
	h2_1.Draw()
	c01.SaveAs(title + "_2d_slices.png")


	c1 = ROOT.TCanvas()
	c1.cd()

	gaus_1 = ROOT.TF1("gaus_1","gaus",0, 55)
	turnout_hist.Fit("gaus", "", "", 0, 54);

	turnout_hist.Draw()
	c1.SaveAs(title + "_turnout.png")

	#~ TF1 *f1=gROOT->GetFunction("myfunc");
	#~ f1->SetParameters(800,1);


	c2 = ROOT.TCanvas()
	c2.cd()
	turnout_weighted_hist.Fit("gaus", "", "");
	turnout_weighted_hist.Draw()
	c2.SaveAs(title + "_turnout_w.png")

	c3 = ROOT.TCanvas()
	c3.cd()
	rp_weighted_hist.GetXaxis().SetRangeUser(0,105)
	rp_weighted_hist.Fit("gaus", "", "");

	rp_weighted_hist.Draw()

	#~ g1 = ROOT.TF1("g1", "gaus", 0, 90)
	#~ g2 = ROOT.TF1("g2", "gaus", 0, 90)
	#~ bkg = ROOT.TF1("bkg", "gaus", 0, 90)
	#~ rp_weighted_hist.Fit("g1", "", "", 0, 30)
	#~ rp_weighted_hist.Fit("g2", "", "",  40, 90)
	#~ rp_weighted_hist.Fit("bkg", "", "",  0, 90)
	#~
	#~ total = ROOT.TF1("total", "gaus(0) + gaus(3)+gaus(6)", 0, 85)
	#~ total.SetParameters( g1.GetParameter(0),g1.GetParameter(1),g1.GetParameter(2),
						 #~ g2.GetParameter(0),g2.GetParameter(1),g2.GetParameter(2),
						 #~ bkg.GetParameter(0),bkg.GetParameter(1),bkg.GetParameter(2))
						 #~
	#~
	#~ rp_weighted_hist.Fit("total", "", "", 0,85)


	c3.SaveAs(title + "_rp_w.png")

	c4 = ROOT.TCanvas()
	c4.cd()
	rp_hist.GetXaxis().SetRangeUser(0,105)
	rp_hist.Draw()
	c4.SaveAs(title + "_rp.png")

	#~ c5 = ROOT.TCanvas()
	#~ c5.cd()
	#~ rp_valid.Draw("COL CONT0")
	#~ c5.SaveAs(title + "_valid_2d.png")

	#~ c6 = ROOT.TCanvas()
	#~ c6.cd()
	#~ rp_abs_rate2.Draw()

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
    #~ make_plots(title, input_files, close = False)

    make_plots(title + '_navalny' , input_files, close = False, party_num = 13, party_name = 'navalny')
