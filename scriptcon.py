import unicodedata

def preCommon(text):
#	text = unicodedata.normalize('NFC', unicodedata.normalize('NFD', text))
	text = text.replace('ng','ŋ')
	return(text)

def postCommon(text):
	text = unicodedata.normalize('NFC', unicodedata.normalize('NFD', text))
	text = text.replace('\\','')
	return(text)

def toCyrillic(text):
	text = preCommon(text)
	text = unicodedata.normalize('NFD', text)
	dataCyrillic = [
	('Pf','Ԥ'),
	('pF','ԥ'),
	('PF','Ԥ'),
	('pf','ԥ'),
#----
	('Tþ','Ҭ'),
	('tÞ','ҭ'),
	('TÞ','Ҭ'),
	('tþ','ҭ'),
#----
	('Kx','Қ'),
	('kX','қ'),
	('KX','Қ'),
	('kx','қ')
	]
	for x in dataCyrillic:
		text = text.replace(x[0],x[1])
	a = 'aæbdegiklmnoprtuyŋ'
	a = a + a.upper()
	b = 'аӕбдегиклмнопртуүҥ'
	b = b + b.upper()
	text = text.translate(str.maketrans(a,b))
	text = unicodedata.normalize('NFC', text)
	return(postCommon(text))

def toKatakana(text):
	text = preCommon(text)
	text = text.lower()
	finals = {ord('b'):'ㇷ゙', ord('d'):'ㇳ゙', ord('g'): 'ㇰ゙', ord('k'): 'ㇰ', ord('l'): 'ㇽ゚', ord('m'): 'ㇺ', ord('n'): 'ン', ord('p'): 'ㇷ゚', ord('r'): 'ㇽ', ord('t'): 'ㇳ', ord('ŋ'): 'ㇰ゚'}
	
	
	for x in [('ka','カ'),('ki','キ'),('ku','ク'),('ke','ケ'),('ko','コ')]:
		text = text.replace(x[0],x[1])

	for x in [('ga','ガ'),('gi','ギ'),('gu','グ'),('ge','ゲ'),('go','ゴ')]:
		text = text.replace(x[0],x[1])

	for x in [('ŋa','カ゚'),('ŋi','キ゚'),('ŋu','ク゚'),('ŋe','ケ゚'),('ŋo','コ゚')]:
		text = text.replace(x[0],x[1])

	for x in [('kxa','カㇵ'),('kxi','キㇶ'),('kxu','クㇷ'),('kxe','ケㇸ'),('kxo','コㇹ')]:
		text = text.replace(x[0],x[1])

	for x in [('ta','タ'),('ti','ティ'),('tu','トゥ'),('te','テ'),('to','ト')]:
		text = text.replace(x[0],x[1])

	for x in [('da','ダ'),('di','ディ'),('du','ドゥ'),('de','デ'),('do','ド')]:
		text = text.replace(x[0],x[1])

	for x in [('tþa','タ゚'),('tþi','テ゚ィ'),('tþu','ト゚ゥ'),('tþe','テ゚'),('tþo','ト゚')]:
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
	text = preCommon(text)
	dataLontara = [('pf','ᨓ'),('tþ','ᨔ'),('kx','ᨖ')]
	consonants = 'ᨅᨉᨁᨀᨒᨆᨊᨄᨑᨈᨂᨓᨔᨖ'
	for x in dataLontara:
		text = text.replace(x[0],x[1])
	a = 'bdgklmnprtŋ'
	a = a + a.upper()
	b = 'ᨅᨉᨁᨀᨒᨆᨊᨄᨑᨈᨂ'
	b = b + b
	text = text.translate(str.maketrans(a,b))

	for vowel in [('i', 'ᨗ'), ('u', 'ᨘ'), ('e', 'ᨙ'), ('o', 'ᨚ')]:
		while vowel[0] in text:
			if text[text.find(vowel[0])-1] in consonants and text.find(vowel[0]) > 0:
				text = text.replace(vowel[0], vowel[1], 1)
			else:
				text = text.replace(vowel[0], 'ᨀ'+vowel[1], 1)

	return(postCommon(text))
