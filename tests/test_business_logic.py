import pytest

from ..dto import BlobRefDTO
from ..business_logic import Handler


@pytest.mark.parametrize(
    "blob_dto,expected_reason",
    [
        pytest.param(
            BlobRefDTO(
                blob_id=1,
                num_ref=1,
                sent_att=0,
                sent_msg=0,
                body=0,
                header=0,
                att=0,
                out_att=0,
                contact_data=0,
            ),
            "ORPHAN_BLOB",
            id="orphan_blob",
        ),
        pytest.param(
            BlobRefDTO(
                blob_id=1,
                num_ref=3,
                sent_att=1,
                sent_msg=1,
                body=1,
                header=1,
                att=1,
                out_att=1,
                contact_data=1,
            ),
            "COUNT_MISMATCH",
            id="count_mismatch",
        ),
    ],
)
def test_orphan_blob(blob_dto, expected_reason):
    h = Handler(dto=blob_dto)
    h.process()
    assert expected_reason in h.msg
