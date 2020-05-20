#This file writes OpenDSS circuit from CYME reader.
#Written for ASU by Karen Montano, Sushrut Thakar

# This version contains the script to generate cvs files of the system under study
# This version contains the code to generate the PV generators in the system
# This version contains the generation of LineCodes acording to cable type and geometry

# If changes are needed, please do it with discretion
###############################################################################################################
#Usage
#Read from cyme version 8.2
# Change Line Definition

###############################################################################################################
#imports following modules, make sure to install them.
#from collections import namedtuple
import os
#import Cyme_Reader as reader
import math
import numpy as np
import cmath

###############################################################################################################
#function definitions:

#convert functions
def convert_master(Substationlist, HeadNodeslist, Sourcelist, SourceEquivalentlist, Feederlist, Transformerlist, casename):
	DSSMaster = []
	DSSMaster.append('!Master File for case {}\n'.format(casename))
	DSSMaster.append('Clear\n'.format(casename))
	DSSMaster.append('Set Datapath = "{}\{}"\n'.format(os.path.dirname(os.path.abspath(__file__)),casename))
	Line = 'New Circuit.'+casename
	Line = Line + ' bus1='+Sourcelist[0].NodeID.replace(".","_")+'.1.2.3'
	Line = Line + ' BasekV='+SourceEquivalentlist[0].Voltage
	if (float(Sourcelist[0].OperatingVoltageA)*(math.sqrt(3)))/12.47 > 0:
		Line = Line + ' pu=' + str((float(Sourcelist[0].OperatingVoltageA)*(math.sqrt(3)))/12.47)
	elif (float(SourceEquivalentlist[7].OperatingVoltage1)*(math.sqrt(3)))/12.47 > 0:
		Line = Line + ' pu=' + str((float(SourceEquivalentlist[7].OperatingVoltage1)*(math.sqrt(3)))/12.47)
	else:
		print (' no operating voltage for circuit')
	Line = Line + ' r1='+SourceEquivalentlist[0].FirstLevelR1
	Line = Line + ' r0='+SourceEquivalentlist[0].FirstLevelR0

	Line = Line + ' x1='+SourceEquivalentlist[0].FirstLevelX1
	Line = Line + ' x0='+SourceEquivalentlist[0].FirstLevelX0

	Line = Line + '\n'
	#objects: redirect
	#TODO: Maybe do something for definitions/impedances change.
	DSSMaster.append(Line)
	DSSMaster.append('Redirect linespacing.dss')
	DSSMaster.append('Redirect wiredata.dss')
	DSSMaster.append('Redirect cablemodel.dss')
	DSSMaster.append('Redirect linegeometryover.dss')
	DSSMaster.append('Redirect linegeometryunder.dss')
	DSSMaster.append('Redirect protection.dss')
	DSSMaster.append('Redirect linecodes.dss')		
	DSSMaster.append('Redirect linesover.dss')
	DSSMaster.append('Redirect linesunder.dss')	
	DSSMaster.append('!Redirect loadshapes.dss')
	DSSMaster.append('Redirect loads.dss')
	DSSMaster.append('Redirect transformerscodes.dss')
	DSSMaster.append('Redirect transformers.dss')
	DSSMaster.append('Redirect capacitors.dss')
	DSSMaster.append('Redirect generators.dss')
	DSSMaster.append('Redirect loadmismatch.dss')
	DSSMaster.append('Redirect switchcontrol.dss')
	DSSMaster.append('Buscoords buscoords.dss')
	DSSMaster.append('')
	#energymeters and monitors
	DSSMaster.append('')
	#solve etc
	Line = 'set Voltagebases = ['
	Line = Line + SourceEquivalentlist[0].Voltage + ','+ str(2*float(Transformerlist[0].KVLLsec))+ ','+ str(float(Transformerlist[0].KVLLsec)*(math.sqrt(3)))+ ',' + Transformerlist[6].KVLLsec
	# for 7.2 kV, str(float(SourceEquivalentlist[0].Voltage)/(math.sqrt(3)))
	Line = Line + ']'
	DSSMaster.append(Line)
	DSSMaster.append('CalcVoltagebases')
	DSSMaster.append('')
	DSSMaster.append('!New Energymeter.CW13 Element= Line.8638910 Terminal=1 option=(r,e,v)')
	DSSMaster.append('set mode = snap')
	DSSMaster.append('solve')
	DSSMaster.append('')
	#outputs
	DSSMaster.append('!plot profile')
	return DSSMaster

def convert_linespacing(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist):
	DSSLinespacing = []
	for linespace in SpacingTableForLinelist:
		Line = 'New Linespacing.'+ linespace.ID.replace(" ","_")
		if linespace.NBPhasesPerCircuit == '':
			continue
		Line = Line + ' nconds='+str(int(linespace.NBPhasesPerCircuit)*int(linespace.NBConductorsPerPhase)+int(linespace.NBNeutrals))
		Line = Line + ' nphases='+linespace.NBPhasesPerCircuit
		Line = Line + ' x='+"["+linespace.PosOfCond1_X +" " + linespace.PosOfCond2_X+" " + linespace.PosOfCond3_X+" " 
		if linespace.NBNeutrals == '1':
			Line = Line + linespace.PosOfNeutralCond_X
		Line = Line +"]"
		Line = Line + ' h='+"["+linespace.PosOfCond1_Y +" " + linespace.PosOfCond2_Y+" " + linespace.PosOfCond3_Y+" " 
		if linespace.NBNeutrals == '1':
			Line = Line + linespace.PosOfNeutralCond_Y
		Line = Line +"]"
		Line = Line + ' units='+'m'

		DSSLinespacing.append(Line)

	return DSSLinespacing

