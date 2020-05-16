
import re;

regobj = re.compile("^(?P<raw>\w+)(\<(?P<parameters>.*)\>)?$", re.I);


def testParse( input):
	print('Parse : ' , input);
	m = regobj.search(input )
	if m != None:
		#			print 'line' + line
		raw = m.group('raw')
		isexist = m.group(3)
		if isexist == None:
			isexist = '<None>';
		else:
			if len(isexist) == 0:
				isexist = '<Empty>';

		p = m.group('parameters');
		if p == None:
			p = '<None>';
		else:
			if len(p) == 0:
				p = '<Empty>';

		print('RAW=' , raw , 'EXIST=', isexist, ' P is' , p );
	else:
		print('Not find' )

	print();


testParse('List');
testParse('Map');
testParse('List<>');
testParse('Map<>');

testParse('List<string>');
testParse('Map<type1,type2>');
testParse('List<Map>');
testParse('List<Map<type1,type2>>');