import printer


def configSectionMap(config,section):
	dict1 = {}
	options = config.options(section)
	for option in options:
		try:
			dict1[option] = config.get(section, option)
			if dict1[option] == -1:
				printer.warn("skip: %s" % option)
		except:
			printer.error("exception on %s!" % option)
			dict1[option] = None
	return dict1


def getKeyFromDict(dict, key):
	if key in dict:
		return dict[key]
	else:
		return None