def convert_wiredata(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist):
	DSSWiredata = []
	for wiredata in Conductorlist:
		if wiredata.ID == 'NONE':
			continue
		Line = 'New Wiredata.'+ wiredata.ID
		Line = Line + ' Capradius='+str(math.sqrt(float(wiredata.Size_mm2)/math.pi))
		Line = Line + ' GMR='+wiredata.GMR
		if float(wiredata.Diameter) == 0:
			continue
		Line = Line + ' DIAM='+wiredata.Diameter
		Line = Line + ' RAC='+ wiredata.R25
		Line = Line + ' RDC='+ wiredata.FirstResistanceDC
		Line = Line + ' NormAmps='+wiredata.Amps
		Line = Line + ' Runits='+'km'
		Line = Line + ' radunits='+'cm'
		Line = Line + ' gmrunits='+'cm'
		
		
		DSSWiredata.append(Line)
	
	return DSSWiredata
	

def convert_cablemodel(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist):
	DSSCablemodel = []
	for cables in Cablelist:
		Line = 'New CNData.'+ cables.ID
		
		Line = Line + ' Runits=mm Radunits=mm GMRunits=mm'
		
		cablename = cables.ID
		insulationindex = -1
		for i in range(len(CableInsulationlist)):
			if cablename == CableInsulationlist[i].ID:
				insulationindex = i
		if insulationindex == -1 :
			print('Insulation name not found')
		
		cablename = cables.ID
		conductorindex = -1
		for i in range(len(CableConductorlist)):
			if cablename == CableConductorlist[i].ID:
				conductorindex = i
		if conductorindex == -1 :
			print('Conductor name not found')
			
		cablename = cables.ID
		ccneutralindex = -1
		for i in range(len(CableConcentricNeutrallist)):
			if cablename == CableConcentricNeutrallist[i].ID:
				ccneutralindex = i
			elif cablename == 'DEFAULT':
				ccneutralindex = -2
		if ccneutralindex == -1 :
			print('cablemodel_No neutral name, {} not found'.format(cables.ID))
			continue
		
		#cable
		Line = Line + ' InsLayer='+ CableInsulationlist[insulationindex].Thickness
		Line = Line + ' DiaIns='+ str(float(cables.OverallDiameter) - 2*float(CableConcentricNeutrallist[ccneutralindex].Thickness))
		Line = Line + ' DiaCable='+ cables.OverallDiameter
		Line = Line + ' EpsR='
		if CableInsulationlist[insulationindex].InsulationMaterialID == 'XLPE_FILLED':
			Line = Line + '2.3'
		elif CableInsulationlist[insulationindex].InsulationMaterialID == 'EPR':
			Line = Line + '3.0'
		elif CableInsulationlist[insulationindex].InsulationMaterialID == 'XLPE_UNFILLED':
			Line = Line + '2.5'
		else:
			print('Insulation material, {} not fount'.format(CableInsulationlist[insulationindex].InsulationMaterialID))
		
		#Phase Conductor
		if CableConductorlist[conductorindex].MaterialID == 'ALUMINUM':
			Elecresis = 0.0000283
			Area = float(CableConductorlist[conductorindex].Size_mm2) 		
			Line = Line + ' RDC='+ str(Elecresis/Area)
		elif CableConductorlist[conductorindex].MaterialID == 'COPPER':
			Elecresis = 0.000017241
			Area = float(CableConductorlist[conductorindex].Size_mm2) 			
			Line = Line + ' RDC='+ str(Elecresis/Area)
		else:
			print('No matterial found')		

		Line = Line + ' diam='+ CableConductorlist[conductorindex].Diameter
		
		# Neutral
		if CableConcentricNeutrallist[ccneutralindex].MaterialID == 'ALUMINUM':
			Elecresis = 0.0000283
			Area = math.pi * (float(CableConcentricNeutrallist[ccneutralindex].Thickness)/2)**2
			Line = Line + ' Rstrand='+ str(1.02*Elecresis/Area)
		elif CableConcentricNeutrallist[ccneutralindex].MaterialID == 'COPPER':
			Elecresis = 0.000017241
			Area = math.pi * (float(CableConcentricNeutrallist[ccneutralindex].Thickness)/2)**2		
			Line = Line + ' Rstrand='+ str(1.02*Elecresis/Area)
		else:
			print('No matterial found')		
		
		Line = Line + ' DiaStrand='+ CableConcentricNeutrallist[ccneutralindex].Thickness
		Line = Line + ' K='+ CableConcentricNeutrallist[ccneutralindex].NumberOfWires
		
	
		DSSCablemodel.append(Line)

	return DSSCablemodel

def convert_linegeometryover(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist):
	DSSLinegeometryOver = []
	for linegeo in OverheadByphaseSettinglist:
		
		Line = 'New LineGeometry.'+ linegeo.DeviceNumber
		
		overheadgeo= linegeo.SectionID
		overheadindex = -1
		for i in range(len(Sectionlist)):
			if overheadgeo == Sectionlist[i].SectionID:
				overheadindex = i
		if overheadindex == -1 :
			print('No conductors not found')
		
		Line = Line + ' nconds=' + str(len(Sectionlist[overheadindex].Phase)) 
		Line = Line + ' nphases=' + str(len(Sectionlist[overheadindex].Phase)) 
		Line = Line + ' spacing='+linegeo.SpacingID.replace(" ","_")
		Line = Line + ' wires='+ "["+linegeo.CondID_A +" " + linegeo.CondID_B+" " + linegeo.CondID_C +"]"

		if len(Sectionlist[overheadindex].Phase) > len(Sectionlist[overheadindex].Phase):
			Line = Line + ' reduce=yes'
				
		DSSLinegeometryOver.append(Line)

	return DSSLinegeometryOver
	
