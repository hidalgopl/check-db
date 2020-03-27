from typing_extensions import TypedDict


class BlobRefDTO(TypedDict):
    blob_id: int
    num_ref: int
    sent_msg: int
    sent_att: int
    body: int
    header: int
    att: int
    out_att: int
    contact_data: int
