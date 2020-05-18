from deliverable_model.builtin.processor.biluo_decode_processor import (
    BILUOEncodeProcessor,
)
from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder
from tokenizer_tools.tagset.exceptions import TagSetDecodeError
from tokenizer_tools.tagset.offset.sequence import Sequence
from tokenizer_tools.tagset.offset.document import Document


def test_build(datadir, tmpdir):
    processor = BILUOEncodeProcessor()
    config = processor.serialize(tmpdir)
    print("config:", processor)
    pass


def test_postprocess(datadir, tmpdir):
    # with decode success
    processor = BILUOEncodeProcessor.load({}, None)
    faked_request = {"data": [[i for i in "上海明天天气"]]}
    processor.preprocess(faked_request)
    faked_response = {"data": [["B-city", "L-city", "O", "O", "O", "O"]]}
    result = processor.postprocess(faked_response)["data"][0]

    assert isinstance(result.sequence, Document)
    assert result.is_failed == False

    # with decode failed
    processor = BILUOEncodeProcessor.load({}, None)
    faked_request = {"data": [[i for i in "上海明天天气"]]}
    processor.preprocess(faked_request)
    faked_response = {"data": [["B-city", "B-city", "O", "O", "O", "O"]]}
    result = processor.postprocess(faked_response)["data"][0]

    assert isinstance(result.sequence, Document)
    assert result.is_failed == True