def convert_linegeometryunder(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist):
	DSSLinegeometryUnder = []
			
	for linegeound in UndergroundlineSettinglist:
		
		Line = 'New LineGeometry.'+ linegeound.DeviceNumber
		
		undergeo= linegeound.SectionID
		undergeoindex = -1
		for i in range(len(Sectionlist)):
			if undergeo == Sectionlist[i].SectionID:
				undergeoindex = i
		if undergeoindex == -1 :
			print('No conductors not found')
		
		Line = Line + ' nconds=' + str(int(linegeound.NumberOfCableInParallel)*len(Sectionlist[undergeoindex].Phase))
		Line = Line + ' nphases=' + str(len(Sectionlist[undergeoindex].Phase)) 
		
		#TODO: find a way to get default values for cables
		if linegeound.LineCableID == 'UA1/0T_UG':
						
			if str(len(Sectionlist[undergeoindex].Phase)) in ['1']:	
				Line = Line + ' CNcables=' + linegeound.LineCableID
				Line = Line + ' h=0.05'
				Line = Line + ' x=0' 
				Line = Line + ' units=ft'
			elif str(len(Sectionlist[undergeoindex].Phase)) in ['3']:
				if str(int(linegeound.NumberOfCableInParallel)) in ['1']:	
					Line = Line + ' CNcables=' + "[" + linegeound.LineCableID +" " + linegeound.LineCableID +" " + linegeound.LineCableID + "]"
					Line = Line + ' cond=1 h=0.05 x=-0.05'
					Line = Line + ' cond=2 h=0.05 x=0.05'
					Line = Line + ' cond=3 h=0.14 x=0'
					Line = Line + ' units=ft'
				elif str(int(linegeound.NumberOfCableInParallel)) in ['2']:
					Line = Line + ' cond=1' + ' CNcable=' + linegeound.LineCableID + ' h=0.08' + " x=-0.08"
					Line = Line + ' cond=2' + ' CNcable=' + linegeound.LineCableID + '  h=0.08' + " x=0.08" 
					Line = Line + ' cond=3' + ' CNcable=' + linegeound.LineCableID + '  h=0.2' + " x=0"
					Line = Line + ' cond=4' + ' CNcable=' + linegeound.LineCableID + '  h=0.08' + " x=0.25"
					Line = Line + ' cond=5' + ' CNcable=' + linegeound.LineCableID + '  h=0.08' + " x=0.4" 
					Line = Line + ' cond=6' + ' CNcable=' + linegeound.LineCableID + '  h=0.2' + " x=0.3"
					Line = Line + ' units=ft'
			else:
				print ('do not identified phase')
		
			#TODO: Will need to add new cables for any new case.
		
		else: 
			print ('No cable type identified for distances')
		
		
		if int(linegeound.NumberOfCableInParallel)*len(Sectionlist[undergeoindex].Phase) > len(Sectionlist[undergeoindex].Phase):
			Line = Line + ' reduce=yes'
		
		DSSLinegeometryUnder.append(Line)

	return DSSLinegeometryUnder

def convert_lineover(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist, switchlist):
	DSSLinesOver = []
	CSVLinesOver = ['DeviceID, From bus, To bus, Phase, geocode, length']
	
	for linesys in OverheadByphaseSettinglist:
		if linesys.DeviceNumber in switchlist:
			Line = 'Edit'
		else:
			Line = 'New'
		Line = Line + ' Line.'+ linesys.DeviceNumber
		
		linebus = linesys.SectionID
		linebusindex = -1
		for i in range(len(Sectionlist)):
			if linebus == Sectionlist[i].SectionID:
				linebusindex = i
		if linebusindex == -1 :
			print('Line bus not found')
		
		if Sectionlist[linebusindex].Phase in ['A']:
			Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.1.0'
			Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.1.0'
		elif Sectionlist[linebusindex].Phase in ['B']:
			Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.2.0'
			Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.2.0'
		elif Sectionlist[linebusindex].Phase in ['C']:
			Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.3.0'
			Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.3.0'		
		elif Sectionlist[linebusindex].Phase in ['ABC']:
			Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.1.2.3'
			Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.1.2.3'
		else:
			print ('do not identified phase')
		
		Line = Line + ' Geometry='+linesys.DeviceNumber
		Line = Line + ' length='+ linesys.Length
		Line = Line + ' units='+'m'

		
		DSSLinesOver.append(Line)
		csvline = linesys.DeviceNumber+ "," + Sectionlist[linebusindex].FromNodeID.replace(".","_") + "," + Sectionlist[linebusindex].ToNodeID.replace(".","_") +","+Sectionlist[linebusindex].Phase+","+linesys.DeviceNumber+","+linesys.Length
		CSVLinesOver.append(csvline)
		
	return DSSLinesOver,CSVLinesOver

def convert_lineunder(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist, switchlist):
	DSSLinesUnder = []
	CSVLinesUnder = ['Switch, DeviceID, From bus, To bus, Phase, geocode, length']
	
	for lineund in UndergroundlineSettinglist:
		if lineund.DeviceNumber in switchlist:
			Line = 'Edit'
			Switchline = 'Switch'
		else:
			Line = 'New'
			Switchline = 'No'
		Line = Line + ' Line.'+ lineund.DeviceNumber
		
		linebus = lineund.SectionID
		linebusindex = -1
		for i in range(len(Sectionlist)):
			if linebus == Sectionlist[i].SectionID:
				linebusindex = i
		if linebusindex == -1 :
			print('Line bus not found')
		
		if Sectionlist[linebusindex].Phase in ['A']:
			Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.1.0'
			Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.1.0'
			Line = Line + ' phases=1'
		elif Sectionlist[linebusindex].Phase in ['B']:
			Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.2.0'
			Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.2.0'
			Line = Line + ' phases=1'
		elif Sectionlist[linebusindex].Phase in ['C']:
			Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.3.0'
			Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.3.0'		
			Line = Line + ' phases=1'			
		elif Sectionlist[linebusindex].Phase in ['ABC']:
			if str(int(lineund.NumberOfCableInParallel)) in ['1']:
				Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.1.2.3'
				Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.1.2.3'
				Line = Line + ' phases=3'
			elif str(int(lineund.NumberOfCableInParallel)) in ['2']:
				Line = Line + ' bus1='+ Sectionlist[linebusindex].FromNodeID.replace(".","_")+'.1.2.3.1.2.3'
				Line = Line + ' bus2='+ Sectionlist[linebusindex].ToNodeID.replace(".","_")+'.1.2.3.1.2.3'
				Line = Line + ' phases=3'
		else:
			print ('do not identified phase')
		
		#TODO: change if cable type has 0 R1
		if lineund.LineCableID in ['CableWith0R1','Cable2With0R1']:
			Line = Line + ' R1=1.00E-07 R0=0 X1=0 X0=0 B1=0 B0=0 length=1'
		else:	
			Line = Line + ' geometry='+ lineund.DeviceNumber
		Line = Line + ' length='+ lineund.Length
		Line = Line + ' units='+'m'
		Line = Line + ' basefreq='+'60'
			
			
		DSSLinesUnder.append(Line)
		csvline = Switchline+ "," +lineund.DeviceNumber+ "," + Sectionlist[linebusindex].FromNodeID.replace(".","_") + "," + Sectionlist[linebusindex].ToNodeID.replace(".","_") +","+Sectionlist[linebusindex].Phase+","+lineund.DeviceNumber+","+lineund.Length
		CSVLinesUnder.append(csvline)	
		
	return DSSLinesUnder, CSVLinesUnder

