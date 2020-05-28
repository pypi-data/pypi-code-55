#! python3  # noqa: E265

"""
    Localization module.

    Author: Isogeo

    See: https://docs.python.org/fr/3/library/gettext.html#module-gettext
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import gettext
import locale
import logging
from pathlib import Path

# package
from scan_metadata_processor.__about__ import __package_name__

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Functions #############
# ##################################


class Localizer(object):
    """Localization module.

    :param str lang_code: language code to use for translation. Defaults to: None - optional
    """

    LANGUAGE_CODE_DEFAULT = "en_GB"
    LANGUAGE_CODE_TO_USE = "fr_FR"

    tr = gettext.gettext

    def __init__(self, lang_code: str = "fr_FR"):
        """Instanciation method."""
        if lang_code is not None:
            self.LANGUAGE_CODE_TO_USE = lang_code
            self.locale_setter(lang_code)
        else:
            # if not set, use system
            self.LANGUAGE_CODE_TO_USE = locale.getdefaultlocale()[0]
            self.locale_setter(locale.getdefaultlocale()[0])

        # init translator with required language
        self.init_translator()

    def init_translator(self) -> gettext.gettext:
        """Handy shortcut to initialize the translator functions.

        :return: gettext translator method
        :rtype: gettext.gettext

        :example:

        .. code-block:: python

            _ = init_translator()
            print(_("Hello Mister Computer!"))
        """
        localedir = Path(__file__).parent / Path("../i18n")
        gettext.bindtextdomain(__package_name__, localedir)
        try:
            translate = gettext.translation(
                domain=__package_name__,
                localedir=str(localedir.resolve()),
                fallback=False,
                languages=[self.LANGUAGE_CODE_TO_USE],
            )
        except FileNotFoundError:
            if not self.LANGUAGE_CODE_TO_USE.startswith("en"):
                logger.warning(
                    "No translation found for language: {}. Using raw texts.".format(
                        self.LANGUAGE_CODE_TO_USE
                    )
                )
            self.LANGUAGE_CODE_TO_USE = self.LANGUAGE_CODE_DEFAULT
            translate = gettext.translation(
                domain=__package_name__,
                localedir=str(localedir.resolve()),
                fallback=True,
                languages=[self.LANGUAGE_CODE_TO_USE],
            )

        translate.install(__package_name__)
        logger.debug(
            "Translation loaded for language: {}".format(self.LANGUAGE_CODE_TO_USE)
        )
        self.tr = translate.gettext
        return translate.gettext

    @staticmethod
    def locale_setter(expected_locale: str = "en_EN"):
        """Ensure locale is the expected one.

        :param str expected_locale: locale code to set. Defaults to: "fr_FR" - optional
        """
        # get the default locale on system
        default_locale = locale.getdefaultlocale()  # -> tuple

        # compare with the expected locale
        if default_locale[0] == expected_locale:
            logger.debug(
                "Default locale is matching the expected one: {}".format(
                    expected_locale
                )
            )
            locale.setlocale(locale.LC_ALL, "")
        else:
            logger.debug(
                "Default locale ({}) is not the expected one: {}. "
                "Change will be effective until the end of program.".format(
                    default_locale, expected_locale
                )
            )
            try:
                locale.setlocale(locale.LC_ALL, expected_locale)
            except locale.Error as err:
                logger.warning(
                    "Expected locale is not available on this system or "
                    "application is not translated intot this. "
                    "Falling back to default locale: {}. Trace: {}.".format(
                        default_locale[0], err
                    )
                )
                locale.resetlocale()
