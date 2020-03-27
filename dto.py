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

    def create_pretty_report(self):
        return f"""#BlobStorage.ID: {self.blob_id}\n"""