def convert_transformercodes(Transformerlist, TransformerSettinglist):
	DSSTransformerscodes = []
	CSVTransformers = ['Code ID, phases, R, X, Vprimary, Vsecondary, KVA']
	
	for transformercus in Transformerlist:
		Line = 'New XfmrCode.'+transformercus.ID
		
		if transformercus.Type in ['1']:
			Line = Line + ' Phases='+'1'
		else:
			Line = Line + ' Phases='+'3'
		
		
		Z1 = float(transformercus.Z1) * float (transformercus.KVA) / 100
		Z0 = float(transformercus.Z0) * float (transformercus.KVA) / 100
		XR = float(transformercus.XR) 
		XR0 = float(transformercus.XR0) 
		R1 = Z1 / math.sqrt(1 + XR * XR)
		R0 = Z0 / math.sqrt(1 + XR0 * XR0)
		X1 = Z1 / math.sqrt(1 + 1 / (XR * XR))
		X0 = Z0 / math.sqrt(1 + 1 / (XR0 * XR0))
		complex0 = complex(R0, X0)
		complex1 = complex(R1, X1)
		matrix = np.matrix(
			[[complex0, 0, 0], [0, complex1, 0], [0, 0, complex1]]
		)
		a = 1 * cmath.exp(2 * math.pi * 1j / 3)
		T = np.matrix([[1., 1., 1.], [1., a * a, a], [1., a, a * a]])
		T_inv = T.I
		Zabc = T * matrix * T_inv
		Z_perc = ((Zabc.item((0, 0))) / float (transformercus.KVA)) * 100
		R_perc = Z_perc.real/2 
		x12 = Z_perc.imag
		
		Line = Line + ' Windings='+'2' #both cases
		Line = Line + ' Wdg='+'1'
		
		if transformercus.Type in ['1']:
			Line = Line + ' kV='+transformercus.KVLLprim#'7.2'
		else:
			Line = Line + ' kV='+transformercus.KVLLprim#'12.47'
				
		Line = Line + ' kVA='+transformercus.KVA
		Line = Line + ' %R='+str(R_perc)
		
		
		
		Line = Line + ' Wdg='+'2'
		if transformercus.Type in ['1']:
			Line = Line + ' kV='+transformercus.KVLLsec#'0.207'
		else:
			Line = Line + ' kV='+transformercus.KVLLsec#'0.480'
				
		Line = Line + ' kVA='+transformercus.KVA
		Line = Line + ' %R='+str(R_perc)
		
		Line = Line + ' XHL='+str(x12)
		
		Line = Line + ' %NoLoadLoss='+str((float(transformercus.NoLoadLosses)/(float(transformercus.KVA)))*100)

		DSSTransformerscodes.append(Line)
		csvtransformers = transformercus.ID + "," + transformercus.Type+ "," + str(2* R_perc) + "," + str(x12)+ "," +transformercus.KVLLprim+ "," +transformercus.KVLLsec+ "," +transformercus.KVA
		CSVTransformers.append(csvtransformers)
		
	return DSSTransformerscodes,CSVTransformers
	
def convert_transformer(Transformerlist, TransformerSettinglist, Sectionlist):
	DSSTransformers = []
	CSVTransformers2 = ['Code ID, Bus 1, Bus 2, Connection']
	
	for trafos in TransformerSettinglist:
	
		Line = 'New Transformer.'+trafos.DeviceNumber
		Line = Line + ' XfmrCode='+trafos.EqID
		
		Line = Line + ' Wdg='+'1'
		
		trafoprimary = trafos.SectionID
		trafoprimaryindex = -1
		for i in range(len(Sectionlist)):
			if trafoprimary == Sectionlist[i].SectionID:
				trafoprimaryindex = i
		if trafoprimaryindex == -1 :
			print('Trafo bus primary not found')
		Line = Line + ' Bus='+Sectionlist[trafoprimaryindex].FromNodeID.replace(".","_")
		
		if Sectionlist[trafoprimaryindex].Phase in ['A']:
			Line = Line +'.1.0'
		elif Sectionlist[trafoprimaryindex].Phase in ['B']:
			Line = Line +'.2.0'
		elif Sectionlist[trafoprimaryindex].Phase in ['C']:
			Line = Line +'.3.0'		
		elif Sectionlist[trafoprimaryindex].Phase in ['ABC']:
			Line = Line +'.1.2.3'
		else:
			print ('do not identified phase')
		
		Line = Line + ' Tap='+str(float(trafos.PrimTap)/100)
		
		if trafos.Conn == '6':
			Line = Line +' Conn=wye'
		elif trafos.Conn == '0':
			Line = Line +' Conn=wye'
		else:
			print ('connection is different')
		
		Line = Line + ' Wdg='+'2'
		Line = Line + ' Bus='+Sectionlist[trafoprimaryindex].ToNodeID.replace(".","_")
		
		if Sectionlist[trafoprimaryindex].Phase in ['A']:
			Line = Line +'.1.0'
		elif Sectionlist[trafoprimaryindex].Phase in ['B']:
			Line = Line +'.2.0'
		elif Sectionlist[trafoprimaryindex].Phase in ['C']:
			Line = Line +'.3.0'		
		elif Sectionlist[trafoprimaryindex].Phase in ['ABC']:
			Line = Line +'.1.2.3'
		else:
			print ('do not identified phase')
		
		Line = Line + ' Tap='+str(float(trafos.SecondaryTap)/100)
		
		if trafos.Conn == '6':
			Line = Line +' Conn=delta'
		elif trafos.Conn == '0':
			Line = Line +' Conn=wye'
		else:
			print ('connection is different')
		
		Line = Line + ' core=shell'
		
		
		Line = Line + ' Basefreq='+'60'
		
		DSSTransformers.append(Line)
		csvtransformers2 = trafos.DeviceNumber + "," + Sectionlist[trafoprimaryindex].FromNodeID.replace(".","_")+ "," +Sectionlist[trafoprimaryindex].ToNodeID.replace(".","_")+ "," + trafos.Conn
		CSVTransformers2.append(csvtransformers2)
		
	return DSSTransformers, CSVTransformers2

