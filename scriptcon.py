import unicodedata

def preCommon(text):
	text = text.replace('ng','ŋ')
	return(text)

def postCommon(text):
	text = unicodedata.normalize('NFC', unicodedata.normalize('NFD', text))
	return(text)

def toCyrillic(text):
	dataCyrillic = [
	('Pf','ԥ'),
	('pF','ԥ'),
	('PF','ԥ'),
	('pf','ԥ'),
#----
	('Tþ','ҭ'),
	('tÞ','ҭ'),
	('TÞ','ҭ'),
	('tþ','ҭ'),
#----
	('Kx','қ'),
	('kX','қ'),
	('KX','қ'),
	('kx','қ')
	]
	for x in dataCyrillic:
		text = text.replace(x[0],x[1])
	a = 'aæbdegiklmnoprtuyŋ'
	a = a + a.upper()
	b = 'аӕбдегиклмнопртуүҥ'
	b = b + b.upper()
	text = text.translate(str.maketrans(a,b))
	return(postCommon(text))

def toKatakana(text):
	finals = {ord('b'):'ㇷ゙', ord('d'):'ㇳ゙', ord('g'): 'ㇰ゙', ord('k'): 'ㇰ', ord('l'): 'ㇽ゚', ord('m'): 'ㇺ', ord('n'): 'ン', ord('p'): 'ㇷ゚', ord('r'): 'ㇽ', ord('t'): 'ㇳ', ord('ŋ'): 'ㇰ゚'}
	
	
	for x in [('ka','カ'),('ki','キ'),('ku','ク'),('ke','ケ'),('ko','コ')]:
		text = text.replace(x[0],x[1])

	for x in [('ga','ガ'),('gi','ギ'),('gu','グ'),('ge','ゲ'),('go','ゴ')]:
		text = text.replace(x[0],x[1])

	for x in [('ŋa','カ゚'),('ŋi','キ゚'),('ŋu','ク゚'),('ŋe','ケ゚'),('ŋo','コ゚')]:
		text = text.replace(x[0],x[1])

	for x in [('kxa','カㇵ'),('kxi','キㇶ'),('kxu','クㇷ'),('kxe','ケㇸ'),('kxo','コㇹ')]:
		text = text.replace(x[0],x[1])

	for x in [('ta','タ'),('ti','チ'),('tu','ツ'),('te','テ'),('to','ト')]:
		text = text.replace(x[0],x[1])

	for x in [('da','ダ'),('di','ヂ'),('du','ヅ'),('de','デ'),('do','ド')]:
		text = text.replace(x[0],x[1])

	for x in [('tþa','タ゚'),('tþi','チ゚'),('tþu','ツ゚'),('tþe','テ゚'),('tþo','ト゚')]:
		text = text.replace(x[0],x[1])

	for x in [('na','ナ'),('ni','ニ'),('nu','ヌ'),('ne','ネ'),('no','ノ')]:
		text = text.replace(x[0],x[1])

	for x in [('pa','パ'),('pi','ピ'),('pu','プ'),('pe','ペ'),('po','ポ')]:
		text = text.replace(x[0],x[1])

	for x in [('ba','バ'),('bi','ビ'),('bu','ブ'),('be','ベ'),('bo','ボ')]:
		text = text.replace(x[0],x[1])

	for x in [('pfa','パㇵ'),('pfi','ピㇶ'),('pfu','プㇷ'),('pfe','ペㇸ'),('pfo','ポㇹ')]:
		text = text.replace(x[0],x[1])

	for x in [('ma','マ'),('mi','ミ'),('mu','ム'),('me','メ'),('mo','モ')]:
		text = text.replace(x[0],x[1])

	for x in [('ra','ラ'),('ri','リ'),('ru','ル'),('re','レ'),('ro','ロ')]:
		text = text.replace(x[0],x[1])

	for x in [('la','ラ゚'),('li','リ゚'),('lu','ル゚'),('le','レ゚'),('lo','ロ゚')]:
		text = text.replace(x[0],x[1])

	for x in [('a','ア'),('i','イ'),('u','ウ'),('e','エ'),('o','オ')]:
		text = text.replace(x[0],x[1])


	text = text.replace(' ','・')


	text = text.translate(finals)

	return(postCommon(text))


def toLontara(text):
	dataCyrillic = [('pf','ᨓ'),('tþ','ᨔ'),('kx','ᨖ')]
	for x in dataCyrillic:
		text = text.replace(x[0],x[1])
	a = 'bdgklmnprtŋ'
	a = a + a.upper()
	b = 'ᨅᨉᨁᨀᨒᨆᨊᨄᨑᨈᨂ'
	b = b + b
	text = text.translate(str.maketrans(a,b))
	return(postCommon(text))
