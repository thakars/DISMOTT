#This file reads cyme circuits version 8.X
#Written for ASU by Karen Montano, Sushrut Thakar
###############################################################################################################
#Usage
#Written for cyme version 8.2
#Export from the cyme database: network.txt, equipment.txt and load.txt. These files are read in this script.
# This version reads the PV databases
# This version does not read batteries
# SI units only. imperial units not implemented

#import the following modules, make sure to install them.
from collections import namedtuple

###############################################################################################################
#function definitions:

#read functions
def read_equipment(filename):
	#named tuple definitions
	Cable = namedtuple('Cable',['ID','R1','R0','X1','X0','B1','B0','Amps','Amps_1','Amps_2','Amps_3','Amps_4','WithstandRating','FailRate','TmpFailRate','MajorRepairTime','MinorRepairTime','MajorFailureProportion','RatedLevel','PositiveSequenceShuntConductance','ZeroSequenceShuntConductance','LockImpedance','Manufacturer','Standard','CableType','NumberOfGroundingConductors','ArmorOuterDiameter','OverallDiameter','ConcentricNeutralBeforeSheath','UserDefinedImpedances','Frequency','Temperature','ImpedancesNote','Favorite','Flags','Comments'])
	Cablelist = []
	CableConcentricNeutral = namedtuple('CableConcentricNeutral',['ID','CableConcentricNeutralLocation','MaterialID','LayerPosition','Thickness','ConcentricNeutralsType','NumberOfWires','StrapWidth','LayLength'])
	CableConcentricNeutrallist = []
	CableInsulation = namedtuple('CableInsulation',['ID','CableInsulationLocation','InsulationMaterialID','Thickness'])
	CableInsulationlist = []
	CableConductor = namedtuple('CableConductor',['ID','CableConductorLocation','MaterialID','CableSize','Size_mm2','Diameter','ConstructionType','NumberOfStrands'])
	CableConductorlist = []
	Conductor = namedtuple('Conductor',['ID','Diameter','GMR','R25','R50','Amps','Amps_1','Amps_2','Amps_3','Amps_4','WithstandRating','FailRate','TmpFailRate','MajorRepairTime','MinorRepairTime','MajorFailureProportion','CodeWord','ConstructionType','FirstResistanceDC','SecondResistanceDC','MaterialId','AWGSize','SizeUnit','Size_mm2','OutsideArea','NumberOfStrands','TemperatureAC1','TemperatureAC2','TemperatureDC1','TemperatureDC2','Frequency','Favorite','Flags','Comments'])
	Conductorlist = []
	SpacingTableForLine = namedtuple('SpacingTableForLine',['ID','GMDPh_Ph','GMDPh_N','AvgPhCondHeight','AvgNeutralHeight','PosOfCond1_X','PosOfCond1_Y','PosOfCond2_X','PosOfCond2_Y','PosOfCond3_X','PosOfCond3_Y','PosOfNeutralCond_X','PosOfNeutralCond_Y','PosOfNeutralCond_N2_X','PosOfNeutralCond_N2_Y','BundleDistance','NBPhasesPerCircuit','NBConductorsPerPhase','NBNeutrals','TowerType','DistanceA','DistanceB','DistanceC','DistanceD','DistanceE','DistanceF','ConductorStatusN1','ConductorStatusN2','FootingResistanceN1','FootingResistanceN2','TowerSpanN1','TowerSpanN2','Favorite','Flags','Comments'])
	SpacingTableForLinelist = []
	Switch = namedtuple('Switch',['ID','Amps','Amps_1','Amps_2','Amps_3','Amps_4','KVLL','Reversible','FailRate','TmpFailRate','MajorRepairTime','MinorRepairTime','MajorFailureProportion','StuckProbability','SwitchTime','SymbolOpenID','SymbolCloseID','SinglePhaseLocking','RemoteControlled','Automated','Favorite','Flags','Comments'])
	Switchlist = []
	Breaker = namedtuple('Breaker',['ID','Amps','Amps_1','Amps_2','Amps_3','Amps_4','KVLL','Reversible','InterruptingRating','FailRate','TmpFailRate','MajorRepairTime','MinorRepairTime','MajorFailureProportion','StuckProbability','SwitchTime','SymbolOpenID','SymbolCloseID','SinglePhaseLocking','SinglePhaseTripping','RemoteControlled','Automated','Standard','Manufacturer','Model','ANSIMaxRatedVoltage','ANSIRatedRangeKFactor','ANSIMaxSymetricalRMS','ANSIClosingLatchingRMS','ANSIClosingLatchingCrest','IECMakingCurrent','InterruptingTime','Favorite','Flags','Comments'])
	Breakerlist = []
	Fuse = namedtuple('Fuse',['ID','Amps','Amps_1','Amps_2','Amps_3','Amps_4','KVLL','Reversible','InterruptingRating','TestCircuitPF','VoltageClassification','Standard','FailRate','TmpFailRate','MajorRepairTime','MinorRepairTime','MajorFailureProportion','StuckProbability','SwitchTime','SymbolOpenID','SymbolCloseID','SinglePhaseLocking','Favorite','Flags','Comments','Manufacturer','Model','TCCRating'])
	Fuselist = []
	Substation = namedtuple('Substation',['ID','MVA','MVA_1','MVA_2','MVA_3','MVA_4','KVLL','KVLLdesired','FirstLevelR1','FirstLevelX1','FirstLevelR0','FirstLevelX0','FirstLevelR2','FirstLevelX2','SecondLevelR1','SecondLevelX1','SecondLevelR0','SecondLevelX0','SecondLevelR2','SecondLevelX2','Connection','PhaseAngle','HarmonicEnveloppe','BackgroundHarmonicVoltage','BaseMVA','ImpedanceUnit','PrimaryEquivalentType','SubEqVal1','SubEqVal2','SubEqVal3','SubEqVal4','SubPrimaryLLVoltage','SecondaryFaultReactance','TxfoConnection','BranchID_1','PrimProtDevID_1','PrimProtDevNum_1','TransformerID_1','TransformerNum_1','SubXs_1','SecProtDevID_1','SecProtDevNum_1','BranchStatus_1','BranchID_2','PrimProtDevID_2','PrimProtDevNum_2','TransformerID_2','TransformerNum_2','SubXs_2','SecProtDevID_2','SecProtDevNum_2','BranchStatus_2','BranchID_3','PrimProtDevID_3','PrimProtDevNum_3','TransformerID_3','TransformerNum_3','SubXs_3','SecProtDevID_3','SecProtDevNum_3','BranchStatus_3','BranchID_4','PrimProtDevID_4','PrimProtDevNum_4','TransformerID_4','TransformerNum_4','SubXs_4','SecProtDevID_4','SecProtDevNum_4','BranchStatus_4','BranchID_5','PrimProtDevID_5','PrimProtDevNum_5','TransformerID_5','TransformerNum_5','SubXs_5','SecProtDevID_5','SecProtDevNum_5','BranchStatus_5','SecondLevelPrimaryEquivalentType','SecondLevelSubEqVal1','SecondLevelSubEqVal2','SecondLevelSubEqVal3','SecondLevelSubEqVal4','SecondLevelSubPrimaryLLVoltage','SecondLevelSecondaryFaultReactance','SecondLevelTxfoConnection','SecondLevelBranchID_1','SecondLevelPrimProtDevID_1','SecondLevelPrimProtDevNum_1','SecondLevelTransformerID_1','SecondLevelTransformerNum_1','SecondLevelSubXs_1','SecondLevelSecProtDevID_1','SecondLevelSecProtDevNum_1','SecondLevelBranchStatus_1','SecondLevelBranchID_2','SecondLevelPrimProtDevID_2','SecondLevelPrimProtDevNum_2','SecondLevelTransformerID_2','SecondLevelTransformerNum_2','SecondLevelSubXs_2','SecondLevelSecProtDevID_2','SecondLevelSecProtDevNum_2','SecondLevelBranchStatus_2','SecondLevelBranchID_3','SecondLevelPrimProtDevID_3','SecondLevelPrimProtDevNum_3','SecondLevelTransformerID_3','SecondLevelTransformerNum_3','SecondLevelSubXs_3','SecondLevelSecProtDevID_3','SecondLevelSecProtDevNum_3','SecondLevelBranchStatus_3','SecondLevelBranchID_4','SecondLevelPrimProtDevID_4','SecondLevelPrimProtDevNum_4','SecondLevelTransformerID_4','SecondLevelTransformerNum_4','SecondLevelSubXs_4','SecondLevelSecProtDevID_4','SecondLevelSecProtDevNum_4','SecondLevelBranchStatus_4','SecondLevelBranchID_5','SecondLevelPrimProtDevID_5','SecondLevelPrimProtDevNum_5','SecondLevelTransformerID_5','SecondLevelTransformerNum_5','SecondLevelSubXs_5','SecondLevelSecProtDevID_5','SecondLevelSecProtDevNum_5','SecondLevelBranchStatus_5','FailRate','TmpFailRate','MajorRepairTime','MinorRepairTime','MajorFailureProportion','SymbolID','Favorite','Flags','Comments'])
	Substationlist = []
	Transformer = namedtuple('Transformer',['ID','Type','WindingType','KVA','VoltageUnit','KVLLprim','KVLLsec','Z1','Z0','Z0PrimSec','Z0PrimMag','Z0SecMag','XR','XR0','XR0PrimSec','XR0PrimMag','XR0SecMag','MagnetizingCurrent','Conn','Rg_prim','Xg_prim','Rg_sec','Xg_sec','IsLTC','Taps','LowerBandwidth','UpperBandwidth','MinReg_Range','MaxReg_Range','Reversible','SelfCooledKVA','SelfCooledKVA_2','SelfCooledKVA_3','SelfCooledKVA_4','NoLoadLosses','FailRate','TmpFailRate','MajorRepairTime','MinorRepairTime','MajorFailureProportion','SymbolID','PhaseShiftType','InsulationType','Favorite','Flags','Comments'])
	Transformerlist = []
	Electronicconvertergenerator = namedtuple('Electronicconvertergenerator',['ID','KVA','KVLL','ActiveGeneration','PF','FaultContribution','Converter','SymbolID','Favorite','Flags','Comments'])
	Electronicconvertergeneratorlist = []
	#read the file
	with open(filename,'r') as inputfile:
		Lineset = inputfile.readlines()
		#now we will go through the file, line by line
		linenum = 0
		#confirm that CYME version is the same
		while not Lineset[linenum].startswith('CYME_VERSION'):
			linenum = linenum + 1
		version_cyme = float(Lineset[linenum].split('=')[1])
		if version_cyme != 8.2:
			print('CYME version not matching with 8.2. This code may not work')
		#SI/imperial units
		while not Lineset[linenum].startswith('['):
			linenum = linenum + 1
			
		#SI units only. imperial units not implemented
		linenum = linenum + 1
		
		#cable
		while not Lineset[linenum].startswith('[CABLE]') and not linenum <= (len(Lineset)-1):
			linenum = linenum + 1
		#print(Lineset[linenum]+'iss')
		if	linenum < (len(Lineset)-1):	
			linenum = linenum + 3#[CABLE] and FORMAT_CABLE
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Cable(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35])
				Cablelist.append(elem)
				linenum = linenum + 1
			
		linenum = 0
		
		#CABLE CONCENTRIC NEUTRAL
		while not Lineset[linenum].startswith('[CABLE CONCENTRIC NEUTRAL]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			
		if	linenum < (len(Lineset)-1):	
			linenum = linenum + 2#[CABLE CONCENTRIC NEUTRAL] and FORMAT_ CABLE CONCENTRIC NEUTRAL
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = CableConcentricNeutral(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8])
				CableConcentricNeutrallist.append(elem)
				linenum = linenum + 1
			
		linenum = 0
		
		#CABLE INSULATION
		while not Lineset[linenum].startswith('[CABLE INSULATION]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):		
			linenum = linenum + 2#[CABLE INSULATION] and FORMAT_ CABLE INSULATION
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = CableInsulation(line[0],line[1],line[2],line[3])
				CableInsulationlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#CABLE CONDUCTOR
		while not Lineset[linenum].startswith('[CABLE CONDUCTOR]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[CABLE CONDUCTOR] and FORMAT_ CABLE CONDUCTOR
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = CableConductor(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7])
				CableConductorlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#CONDUCTOR
		while not Lineset[linenum].startswith('[CONDUCTOR]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[CONDUCTOR] and FORMAT_ CONDUCTOR
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Conductor(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33])
				Conductorlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#SPACING TABLE FOR LINE
		while not Lineset[linenum].startswith('[SPACING TABLE FOR LINE]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[SPACING TABLE FOR LINE] and FORMAT_ SPACING TABLE FOR LINE
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = SpacingTableForLine(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34])
				SpacingTableForLinelist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#ELECTRONIC CONVERTER GENERATOR
		while not Lineset[linenum].startswith('[ELECTRONIC CONVERTER GENERATOR]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Electronicconvertergenerator] and FORMAT_ Electronicconvertergenerator
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Electronicconvertergenerator(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10])
				Electronicconvertergeneratorlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#SWITCH
		while not Lineset[linenum].startswith('[SWITCH]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[SWITCH] and FORMAT_ SWITCH
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Switch(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22])
				Switchlist.append(elem)
				linenum = linenum + 1
		linenum = 0
		
		#BREAKER
		while not Lineset[linenum].startswith('[BREAKER]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[BREAKER] and FORMAT_ BREAKER
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Breaker(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34])
				Breakerlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#FUSE
		while not Lineset[linenum].startswith('[FUSE]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[FUSE] and FORMAT_ FUSE
			while not len(Lineset[linenum].strip()) == 0:#read cable data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Fuse(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27])
				Fuselist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#SUBSTATION
		while not Lineset[linenum].startswith('[SUBSTATION]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Substation] and FORMAT_ Substation
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Substation(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38],line[39],line[40],line[41],line[42],line[43],line[44],line[45],line[46],line[47],line[48],line[49],line[50],line[51],line[52],line[53],line[54],line[55],line[56],line[57],line[58],line[59],line[60],line[61],line[62],line[63],line[64],line[65],line[66],line[67],line[68],line[69],line[70],line[71],line[72],line[73],line[74],line[75],line[76],line[77],line[78],line[79],line[80],line[81],line[82],line[83],line[84],line[85],line[86],line[87],line[88],line[89],line[90],line[91],line[92],line[93],line[94],line[95],line[96],line[97],line[98],line[99],line[100],line[101],line[102],line[103],line[104],line[105],line[106],line[107],line[108],line[109],line[110],line[111],line[112],line[113],line[114],line[115],line[116],line[117],line[118],line[119],line[120],line[121],line[122],line[123],line[124],line[125],line[126],line[127],line[128],line[129],line[130],line[131],line[132],line[133],line[134],line[135],line[136],line[137],line[138],line[139],line[140])
				Substationlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#TRANSFORMER
		while not Lineset[linenum].startswith('[TRANSFORMER]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Transformer] and FORMAT_ Transformer
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Transformer(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38],line[39],line[40],line[41],line[42],line[43],line[44],line[45])
				Transformerlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
	return Cablelist, CableConcentricNeutrallist, CableInsulationlist, CableConductorlist, Conductorlist, SpacingTableForLinelist, Switchlist, Breakerlist, Fuselist, Substationlist, Transformerlist, Electronicconvertergeneratorlist
   
def read_load(filename):
	#named tuple definitions
	CustomerClass = namedtuple('CustomerClass',['ID','DCCustomerType','Description','Color','SymbolID','ConstantPower','ConstantCurrent','ConstantImpedance','UtilizationFactor','PowerFactor','MeteredLoads','NonMeteredLoads','LoadFactor','FrequencySensitivityP','FrequencySensitivityQ','EnableHarmonic','HarmonicCurrentSourceInPercent','IsExponentialModel','ConstantImpedanceZP','ConstantImpedanceZQ','ConstantCurrentIP','ConstantCurrentIQ','ConstantPowerPP','ConstantPowerPQ','ExponentialModelP','ExponentialModelQ','LoadFlowVoltagePercentOfNominal','LossesPerCustomer','ConnectedCenterTap1N','ConnectedCenterTap2N','AdjustmentSettings','PowerCurveModel','PowerCurveModelId'])
	CustomerClasslist = []
	Loads = namedtuple('Loads',['SectionID','DeviceNumber','DeviceStage','Flags','LoadType','Connection','Location'])
	Loadslist = []
	CustomerLoads = namedtuple('CustomerLoads',['SectionID','DeviceNumber','LoadType','CustomerNumber','CustomerType','ConnectionStatus','LockDuringLoadAllocation','Year','LoadModelID','NormalPriority','EmergencyPriority','ValueType','LoadPhase','Value1','Value2','ConnectedKVA','KWH','NumberOfCustomer','CenterTapPercent','CenterTapPercent2','LoadValue1N1','LoadValue1N2','LoadValue2N1','LoadValue2N2'])
	CustomerLoadslist = []
	LoadModelInformation = namedtuple('LoadModelInformation',['ID','Name'])
	LoadModelInformationlist = []
	#read the file
	with open(filename,'r') as inputfile:
		Lineset = inputfile.readlines()
		#now we will go through the file, line by line. Skip the initial lines.
		linenum = 7

		#CUSTOMER CLASS
		while not Lineset[linenum].startswith('[CUSTOMER CLASS]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Customerclass] and FORMAT_ Customerclass
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = CustomerClass(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32])
				CustomerClasslist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#LOADS
		while not Lineset[linenum].startswith('[LOADS]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Loads] and FORMAT_ Loads
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Loads(line[0],line[1],line[2],line[3],line[4],line[5],line[6])
				Loadslist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#CUSTOMER LOADS
		while not Lineset[linenum].startswith('[CUSTOMER LOADS]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Customerloads] and FORMAT_ Customerloads
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = CustomerLoads(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23])
				CustomerLoadslist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#LOAD MODEL INFORMATION
		while not Lineset[linenum].startswith('[LOAD MODEL INFORMATION]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			if linenum == len(Lineset):
				linenum = 0
				break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Loadmodelinformation] and FORMAT_ Loadmodelinformation
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = LoadModelInformation(line[0],line[1])
				LoadModelInformationlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
	return CustomerClasslist, Loadslist, CustomerLoadslist, LoadModelInformationlist

def read_network(filename):
	#named tuple definitions
	Node = namedtuple('Node',['NodeID','CoordX','CoordY','TagText','TagProperties','TagDeltaX','TagDeltaY','TagAngle','TagAlignment','TagBorder','TagBackground','TagTextColor','TagBorderColor','TagBackgroundColor','TagLocation','TagFont','TagTextSize','TagOffset','ZoneID','ExposedCircuitType','BusGap','WorkingDistance','UseUserDefinedFaultCurrent','UserDefinedFaultCurrent','OpeningTimeMode','UserDefinedOpeningTime','EnclosureWidth','EnclosureHeight','EnclosureDepth','CoefficientA','CoefficientK','UserDefinedTimeConstant','TimeConstant','OverrideLFVoltageLimit','HighVoltageLimit','LowVoltageLimit','LoadSheddingActive','MaximumLoadShed','ShedLoadCost','UserDefinedBaseVoltage','Installation','RatedVoltage','RatedCurrent','ANSISymCurrent','ANSIAsymCurrent','PeakCurrent','Standard','TestCircuitPowerFactor'])
	Nodelist = []
	HeadNodes = namedtuple('HeadNodes',['NodeID','NetworkID','ConnectorIndex','StructureID','HarmonicEnveloppe','EquivalentSourceConfiguration','EquivalentSourceSinglePhaseCT','EquivSourceCenterTapPhase','BackgroundHarmonicVoltage'])
	HeadNodeslist = []
	Source = namedtuple('Source',['SourceID','DeviceNumber','NodeID','NetworkID','OperatingVoltageA','OperatingVoltageB','OperatingVoltageC','UseSecondLevelImpedance','SinglePhaseCenterTap','CenterTapPhase'])
	Sourcelist = []
	SourceEquivalent = namedtuple('SourceEquivalent',['NodeID','LoadModelName','Voltage','OperatingAngle1','OperatingAngle2','OperatingAngle3','UseSecondLevelImpedance','FirstLevelR1','FirstLevelX1','FirstLevelR0','FirstLevelX0','FirstLevelR2','FirstLevelX2','SecondLevelR1','SecondLevelX1','SecondLevelR0','SecondLevelX0','SecondLevelR2','SecondLevelX2','OperatingVoltage1','OperatingVoltage2','OperatingVoltage3','BaseMVA','ImpedanceUnit'])
	SourceEquivalentlist = []
	LoadEquivalent = namedtuple('LoadEquivalent',['NodeID','LoadModelName','Format','Value1A','Value1B','Value1C','Value2A','Value2B','Value2C','ValueSinglePhaseCT11','ValueSinglePhaseCT12','ValueSinglePhaseCT21','ValueSinglePhaseCT22'])
	LoadEquivalentlist = []
	DeviceStage = namedtuple('DeviceStage',['DeviceStageName','DeviceStageID','Description','Color','DefaultStage'])
	DeviceStagelist = []
	OverheadByphaseSetting = namedtuple('OverheadByphaseSetting',['SectionID','DeviceNumber','DeviceStage','Flags','InitFromEquipFlags','CondID_A','CondID_B','CondID_C','CondID_N1','CondID_N2','SpacingID','Length','ConnectionStatus','NominalRatingA','NominalRatingB','NominalRatingC','FirstRatingA','FirstRatingB','FirstRatingC','SecondRatingA','SecondRatingB','SecondRatingC','ThirdRatingA','ThirdRatingB','ThirdRatingC','FourthRatingA','FourthRatingB','FourthRatingC','AmpacityDeratingFactor','ConductorPosition','CoordX','CoordY','HarmonicModel','TCCRepositoryID','EarthResistivity','FlowConstraintActive','FlowConstraintUnit','MaximumFlow'])
	OverheadByphaseSettinglist = []
	UndergroundlineSetting = namedtuple('UndergroundlineSetting',['SectionID','DeviceNumber','DeviceStage','Flags','InitFromEquipFlags','LineCableID','Length','NumberOfCableInParallel','CTConnection','Amps','Amps_1','Amps_2','Amps_3','Amps_4','ConnectionStatus','CoordX','CoordY','HarmonicModel','TCCRepositoryID','EarthResistivity','OperatingTemperature','Height','DistanceBetweenConductors','BondingType','CableConfiguration','DuctMaterial','Bundled','Neutral1Type','Neutral2Type','Neutral3Type','Neutral1ID','Neutral2ID','Neutral3ID','AmpacityDeratingFactor','FlowConstraintActive','FlowConstraintUnit','MaximumFlow'])
	UndergroundlineSettinglist = []
	Section = namedtuple('Section',['SectionID','FromNodeID','FromNodeIndex','ToNodeID','ToNodeIndex','Phase','ZoneID','SubNetworkId','EnvironmentID'])
	Sectionlist = []
	Feeder = namedtuple('Feeder',['NetworkID','HeadNodeID','CoordSet','Year','Description','Color','LoadFactor','LossLoadFactorK','Group1','Group2','Group3','North','South','East','West','AreaFilter','TagText','TagProperties','TagDeltaX','TagDeltaY','TagAngle','TagAlignment','TagBorder','TagBackground','TagTextColor','TagBorderColor','TagBackgroundColor','TagLocation','TagFont','TagTextSize','TagOffset','Version','EnvironmentID'])
	Feederlist = []
	TransformerSetting = namedtuple('TransformerSetting',['SectionID','Location','EqID','DeviceNumber','DeviceStage','Flags','InitFromEquipFlags','CoordX','CoordY','Conn','PrimTap','SecondaryTap','RgPrim','XgPrim','RgSec','XgSec','ODPrimPh','PrimaryBaseVoltage','SecondaryBaseVoltage','FromNodeID','SettingOption','SetPoint','ControlType','LowerBandWidth','UpperBandWidth','TapLocation','InitialTapPosition','InitialTapPositionMode','Tap','MaxBuck','MaxBoost','CT','PT','Rset','Xset','FirstHouseHigh','FirstHouseLow','PhaseON','AtSectionID','MasterID','FaultIndicator','PhaseShiftType','GammaPhaseShift','CTPhase','PrimaryCornerGroundedPhase','SecondaryCornerGroundedPhase','ConnectionStatus','TCCRepositoryID','Reversible'])
	TransformerSettinglist = []
	SwitchSetting = namedtuple('SwitchSetting',['SectionID','Location','EqID','DeviceNumber','DeviceStage','Flags','InitFromEquipFlags','CoordX','CoordY','ClosedPhase','Locked','RC','NStatus','PhPickup','GrdPickup','Alternate','PhAltPickup','GrdAltPickup','FromNodeID','FaultIndicator','Automated','SensorMode','Strategic','RestorationMode','ConnectionStatus','ByPassOnRestoration','Reversible'])
	SwitchSettinglist = []
	BreakerSetting = namedtuple('BreakerSetting',['SectionID','Location','EqID','DeviceNumber','DeviceStage','Flags','InitFromEquipFlags','CoordX','CoordY','ClosedPhase','Locked','RC','NStatus','TCCID','PhPickup','GrdPickup','Alternate','PhAltPickup','GrdAltPickup','FromNodeID','EnableReclosing','FaultIndicator','EnableFuseSaving','MinRatedCurrentForFuseSaving','Automated','SensorMode','Strategic','RestorationMode','ConnectionStatus','ByPassOnRestoration','Speed','SeqOpFirstPhase','SeqOpFirstGround','SeqOpLockoutPhase','SeqOpLockoutGround','SeqResetTime','SeqReclosingTime1','SeqReclosingTime2','SeqReclosingTime3','Reversible'])
	BreakerSettinglist = []
	FuseSetting = namedtuple('FuseSetting',['SectionID','Location','EqID','DeviceNumber','DeviceStage','Flags','InitFromEquipFlags','CoordX','CoordY','ClosedPhase','Locked','RC','NStatus','TCCID','PhPickup','GrdPickup','Alternate','PhAltPickup','GrdAltPickup','FromNodeID','FaultIndicator','Strategic','RestorationMode','ConnectionStatus','TCCRepositoryID','ByPassOnRestoration','Reversible'])
	FuseSettinglist = []
	ShuntCapacitorSetting = namedtuple('ShuntCapacitorSetting',['SectionID','DeviceNumber','DeviceStage','Flags','InitFromEquipFlags','Location','Connection','FixedKVARA','FixedKVARB','FixedKVARC','FixedLossesA','FixedLossesB','FixedLossesC','SwitchedKVARA','SwitchedKVARB','SwitchedKVARC','SwitchedLossesA','SwitchedLossesB','SwitchedLossesC','ByPhase','VoltageOverride','VoltageOverrideOn','VoltageOverrideOff','VoltageOverrideDeadband','KV','Control','OnValueA','OnValueB','OnValueC','OffValueA','OffValueB','OffValueC','SwitchingMode','InitiallyClosedPhase','CurrentClosedPhase','ControllingPhase','SensorLocation','ControlledNodeId','PythonDeviceScriptID','ShuntCapacitorID','ConnectionStatus','CTConnection','InterruptingRating'])
	ShuntCapacitorSettinglist = []
	IntermediateNodes = namedtuple('IntermediateNodes',['SectionID','SeqNumber','CoordX','CoordY','IsBreakPoint','BreakPointLocation'])
	IntermediateNodeslist = []
	CapacitorExtltd = namedtuple('CapacitorExtltd',['DeviceNumber','DeviceType','EnableDelays','CloseDelay','TripDelay','BreakerDelay'])
	CapacitorExtltdlist = []
	OvercurrentRelayInstrument = namedtuple('OvercurrentRelayInstrument',['InstrumentNumber','InstrumentIndex','Flags','Location','ConnectionStatus','TCCRepositoryID','Manufacturer','Model','RelayType','EnableDirectionalUnit','ForwardNodeID','ForwardTripDirection','MaximumTorqueAngle','PolarizingMode','PolarizingVoltage','PolarizingCurrent','IndependentTripSettings','DirectionalPickup','DirectionalDefiniteTime','PTPrimaryRating','PTSecondaryRating','Pickup','OperatingTime','ObservationDelay','ProtectionType','SymbolText','OwnerDeviceNumber','OwnerDeviceType','TagText','TagDeltaX','TagDeltaY','TagAngle','TagLocation','TagProp','TagAlignment','TagBorder','TagBackground','TagTextColor','TagBorderColor','TagBackgroundColor','TagFont','TagTextSize','TagOffset'])
	OvercurrentRelayInstrumentlist = []
	CurrentTransformerInstrument = namedtuple('CurrentTransformerInstrument',['InstrumentNumber','InstrumentIndex','Flags','Location','ConnectionStatus','PhasePrimaryRating','PhaseSecondaryRating','GroundPrimaryRating','GroundSecondaryRating','PhaseConnection','GroundConnection','DeltaConnection','OwnerDeviceNumber','OwnerDeviceType','TagText','TagDeltaX','TagDeltaY','TagAngle','TagLocation','TagProp','TagAlignment','TagBorder','TagBackground','TagTextColor','TagBorderColor','TagBackgroundColor','TagFont','TagTextSize','TagOffset'])
	CurrentTransformerInstrumentlist = []
	DeviceUdd = namedtuple('DeviceUdd',['DeviceNumber','DeviceType','DataId','DataType','DataValue'])
	DeviceUddlist = []
	Electronicconvertergeneratorsetting = namedtuple('Electronicconvertergeneratorsetting',['SectionID','Location','EqID','DeviceNumber','DeviceStage','Flags','InitFromEquipFlags','EqPhase','NumberOfGenerators','ConnectionStatus','ConnectionConfiguration','FaultContributionBasedOnRatedPower','FaultContributionUnit','FaultContribution','CTConnection','FrequencySourceID'])
	Electronicconvertergeneratorsettinglist = []
	Converter = namedtuple('Converter',['DeviceNumber','DeviceType','ACDCConverterID','Manufacturer','Model','Standard','PhaseType','ConverterRating','ActivePowerRating','ReactivePowerRating','MinimumPowerFactor','Efficiency','InternalLosses','UseDCCapacitor','DCCapacitor','RatedDCVoltage','InternalCouplingElement','CouplingResistance','CouplingInductance','ModelControl','ReactivePowerRef','DCVoltageRef','CurrentRef','KPQ','KIQ','KPD','KID','KPI','KII','PowerFallLimit','PowerRiseLimit','RiseFallUnit'])
	Converterlist = []
	Convertercontrolsetting = namedtuple('Convertercontrolsetting',['DeviceNumber','DeviceType','ControlIndex','TimeTriggerIndex','ControlType','FixedVarInjection','InjectionReference','ConverterControlID','PowerReference','PowerFactor','StartTime','Status','Power','ActivePowerReference','PowerLimit','MonitorRemoteLocation','RemoteItemID','RemoteItemType','DischargeTrigger','DischargeIdleTrigger','DischargeTriggerUnit','ChargeTrigger','ChargeIdleTrigger','ChargeTriggerUnit','ChargePower','DischargePower','ChargePowerReference','DischargePowerReference','LevelTriggerPower','Tolerance','RiseLimit','FallLimit','RiseFallUnit','VoltageReference','HysteresisOffset','MinimumDeadbandVoltage','MaximumDeadbandVoltage','LowVoltageGradient','HighVoltageGradient'])
	Convertercontrolsettinglist = []
	Longtermdynamicscurveext = namedtuple('Longtermdynamicscurveext',['DeviceNumber','DeviceType','AdjustmentSettings','PowerCurveModel','PowerCurveModelId','ApplyOutputPowerLimit'])
	Longtermdynamicscurveextlist = []
	Dggenerationmodel = namedtuple('Dggenerationmodel',['DeviceNumber','DeviceType','LoadModelName','ActiveGeneration','PowerFactor'])
	Dggenerationmodellist = []
	Controlleddevice = namedtuple('Controlleddevice',['InstrumentNumber','InstrumentType','SeqNumber','Active','DeviceNumber','DeviceType','OverCondition','ObservationDelay','Threshold','Operation'])
	Controlleddevicelist = []
	#read the file
	with open(filename,'r') as inputfile:
		Lineset = inputfile.readlines()
		#now we will go through the file, line by line. Skip the initial lines.
		linenum = 7

		#NODE
		while not Lineset[linenum].startswith('[NODE]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Node] and FORMAT_ Node
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Node(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38],line[39],line[40],line[41],line[42],line[43],line[44],line[45],line[46],line[47])
				Nodelist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#HEADNODES
		while not Lineset[linenum].startswith('[HEADNODES]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Headnodes] and FORMAT_ Headnodes
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = HeadNodes(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8])
				HeadNodeslist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#SOURCE
		while not Lineset[linenum].startswith('[SOURCE]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Source] and FORMAT_ Source
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Source(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9])
				Sourcelist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#SOURCE EQUIVALENT
		while not Lineset[linenum].startswith('[SOURCE EQUIVALENT]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Sourceequivalent] and FORMAT_ Sourceequivalent
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = SourceEquivalent(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23])
				SourceEquivalentlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#LOAD EQUIVALENT
		while not Lineset[linenum].startswith('[LOAD EQUIVALENT]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Loadequivalent] and FORMAT_ Loadequivalent
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = LoadEquivalent(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12])
				LoadEquivalentlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#DEVICE STAGE
		while not Lineset[linenum].startswith('[DEVICE STAGE]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Devicestage] and FORMAT_ Devicestage
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = DeviceStage(line[0],line[1],line[2],line[3],line[4])
				DeviceStagelist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#OOVERHEAD BYPHASE SETTING
		while not Lineset[linenum].startswith('[OVERHEAD BYPHASE SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
			# if linenum == len(Lineset):
				# linenum = 0
				# break
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Overheadbyphasesetting] and FORMAT_ Overheadbyphasesetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = OverheadByphaseSetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37])
				OverheadByphaseSettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#UNDERGROUNDLINE SETTING
		while not Lineset[linenum].startswith('[UNDERGROUNDLINE SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Undergroundlinesetting] and FORMAT_ Undergroundlinesetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = UndergroundlineSetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36])
				UndergroundlineSettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#Section and Feeder
		while not Lineset[linenum].startswith('[SECTION]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 3#[Section] and FORMAT_ Section and FORMAT_ Feeder
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				if line.startswith('FEEDER='):
					line = line.split(',')
					elem = Feeder(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32])
					Feederlist.append(elem)
					linenum = linenum + 1
				else:
					line = line.split(',')
					elem = Section(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8])
					Sectionlist.append(elem)
					linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#ELECTRONIC CONVERTER GENERATOR SETTING
		while not Lineset[linenum].startswith('[ELECTRONIC CONVERTER GENERATOR SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Electronicconvertergeneratorsetting] and FORMAT_ Electronicconvertergeneratorsetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Electronicconvertergeneratorsetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15])
				Electronicconvertergeneratorsettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#TRANSFORMER SETTING]
		while not Lineset[linenum].startswith('[TRANSFORMER SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Transformersetting] and FORMAT_ Transformersetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = TransformerSetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38],line[39],line[40],line[41],line[42],line[43],line[44],line[45],line[46],line[47],line[48])
				TransformerSettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#SWITCH SETTING
		while not Lineset[linenum].startswith('[SWITCH SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Switchsetting] and FORMAT_ Switchsetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = SwitchSetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26])
				SwitchSettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#BREAKER SETTING
		while not Lineset[linenum].startswith('[BREAKER SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Breakersetting] and FORMAT_ Breakersetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = BreakerSetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38],line[39])
				BreakerSettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#FUSE SETTING
		while not Lineset[linenum].startswith('[FUSE SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Fusesetting] and FORMAT_ Fusesetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = FuseSetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26])
				FuseSettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#SHUNT CAPACITOR SETTING
		while not Lineset[linenum].startswith('[SHUNT CAPACITOR SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Shuntcapacitorsetting] and FORMAT_ Shuntcapacitorsetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = ShuntCapacitorSetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38],line[39],line[40],line[41],line[42])
				ShuntCapacitorSettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#INTERMEDIATE NODES
		while not Lineset[linenum].startswith('[INTERMEDIATE NODES]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Intermediatenodes] and FORMAT_ Intermediatenodes
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = IntermediateNodes(line[0],line[1],line[2],line[3],line[4],line[5])
				IntermediateNodeslist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#CONVERTER
		while not Lineset[linenum].startswith('[CONVERTER]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Converter] and FORMAT_ Converter
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Converter(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31])
				Converterlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#CONVERTER CONTROL SETTING
		while not Lineset[linenum].startswith('[CONVERTER CONTROL SETTING]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Convertercontrolsetting] and FORMAT_ Convertercontrolsetting
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Convertercontrolsetting(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38])
				Convertercontrolsettinglist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#CAPACITOR EXTLTD
		while not Lineset[linenum].startswith('[CAPACITOR EXTLTD]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Capacitorextltd] and FORMAT_ Capacitorextltd
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = CapacitorExtltd(line[0],line[1],line[2],line[3],line[4],line[5])
				CapacitorExtltdlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#LONG TERM DYNAMICS CURVE EXT
		while not Lineset[linenum].startswith('[LONG TERM DYNAMICS CURVE EXT]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Longtermdynamicscurveext] and FORMAT_ Longtermdynamicscurveext
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Longtermdynamicscurveext(line[0],line[1],line[2],line[3],line[4],line[5])
				Longtermdynamicscurveextlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#DGGENERATIONMODEL
		while not Lineset[linenum].startswith('[DGGENERATIONMODEL]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Dggenerationmodel] and FORMAT_ Dggenerationmodel
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Dggenerationmodel(line[0],line[1],line[2],line[3],line[4])
				Dggenerationmodellist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0

		#OVERCURRENT RELAY INSTRUMENT
		while not Lineset[linenum].startswith('[OVERCURRENT RELAY INSTRUMENT]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Overcurrentrelayinstrument] and FORMAT_ Overcurrentrelayinstrument
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = OvercurrentRelayInstrument(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38],line[39],line[40],line[41],line[42])
				OvercurrentRelayInstrumentlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#CURRENT TRANSFORMER INSTRUMENT
		while not Lineset[linenum].startswith('[CURRENT TRANSFORMER INSTRUMENT]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Currenttransformerinstrument] and FORMAT_ Currenttransformerinstrument
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = CurrentTransformerInstrument(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28])
				CurrentTransformerInstrumentlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#DEVICEUDD
		while not Lineset[linenum].startswith('[DEVICEUDD]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Deviceudd] and FORMAT_ Deviceudd
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = DeviceUdd(line[0],line[1],line[2],line[3],line[4])
				DeviceUddlist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0
		
		#CONTROLLED DEVICE INSTRUMENT
		while not Lineset[linenum].startswith('[CONTROLLED DEVICE INSTRUMENT]') and linenum < (len(Lineset)-1):
			linenum = linenum + 1
		if	linenum < (len(Lineset)-1):
			linenum = linenum + 2#[Controlleddevice] and FORMAT_ Controlleddevice
			while not len(Lineset[linenum].strip()) == 0:#read data till we reach a blank line
				line = Lineset[linenum].strip()
				line = line.split(',')
				elem = Controlleddevice(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9])
				Controlleddevicelist.append(elem)
				linenum = linenum + 1
			#linenum = linenum + 1
		linenum = 0


	return Nodelist, HeadNodeslist, Sourcelist, SourceEquivalentlist, LoadEquivalentlist, DeviceStagelist, OverheadByphaseSettinglist, UndergroundlineSettinglist, Sectionlist, Feederlist, TransformerSettinglist, SwitchSettinglist, BreakerSettinglist, FuseSettinglist, ShuntCapacitorSettinglist, IntermediateNodeslist, CapacitorExtltdlist, OvercurrentRelayInstrumentlist, CurrentTransformerInstrumentlist, DeviceUddlist, Electronicconvertergeneratorsettinglist, Converterlist,  Convertercontrolsettinglist, Longtermdynamicscurveextlist, Dggenerationmodellist, Controlleddevicelist

if __name__ == "__main__":
	print('Please do not run this file, run the main file!')