def convert_load(CustomerClasslist, Loadslist, CustomerLoadslist, LoadModelInformationlist, LoadEquivalentlist, Sectionlist, Transformerlist, TransformerSettinglist):
	DSSLoads = []
	CSVLoads = ['Customer Number, Bus, Phase, Active Power [kW], Reactive Power [kVar], PF, Connection, ValueType']
			
	LoadModel = '1'
	#TODO: see what loadmodel is proper.
	
	for Loadcust in CustomerLoadslist:
		if Loadcust.LoadModelID == LoadModel:
			Line = 'New Load.'+Loadcust.CustomerNumber+'_'+Loadcust.LoadModelID
		else:
			continue
		
		if Loadcust.LoadPhase in ['A','B','C']:
			Line = Line + ' Phases='+'1'
		else:
			Line = Line + ' Phases='+'3'
		
		
		loadsection = Loadcust.SectionID
		loadsectionindex = -1
		for i in range(len(Sectionlist)):
			if loadsection == Sectionlist[i].SectionID:
				loadsectionindex = i
		if loadsectionindex == -1 :
			print('Load section not found')
		Line = Line + ' Bus1='+Sectionlist[loadsectionindex].FromNodeID.replace(".","_")
				
		if Loadcust.LoadPhase in ['A']:
			Line = Line +'.1.0'
		elif Loadcust.LoadPhase in ['B']:
			Line = Line +'.2.0'
		elif Loadcust.LoadPhase in ['C']:
			Line = Line +'.3.0'		
		elif Loadcust.LoadPhase in ['ABC']:
			Line = Line +'.1.2.3'
		else:
			print ('do not identified phase')
		
		if (Loadcust.Value1) == "0.000000":
			continue
		if Loadcust.ValueType == '2':
			Line = Line + ' kW='+Loadcust.Value1
			Line = Line + ' pf='+str(float(Loadcust.Value2)/100)
		elif Loadcust.ValueType == '0':
			Line = Line + ' kW='+Loadcust.Value1
			Line = Line + ' kVAr='+Loadcust.Value2
		else:
			print('A load with ValueType = {}'.format(Loadcust.ValueType))
			
		if Loadcust.LoadPhase in ['A','B','C']:
			Line = Line + ' kV='+'0.240'
		else:
			Line = Line + ' kV='+'0.208'
			
		
		Line = Line + ' Basefreq='+'60'
		Line = Line + ' Model='+'1'
		Line = Line + ' Vminpu='+'0.95'
		Line = Line + ' Vmaxpu='+'1.05'
		DSSLoads.append(Line)
		csvline = Loadcust.CustomerNumber+","+ Sectionlist[loadsectionindex].FromNodeID.replace(".","_")+","+Loadcust.LoadPhase+","+Loadcust.Value1+","+Loadcust.Value2+","+str(float(Loadcust.Value2)/100)+","+"wye"+","+Loadcust.ValueType
		CSVLoads.append(csvline)
		
	return DSSLoads,CSVLoads

