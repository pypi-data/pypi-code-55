# clirail: command line interface to iRail
# Copyright © 2019 Midgard
# License: GPLv3+

from .config import LANG


_messages = {
	"en": {
		"public_log": """This program uses the iRail API. All requests to iRail are \x1b[1mpublically logged\x1b[0m.
Learn more at the iRail API documentation: https://docs.irail.be/#log-and-feedback-data
If you are okay with this, press Enter to continue. Otherwise, press Ctrl+C.""",

		"downloading_stations": "Downloading list of stations… This only needs to be done once.",

		"didnt_understand_moment": """Didn’t understand moment “{moment}”, try writing it in another way.
Examples of easily understood moments are “8:30” and “2019-01-01, 8:30”.""",

		"canceled": "canceled",

		"departure_in": "Departure in {station}",
		"departure_in_w_code": "Departure in {station} ({telegraphic_code})",

		"train": "train",
		"destination": "destination",
		"platform": "platform",
		"departure": "departure",
		"duration": "dur.",
		"dep_arr": "dep/arr",
		"station": "station",
		"towards": "towards",

		"go_to_next_station": "go to the next station on your own",
	},

	"nl": {
		"public_log": """Dit programma gebruikt de iRail-API. Alle opzoekingen bij iRail worden \x1b[1mpubliek gelogd\x1b[0m.
Lees meer in de iRail-API-documentatie (in het Engels): https://docs.irail.be/#log-and-feedback-data
Als dit oké is, druk dan Enter om door te gaan. Druk anders Ctrl+C.""",

		"downloading_stations": "Lijst van stations downloaden… Dit moet maar één keer gebeuren.",

		"didnt_understand_moment": """Moment “{moment}” werd niet begrepen, probeer het eens op een andere manier te schrijven.
Voorbeelden van gemakkelijk te begrijpen momenten zijn “8:30” en “2019-01-01, 8:30”.""",

		"canceled": "afgeschaft",

		"departure_in": "Vertrek in {station}",
		"departure_in_w_code": "Vertrek in {station} ({telegraphic_code})",

		"train": "trein",
		"destination": "bestemming",
		"platform": "spoor",
		"departure": "vertrek",
		"duration": "duur",
		"dep_arr": "ver/aan",
		"station": "station",
		"towards": "richting",

		"go_to_next_station": "raak zelf in volgende station",
	}
}

def t(key):
	return _messages \
		.get(LANG, _messages["en"]) \
		.get(key, "Missing translation for " + key)
