#This file writes OpenDSS circuit from CYME reader.
#Written for ASU by Karen Montano, Sushrut Thakar

# This version contains the script to generate csv files of the system under study
# This version contains the code to generate the PV generators in the system

###############################################################################################################
#Usage
#Read from cyme version 8.2



###############################################################################################################
#imports following modules, make sure to install them.
#from collections import namedtuple
import os
import Cyme_Reader_DISMOTT as reader
import OpenDSS_Writer_DISMOTT as writer
#import math
#import numpy as np
#import cmath

##############################################################################################################
#main script
if __name__ == "__main__":
	print('Converting CYME to OpenDSS')	
	#inputs
	#navigate folder structure here
	casename = 'Casename' #create this folder in the same location as input '.txt' files
	equipmentfile = 'equipment.txt'
	loadfile = 'load.txt'
	networkfile = 'network.txt'
	
		
	#read cyme database files
	Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, Switchlist, Breakerlist, Fuselist, Substationlist, Transformerlist, Electronicconvertergeneratorlist = reader.read_equipment(equipmentfile)
	CustomerClasslist, Loadslist, CustomerLoadslist, LoadModelInformationlist = reader.read_load(loadfile)
	Nodelist, HeadNodeslist, Sourcelist, SourceEquivalentlist, LoadEquivalentlist, DeviceStagelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist, Feederlist, TransformerSettinglist, SwitchSettinglist, BreakerSettinglist, FuseSettinglist, ShuntCapacitorSettinglist, IntermediateNodeslist, CapacitorExtltdlist, OvercurrentRelayInstrumentlist, CurrentTransformerInstrumentlist, DeviceUddlist, Electronicconvertergeneratorsettinglist, Converterlist,  Convertercontrolsettinglist, Longtermdynamicscurveextlist, Dggenerationmodellist, Controlleddevicelist = reader.read_network(networkfile)
	#convert files
	
	#write opendss files
	#change folder
	#os.makedirs(casename)
	try:
		os.chdir(casename)
	except FileNotFoundError:
		print('The folder with the casename {} was not present, so created it.'.format(casename))
		os.makedirs(casename)
		os.chdir(casename)
		
	DSSMaster = writer.convert_master(Substationlist, HeadNodeslist, Sourcelist, SourceEquivalentlist, Feederlist, Transformerlist, casename)
	writer.writefileopendss('Master.dss', DSSMaster, 0)
	
	DSSProtecction, DSSSwitchcontrol, switchlist, CSVSW, CSVBR, CSVFUSE = writer.convert_protection(Switchlist, Breakerlist, Fuselist, SwitchSettinglist, BreakerSettinglist, FuseSettinglist, OvercurrentRelayInstrumentlist, CurrentTransformerInstrumentlist,OverheadByphaseSettinglist,UndergroundlineSettinglist, Sectionlist)
	writer.writefileopendss('protection.dss', DSSProtecction, 0)
	writer.writefileopendss('switchcontrol.dss', DSSSwitchcontrol, 0)
	writer.writefileopendss('Switch.csv', CSVSW, 0)
	writer.writefileopendss('Breaker.csv', CSVBR, 0)
	writer.writefileopendss('Fuses.csv', CSVFUSE, 0)
	
	DSSLinesOver,CSVLinesOver = writer.convert_lineover(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist, switchlist)
	writer.writefileopendss('linesover.dss', DSSLinesOver, 0)
	writer.writefileopendss('LinesOver.csv', CSVLinesOver, 0)
	
	DSSWiredata = writer.convert_wiredata(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist)
	writer.writefileopendss('wiredata.dss', DSSWiredata, 0)
	
	DSSLinegeometryOver = writer.convert_linegeometryover(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist)
	writer.writefileopendss('linegeometryover.dss', DSSLinegeometryOver, 0)
	
	DSSLinespacing = writer.convert_linespacing(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist)
	writer.writefileopendss('linespacing.dss', DSSLinespacing, 0)
		
	# Definitions: Data from Cymedist for cable and wire definitions
	# Impedances: lines impedances exported from CYMEDIST

	LineDefinitionBasedOn = 'Definitions'
	csvname = 'NameOfTheCSVFile.csv' #If using direct impedances, please use the CYME report option to export cable impedances to a csv file, and put it in the same folder (casename) [please read the readme.]
	
	if LineDefinitionBasedOn == 'Definitions':	
	
		DSSLinesUnder,CSVLinesUnder = writer.convert_lineunder(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist, switchlist)
		writer.writefileopendss('linesunder.dss', DSSLinesUnder, 0)
		writer.writefileopendss('LinesUnder.csv', CSVLinesUnder, 0)
		
		DSSCablemodel = writer.convert_cablemodel(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist)
		writer.writefileopendss('cablemodel.dss', DSSCablemodel, 0)
		
		DSSLinegeometryUnder = writer.convert_linegeometryunder(Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist)
		writer.writefileopendss('linegeometryunder.dss', DSSLinegeometryUnder, 0)
	
	elif LineDefinitionBasedOn == 'Impedances':
	
		DSSLinesUnder = writer.LineImpedances(csvname, UndergroundlineSettinglist, SwitchSettinglist, BreakerSettinglist, FuseSettinglist)
		writer.writefileopendss('linesunder.dss', DSSLinesUnder, 0)
		writer.writefileopendss('cablemodel.dss', [], 0)
		writer.writefileopendss('linegeometryunder.dss', [], 0)
		
		DSSLineCodes = writer.LineCodes(csvname, UndergroundlineSettinglist, SwitchSettinglist, BreakerSettinglist, FuseSettinglist)
		writer.writefileopendss('linecodes.dss', DSSLineCodes, 0)
		
	
	DSSTransformerscodes, CSVTransformers = writer.convert_transformercodes(Transformerlist, TransformerSettinglist)
	writer.writefileopendss('transformerscodes.dss', DSSTransformerscodes, 0)
	writer.writefileopendss('Transformers.csv', CSVTransformers, 0)
	
	DSSTransformers, CSVTransformers2 = writer.convert_transformer(Transformerlist, TransformerSettinglist, Sectionlist)
	writer.writefileopendss('transformers.dss', DSSTransformers, 0)
	writer.writefileopendss('Transformers2.csv', CSVTransformers2, 0)
	
	DSSLoads, CSVLoads = writer.convert_load(CustomerClasslist, Loadslist, CustomerLoadslist, LoadModelInformationlist, LoadEquivalentlist, Sectionlist, Transformerlist, TransformerSettinglist)
	writer.writefileopendss('loads.dss', DSSLoads, 0)
	writer.writefileopendss('Load.csv', CSVLoads, 0)
	
	DSSGenerators, CSVPVs = writer.convert_generators(Sectionlist, Electronicconvertergeneratorlist, Electronicconvertergeneratorsettinglist, Converterlist, Convertercontrolsettinglist, Longtermdynamicscurveextlist, Dggenerationmodellist, Controlleddevicelist)
	writer.writefileopendss('generators.dss', DSSGenerators, 0)
	writer.writefileopendss('PVs.csv', CSVPVs, 0)
	
	DSSCapacitors, CSVCapacitors = writer.convert_capacitors(ShuntCapacitorSettinglist, CapacitorExtltdlist, Sectionlist)
	writer.writefileopendss('capacitors.dss', DSSCapacitors, 0)
	writer.writefileopendss('Capacitors.csv', CSVCapacitors, 0)
	
	DSSBuscoords = writer.convert_buses(Nodelist, IntermediateNodeslist)
	writer.writefileopendss('buscoords.dss', DSSBuscoords, 0)
	