def convert_generators(Sectionlist, Electronicconvertergeneratorlist, Electronicconvertergeneratorsettinglist, Converterlist, Convertercontrolsettinglist, Longtermdynamicscurveextlist, Dggenerationmodellist, Controlleddevicelist):
	DSSGenerators = []
	CSVPVs = ['Name, Bus, Phase, Voltage Level, Power Rating [kVA], PF']
	
	for genpv in Electronicconvertergeneratorsettinglist:
		
		Line = 'New generator.'+genpv.DeviceNumber
				
		pvsection = genpv.SectionID
		pvsectionindex = -1
		for i in range(len(Sectionlist)):
			if pvsection == Sectionlist[i].SectionID:
				pvsectionindex = i
		if pvsectionindex == -1 :
			print('PV section not found')
		Line = Line + ' Bus1='+Sectionlist[pvsectionindex].FromNodeID.replace(".","_")
				
		if genpv.EqPhase in ['A']:
			Line = Line +'.1.0'
			Line = Line +' phases=1'
		elif genpv.EqPhase in ['B']:
			Line = Line +'.2.0'
			Line = Line +' phases=1'
		elif genpv.EqPhase in ['C']:
			Line = Line +'.3.0'	
			Line = Line +' phases=1'			
		elif genpv.EqPhase in ['ABC']:
			Line = Line +'.1.2.3'
			Line = Line +' phases=3'
		else:
			print ('do not identified PV phase')
		
		pvrating = genpv.DeviceNumber
		pvratingindex = -1
		for i in range(len(Dggenerationmodellist)):
			if pvrating == Dggenerationmodellist[i].DeviceNumber and Dggenerationmodellist[i].LoadModelName == 'DEFAULT':
				pvratingindex = i
		if pvratingindex == -1 :
			print('PV rating not found')
		
		if float(Dggenerationmodellist[pvratingindex].ActiveGeneration) < 100:
			Line = Line + ' kW='+Dggenerationmodellist[pvratingindex].ActiveGeneration
			if float(Dggenerationmodellist[pvratingindex].PowerFactor) == 1.000000:
				Line = Line + ' pf='+Dggenerationmodellist[pvratingindex].PowerFactor
			else:
				Line = Line + ' pf='+str(float(Dggenerationmodellist[pvratingindex].PowerFactor)/100)
		else:
			pvratingindex = -1
			for i in range(len(Dggenerationmodellist)):
				if pvrating == Dggenerationmodellist[i].DeviceNumber and Dggenerationmodellist[i].LoadModelName == 'LoadModelName':
					#TODO: figure the proper load model out
					pvratingindex = i
			if pvratingindex == -1 :
				print('PV rating not found')
		
		if float(Dggenerationmodellist[pvratingindex].ActiveGeneration) < 100:
			Line = Line + ' kW='+Dggenerationmodellist[pvratingindex].ActiveGeneration
			if float(Dggenerationmodellist[pvratingindex].PowerFactor) == 1.000000:
				Line = Line + ' pf='+Dggenerationmodellist[pvratingindex].PowerFactor
			else:
				Line = Line + ' pf='+str(float(Dggenerationmodellist[pvratingindex].PowerFactor)/100)
		else:
			#print ('generator {} is not used'.format(genpv.DeviceNumber))
			continue
		
					
		if genpv.EqPhase in ['A','B','C']:
			Line = Line + ' kV=0.240'
		else:
			print('three phase PV found')
		
		Line = Line + ' Basefreq='+'60'
		Line = Line + ' Model='+'7'
		Line = Line + ' Vminpu='+'0.95'
		Line = Line + ' Vmaxpu='+'1.05'
		
		DSSGenerators.append(Line)
		csvline = genpv.DeviceNumber+','+Sectionlist[pvsectionindex].FromNodeID+','+genpv.EqPhase+','+'7.2'+','+Dggenerationmodellist[pvratingindex].ActiveGeneration+','+'1.0'
		CSVPVs.append(csvline)
		
	return DSSGenerators,CSVPVs

def convert_capacitors(ShuntCapacitorSettinglist, CapacitorExtltdlist, Sectionlist):
	DSSCapacitors = []
	CSVCapacitors = ['Rating (kVAR), Bus, Phases, Configuration']
	
	for capacitors in ShuntCapacitorSettinglist:
		Line = 'New Capacitor.'+capacitors.DeviceNumber

		capsection = capacitors.SectionID
		capssectionindex = -1
		for i in range(len(Sectionlist)):
			if capsection == Sectionlist[i].SectionID:
				capssectionindex = i
		if capssectionindex == -1 :
			print('Capacitor section not found')
		if capacitors.Location == '2':
			Line = Line + ' Bus1='+Sectionlist[capssectionindex].FromNodeID.replace(".","_")
		else:
			print('Capacitor location is not 2/To bus. Please check and update the node.')
		if Sectionlist[capssectionindex].Phase in ['A']:
			Line = Line +'.1.0'+ ' Phases='+'1'
		elif Sectionlist[capssectionindex].Phase in ['B']:
			Line = Line +'.2.0'+ ' Phases='+'1'
		elif Sectionlist[capssectionindex].Phase in ['C']:
			Line = Line +'.3.0'+ ' Phases='+'1'		
		elif Sectionlist[capssectionindex].Phase in ['ABC']:
			Line = Line +'.1.2.3'+ ' Phases='+'3'
		else:
			print ('do not identified phase')
		
		Line = Line + ' kVAr='+ str(float(capacitors.SwitchedKVARA)+float(capacitors.SwitchedKVARB)+float(capacitors.SwitchedKVARC))
		
		Line = Line + ' kV=12.47'
		
		if capacitors.Connection == 'Y':
			Line = Line + ' Conn='+'wye'
		else:
			Line = Line + ' Conn='+'delta'
		
		Line = Line + ' Basefreq='+'60'
		DSSCapacitors.append(Line)
		csvcapacitors =  str(float(capacitors.SwitchedKVARA)+float(capacitors.SwitchedKVARB)+float(capacitors.SwitchedKVARC))+ "," + Sectionlist[capssectionindex].FromNodeID.replace(".","_")+ "," + Sectionlist[capssectionindex].Phase+ "," +capacitors.Connection		
		CSVCapacitors.append(csvcapacitors)
	
	return DSSCapacitors, CSVCapacitors


