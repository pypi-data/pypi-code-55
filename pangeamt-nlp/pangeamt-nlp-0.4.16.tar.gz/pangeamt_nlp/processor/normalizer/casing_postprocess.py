from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg


class CasingPostprocess(NormalizerBase):
    NAME = "casing_postprocess"

    DESCRIPTION_TRAINING = """"""

    DESCRIPTION_DECODING = """
        Copy the casing of the source
    """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        pass

    def process_tgt_decoding(self, seg: Seg) -> None:
        if seg.src.isupper():
            seg.tgt = seg.tgt.upper()
        elif seg.src[0].isupper():
           seg.tgt = seg.tgt[0].upper() + seg.tgt[1:]
        elif seg.src[0].islower():
            seg.tgt = seg.tgt[0].lower() + seg.tgt[1:]
        seg.tgt = seg.tgt
