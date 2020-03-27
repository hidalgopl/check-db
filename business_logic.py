from dto import BlobRefDTO


class Handler:
    def __init__(self, dto: BlobRefDTO):
        self.dto = dto
        self.real_num_ref = self._count_rel_num_ref()
        self.msg = ""

    def _count_rel_num_ref(self) -> int:
        return (
            self.dto["sent_msg"]
            + self.dto["sent_att"]
            + self.dto["body"]
            + self.dto["header"]
            + self.dto["att"]
            + self.dto["out_att"]
            + self.dto["contact_data"]
        )

    def _detect_inconsistency_type(self) -> str:
        if self.real_num_ref == 0 and self.dto["num_ref"]:
            return "ORPHAN_BLOB"
        if self.real_num_ref != self.dto["num_ref"]:
            return "COUNT_MISMATCH"

    def _prepare_msg(self, reason: str):
        if reason is None:
            return ""
        self.msg = f"BlobID: {self.dto['blob_id']} {reason}:\n{self.dto}"
        print(self.msg)

    def process(self):
        reason = self._detect_inconsistency_type()
        return self._prepare_msg(reason)