def convert_protection(Switchlist, Breakerlist, Fuselist, SwitchSettinglist, BreakerSettinglist, FuseSettinglist, OvercurrentRelayInstrumentlist, CurrentTransformerInstrumentlist,OverheadByphaseSettinglist,UndergroundlineSettinglist, Sectionlist):
	DSSProtecction = []
	DSSSwitchcontrol = []
	switchlist = []
	CSVSW = ['Device Number, Location - Overhead, Location - Underhead, SW Location, Phase, Type, Cabinate/Transformer Location ']
	
	for protectssw in SwitchSettinglist:	
		switch = protectssw.SectionID
		swindexover = -1
		swindexunder = -1
		for i in range(len(OverheadByphaseSettinglist)):
			if switch == OverheadByphaseSettinglist[i].SectionID:
				swindexover = i
		if swindexover == -1 :
			for i in range(len(UndergroundlineSettinglist)):
				if switch == UndergroundlineSettinglist[i].SectionID:
					swindexunder = i
			if swindexunder == -1 :	
				print("no switch")
			else:
				if UndergroundlineSettinglist[swindexunder].DeviceNumber in switchlist:
					Line = "Edit Line."
				else:
					Line = "New Line."
				Line = Line +UndergroundlineSettinglist[swindexunder].DeviceNumber
				switchlist.append(UndergroundlineSettinglist[swindexunder].DeviceNumber)
				SWLine = 'New SwtControl.'+UndergroundlineSettinglist[swindexunder].DeviceNumber
				SWLine = SWLine + ' SwitchedObj=Line.'+UndergroundlineSettinglist[swindexunder].DeviceNumber
		else:
			if OverheadByphaseSettinglist[swindexover].DeviceNumber in switchlist:
				Line = "Edit Line."
			else:
				Line = "New Line."
			Line = Line +OverheadByphaseSettinglist[swindexover].DeviceNumber
			switchlist.append(OverheadByphaseSettinglist[swindexover].DeviceNumber)
			SWLine = 'New SwtControl.'+OverheadByphaseSettinglist[swindexover].DeviceNumber
			SWLine = SWLine + ' SwitchedObj=Line.'+OverheadByphaseSettinglist[swindexover].DeviceNumber
			
		Line = Line + ' switch=yes'	
		SWLine = SWLine + ' SwitchedTerm=1'
		
		if protectssw.NStatus == '1':
			print('Switch {} is open'.format(protectssw.SectionID))
			SWLine = SWLine + ' Normal=Open Action=Open'
		else:
			SWLine = SWLine + ' Normal=Close Action=Close'
		
		SWLine = SWLine + ' Delay=0'
		
		DSSProtecction.append(Line)
		DSSSwitchcontrol.append(SWLine)
		csvsw = protectssw.DeviceNumber + "," + OverheadByphaseSettinglist[swindexover].DeviceNumber+ "," +UndergroundlineSettinglist[swindexunder].DeviceNumber + "," + str(swindexover)
		swsectionindex = -1
		for i in range(len(Sectionlist)):
			if protectssw.SectionID == Sectionlist[i].SectionID:
				swsectionindex = i
		if swsectionindex == -1 :
			print('Switch section not found for {}'.format(switch))
		csvsw = csvsw + "," + Sectionlist[swsectionindex].Phase
		CabinateNum=''
		SwType='-1'
		#TODO: switchtype and cabinate number does not work.
		csvsw = csvsw + "," + SwType + "," + CabinateNum
		CSVSW.append(csvsw)
		
	CSVBR = ['Device Number, Location - Overhead, Location - Underhead, BR Location ']	
	for protectsbr in BreakerSettinglist:			
		breaker = protectsbr.SectionID
		
		
		brindexover = -1
		brindexunder = -1
		for i in range(len(OverheadByphaseSettinglist)):
			if breaker == OverheadByphaseSettinglist[i].SectionID:
				brindexover = i
		if brindexover == -1 :
			for i in range(len(UndergroundlineSettinglist)):
				if breaker == UndergroundlineSettinglist[i].SectionID:
					brindexunder = i
			if brindexunder == -1 :	
				print("no switch")
			else:
				if UndergroundlineSettinglist[brindexunder].DeviceNumber in switchlist:
					Line = "Edit Line."
				else:
					Line = "New Line."			
				Line = Line +UndergroundlineSettinglist[brindexunder].DeviceNumber
				switchlist.append(UndergroundlineSettinglist[brindexunder].DeviceNumber)
		else:
			if OverheadByphaseSettinglist[brindexover].DeviceNumber in switchlist:
				Line = "Edit Line."
			else:
				Line = "New Line."	
			Line = Line +OverheadByphaseSettinglist[brindexover].DeviceNumber
			switchlist.append(OverheadByphaseSettinglist[brindexover].DeviceNumber)
				
		Line = Line + ' switch=yes'	
		if protectsbr.NStatus == '1':
			print('Breaker {} is open'.format(protectsbr.SectionID))
			Line = Line + ' enabled=no'

		DSSProtecction.append(Line)
		csvbr = protectsbr.DeviceNumber + "," + OverheadByphaseSettinglist[brindexover].DeviceNumber+ "," +UndergroundlineSettinglist[brindexunder].DeviceNumber + "," + str(brindexover)
		CSVBR.append(csvbr)

	CSVFUSE  = ['Device Number, Location - Overhead, Location - Underhead, BR Location, Phase, Type, CabinateNum  ']
	for protectsfuse in FuseSettinglist:	
		Line = "New Line."
		fuse = protectsfuse.SectionID
		fsindexover = -1
		fsindexunder = -1
		for i in range(len(OverheadByphaseSettinglist)):
			if fuse == OverheadByphaseSettinglist[i].SectionID:
				fsindexover = i
		if fsindexover == -1 :
			for i in range(len(UndergroundlineSettinglist)):
				if fuse == UndergroundlineSettinglist[i].SectionID:
					fsindexunder = i
			if fsindexunder == -1 :	
				print("no switch")
			else:
				if UndergroundlineSettinglist[fsindexunder].DeviceNumber in switchlist:
					Line = "Edit Line."
				else:
					Line = "New Line."						
				Line = Line +UndergroundlineSettinglist[fsindexunder].DeviceNumber
				switchlist.append(UndergroundlineSettinglist[fsindexunder].DeviceNumber)
		else:
			if OverheadByphaseSettinglist[fsindexover].DeviceNumber in switchlist:
				Line = "Edit Line."
			else:
				Line = "New Line."			
			Line = Line +OverheadByphaseSettinglist[fsindexover].DeviceNumber
			switchlist.append(OverheadByphaseSettinglist[fsindexover].DeviceNumber)
				
		Line = Line + ' switch=yes'	
		if protectsfuse.NStatus == '1':
			print('Fuse {} is open'.format(protectsfuse.SectionID))
			Line = Line + ' enabled=no'
	
		DSSProtecction.append(Line)
		csvfuse = protectsfuse.SectionID + "," + OverheadByphaseSettinglist[fsindexover].DeviceNumber+ "," +UndergroundlineSettinglist[fsindexunder].DeviceNumber + "," + str(fsindexover)
		fusesectionindex = -1
		for i in range(len(Sectionlist)):
			if protectsfuse.SectionID == Sectionlist[i].SectionID:
				fusesectionindex = i
		if fusesectionindex == -1 :
			print('Switch section not found for {}'.format(fuse))
		csvfuse = csvfuse + "," + Sectionlist[fusesectionindex].Phase
		CabinateNum=''
		FsType='-1'
		#TODO: Fstype and cabinate number does not work.
		csvfuse = csvfuse + "," + FsType + "," + CabinateNum
		CSVFUSE.append(csvfuse)
		
	return DSSProtecction, DSSSwitchcontrol, switchlist, CSVSW, CSVBR, CSVFUSE

