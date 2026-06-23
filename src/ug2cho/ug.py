import dataclasses
import strictyaml
import re

@dataclasses.dataclass
class UG:
    leadsheet: str
    metadata: dict()

    def to_str(self):
        metadata = self.metadata.copy()
        metadata.pop('applicature')   # applicature is huge, don't bother with it for now

        meta_yaml = strictyaml.as_document(metadata)
        header = meta_yaml.as_yaml()

        return f'---\n{header}---\n{self.leadsheet}'

    @staticmethod
    def from_str(s):
        items = s.split('---\n', 3)
        if len(items) == 3:
            _, header, leadsheet = items
        elif len(items) == 2:
            header, leadsheet = items
        else:
            leadsheet = s
            header = dict()

        metadata = strictyaml.load(header).data

        return UG(
            leadsheet=leadsheet,
            metadata=metadata,
        )

    def plain_text_leadsheet(self):
        txt = self.leadsheet
        txt = txt.replace("[tab]", "")
        txt = txt.replace("[/tab]", "")
        txt = re.sub(r'\[ch\]([^\[]*)\[\/ch\]', lambda match: match.group(1), txt)
        return txt