def ProperCableName(UndergroundlineSettinglist):
	CableNamelist = []
	CableSectionID = []
	for cable in UndergroundlineSettinglist:
		CableNamelist.append(cable.DeviceNumber)
		CableSectionID.append(cable.SectionID)
	return CableNamelist, CableSectionID

def FindProtection(SwitchSettinglist, BreakerSettinglist, FuseSettinglist):
	Isswitchlist = []
	for switch in SwitchSettinglist:
		if switch.SectionID not in Isswitchlist:
			Isswitchlist.append(switch.SectionID)
	for breaker in BreakerSettinglist:
		if breaker.SectionID not in Isswitchlist:
			Isswitchlist.append(breaker.SectionID)
	for fuse in FuseSettinglist:
		if fuse.SectionID not in Isswitchlist:
			Isswitchlist.append(fuse.SectionID)
	return Isswitchlist

def LineImpedances(csvname, UndergroundlineSettinglist, SwitchSettinglist, BreakerSettinglist, FuseSettinglist):
	CableNamelist, CableSectionID = ProperCableName(UndergroundlineSettinglist)
	Isswitchlist = FindProtection(SwitchSettinglist, BreakerSettinglist, FuseSettinglist)
	
	OpenDSSlist = []
	with open(csvname,'r') as ipfile:
		Lineset = ipfile.readlines()
		for i in range(0,len(Lineset)):
			Line = Lineset[i].rstrip()
			if Line.strip() == '':
				continue
			Line = Line.split(',')
			linesection = Line[1]
			devicenumindex = CableSectionID.index(linesection)
			if linesection in Isswitchlist:
				DSSLine = 'Edit'
			else:
				DSSLine = 'New'
			DSSLine = DSSLine+' Line.'+CableNamelist[devicenumindex]
			phaseword='-1'
			if Line[5] == 'ABC':
				phaseword='.1.2.3'
			elif Line[5] == 'A':
				phaseword='.1.0'
			elif Line[5] == 'B':
				phaseword='.2.0'
			elif Line[5] == 'C':
				phaseword='.3.0'
			else:
				print('phase not found')
			DSSLine = DSSLine + ' bus1='+Line[6].replace(".","_")+phaseword
			DSSLine = DSSLine + ' bus2='+Line[7].replace(".","_")+phaseword
			DSSLine = DSSLine + ' length='+Line[8]
			DSSLine = DSSLine + ' units=m'
			DSSLine = DSSLine + ' phases='+str(len(Line[5]))
			DSSLine = DSSLine + ' phases='+str(len(Line[5]))
			DSSLine = DSSLine + ' LineCode='+Line[2].replace(".","_")+"_"+str(len(Line[5]))+"_"+Line[9]+"Cond"
			DSSLine = DSSLine + ' NormAmps='+Line[13]
			DSSLine = DSSLine + '\n'
			OpenDSSlist.append(DSSLine)
	
	return OpenDSSlist
	
def LineCodes(csvname, UndergroundlineSettinglist, SwitchSettinglist, BreakerSettinglist, FuseSettinglist):
	CableNamelist, CableSectionID = ProperCableName(UndergroundlineSettinglist)
	Isswitchlist = FindProtection(SwitchSettinglist, BreakerSettinglist, FuseSettinglist)
	
	DSSLineCodes = []
	CSVLineCodes = ['Cable Type, Phases, Number of Conductors, R1[ohm/m], R0[ohm/m], X1[ohm/m], X0[ohm/m], B1[uS/m], B0[uS/m]']
	
	with open(csvname,'r') as ipfile:
		Lineset = ipfile.readlines()
		for i in range(0,len(Lineset)):
			Line = Lineset[i].rstrip()
			if Line.strip() == '':
				continue
			Line = Line.split(',')
			linesection = Line[1]
			devicenumindex = CableSectionID.index(linesection)
			
			DSSLine = 'New LineCode.'+Line[2].replace(".","_")+"_"+str(len(Line[5]))+"_"+Line[9]+"Cond"
			DSSLine = DSSLine + ' NPhases='+str(len(Line[5]))

			if float(Line[21]) == 0:
				DSSLine = DSSLine + ' R1=1.00E-07'
			else:
				DSSLine = DSSLine + ' R1='+Line[21]
			if float(Line[24]) == 0:
				DSSLine = DSSLine + ' R0=1.00E-07'
			else:
				DSSLine = DSSLine + ' R0='+Line[24]

			if float(Line[22])==0:
				DSSLine = DSSLine + ' X1='+'1.00E-07'
			else:
				DSSLine = DSSLine + ' X1='+Line[22]
			DSSLine = DSSLine + ' X0='+Line[25]
			DSSLine = DSSLine + ' B1='+Line[23]
			DSSLine = DSSLine + ' B0='+Line[26] 
			
			DSSLine = DSSLine + ' Units=m'
			
			if DSSLine in DSSLineCodes:
				continue
			else:
				DSSLineCodes.append(DSSLine)
	
	return DSSLineCodes	
	

def convert_buses(Nodelist, IntermediateNodeslist):
	DSSBuscoords = []
	for Busnode in Nodelist:
		Line = Busnode.NodeID.replace(".","_")
		Line = Line + ', '+Busnode.CoordX
		Line = Line + ', '+Busnode.CoordY
		DSSBuscoords.append(Line)	
	return DSSBuscoords

#write functions
def writefileopendss (circuitName, codeList, openfile) :
	with open(circuitName,'w') as f:
		if len(codeList) > 0 :
			for s in codeList :
				f.write(s+'\n')
				if (openfile == 1):
					print(s)
		else :
			print('Empty file {}'.format(circuitName))
	return

if __name__ == "__main__":
	print('Please do not run this file, run the main file!')
